@description('An existing Azure OpenAI resource')
param openAIName string = ''

@description('An existing Azure OpenAI resource group')
param openAIRGName string = ''

@description('The location in which all resources should be deployed.')
param location string = resourceGroup().location

@description('The region for the Azure AI Search service')
@allowed(['francecentral', 'eastus', 'eastus2', 'japaneast'])
param aiSearchRegion string = 'eastus'

@description('A prefix that will be prepended to resource names')
@minLength(2)
@maxLength(10)
param namePrefix string = 'dev'

@description('Location for a new Azure OpenAI resource. Leave openAIName and openAIRGName empty to deploy a new resource.')
@allowed(['swedencentral', 'eastus', ''])
param newOpenAILocation string = ''

@description('True to avoid building images from the repo. In this case images must be published via push.ps1 script')
param skipImageBuild bool = false

@description('Git repo from which the Docker images are built (must contain the app code patches)')
param gitRepoUrl string = 'https://github.com/AT2018cow/multimodal-rag-code-execution'

@description('Branch of gitRepoUrl used to build the Docker images')
param gitRepoBranch string = 'main'

var uniqueid = uniqueString(resourceGroup().id)
var di_location = 'westeurope'

// ---- Log Analytics workspace ----
var logWorkspaceName = 'log-${uniqueid}'
resource logWorkspace 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logWorkspaceName
  location: location  
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

// Application insights resource
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: '${namePrefix}-appin-${uniqueid}'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logWorkspace.id
  }
}

// Deploy storage account with private endpoint and private DNS zone
module storageModule 'storage.bicep' = {
  name: 'storageDeploy'
  params: {
    location: location
    namePrefix: namePrefix
    uniqueid: uniqueid        
  }
}

module acr 'registry.bicep' = {
  name: 'acrDeploy'
  params: {
    location: location
    uniqueid: uniqueid
    namePrefix: namePrefix
  }
}

module buildImages 'modules/build-images.bicep' = if (!skipImageBuild) {
  name: 'buildImages'
  params: {
    acrName: acr.outputs.containerRegistryName
    gitRepoUrl: gitRepoUrl
    gitRepoBranch: gitRepoBranch
  }
  dependsOn: [
    acr
  ]
}

module openAIResource 'openai.bicep' = {
  name: 'openaiDeploy'
  params: {
    openAIName: openAIName
    openAIRGName: openAIRGName
    namePrefix: namePrefix
    location: !empty(newOpenAILocation) ? newOpenAILocation : 'swedencentral'
    envName: namePrefix
  }
}


module azureVisionResource 'vision.bicep' =  {
  name: 'azureVisionResource'
  params: {
    uniqueid: uniqueid
    location: location       
    namePrefix:namePrefix         
  }
}

module cosmosDbModule 'cosmosdb.bicep' =  {
  name: 'cosmosdbDeploy'
  params: {
    location: location
    uniqueid: uniqueid
    namePrefix:namePrefix
  }
}

module ai_search 'ai_search.bicep' = {
  name: 'ai_search'
  params: {
    uniqueid: uniqueid
    aiSearchRegion: aiSearchRegion
    namePrefix:namePrefix                
  }
}

module documentInteligence 'documentintelligence.bicep' =  {
  name: 'document-Intelligence'
  params: {
    namePrefix:namePrefix
    documentIntelligence: 'doc-int'
    uniqueid:  uniqueid
    location: di_location
  }
}

module machineLearning 'machine_learning.bicep' =  {
  name: 'machine-learing-worksapce'
  params: {
    namePrefix:namePrefix
    machineLearningName: 'mlws' 
    uniqueid:  uniqueid
    location: location
    appInsightsId: appInsights.id
    acrId: acr.outputs.containerRegistryId
  }
}

// Deployment script from modules
module script 'modules/script.bicep' = {
  name: 'script'
  params: {
    uniqueid: uniqueid
    storageName: storageModule.outputs.storageName
  }
  dependsOn: [
    storageModule
  ]
}

module uami 'uami.bicep' = {
  name: 'uami'
  params: {
    location: location
    uniqueId: uniqueid
    prefix: namePrefix
    storageName: storageModule.outputs.storageName
    mlWorkspaceName: machineLearning.outputs.workspaceName
    acrName: acr.outputs.containerRegistryName
  }
}

// App hosting, split across two meters (see AGENTS.md "Microsoft for Startups cost setup"):
// - App Service B3 plan hosts the API + Chainlit chat apps (webapp.bicep)
// - one Azure Container App hosts the streamlit UI (aca_streamlit.bicep)
module webapps 'webapp.bicep' = {
  name: 'webapp'
  params: {
    location: location
    uniqueId: uniqueid
    prefix: namePrefix
    uamiId: uami.outputs.uamiId
    uamiClientId: uami.outputs.uamiClientId
    aiSearchAdminKey: ai_search.outputs.aiSearchAdminKey
    aiSearchEndpoint: ai_search.outputs.aiSearchEndpoint
    aiSearchRegion: aiSearchRegion
    cosmosDbKey: cosmosDbModule.outputs.cosmosDbKey
    cosmosdbName: cosmosDbModule.outputs.cosmosdbName
    cosmosDbUri: cosmosDbModule.outputs.cosmosDbUri
    openAiApiKey: openAIResource.outputs.aoaiResourceKey
    openAiName: openAIResource.outputs.aoaiResourceName
    storageKey: storageModule.outputs.storageKey
    storageName: storageModule.outputs.storageName
    documentIntelligenceEndpoint: documentInteligence.outputs.documentIntelligenceEndpoint
    documentIntelligenceKey: documentInteligence.outputs.documentIntelligenceKey
    accountsVisionEndpoint: azureVisionResource.outputs.accountsVisionEndpoint
    accountsVisionKey: azureVisionResource.outputs.accountsVisionKey
    mlWorkspaceName: machineLearning.outputs.workspaceName
    logAnalyticsWorkspaceName: logWorkspace.name
    containerRegistryName: acr.outputs.containerRegistryName
    containerRegistryPassword: acr.outputs.containerRegistryPassword
    applicationInsightsInstrumentationKey: appInsights.properties.InstrumentationKey
  }
  dependsOn: [
    uami
    openAIResource
    ai_search
    cosmosDbModule
    storageModule
    documentInteligence
    azureVisionResource
    machineLearning
    acr
  ]
}

module acaStreamlit 'aca_streamlit.bicep' = {
  name: 'acaStreamlit'
  params: {
    uniqueId: uniqueid
    prefix: namePrefix
    uamiId: uami.outputs.uamiId
    containerRegistry: acr.outputs.containerRegistryName
    location: location
    logAnalyticsWorkspaceName: logWorkspace.name
    apiBaseUrl: webapps.outputs.apiUrl
    skipImagePulling: skipImageBuild
  }
  dependsOn: [
    webapps
    acr
    buildImages
  ]
}

output chatUrl string = webapps.outputs.chatUrl
output mainUrl string = acaStreamlit.outputs.mainContainerAppUrl
