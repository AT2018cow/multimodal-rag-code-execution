// Azure Container Apps module hosting ONLY the streamlit app (Ingestion + Prompt
// Management UI). The chat and API apps live on the shared App Service plan
// (webapp.bicep). Hosting streamlit separately here keeps the Microsoft.App
// service meter above the Microsoft for Startups daily minimum-spend threshold
// (~$1.25/day at 0.5 cpu / 1GiB with minReplicas 1) while giving the app a
// public URL.
param uniqueId string
param prefix string
param uamiId string
param containerRegistry string = '${prefix}acr${uniqueId}'
param location string = resourceGroup().location
param logAnalyticsWorkspaceName string
param apiBaseUrl string
param skipImagePulling bool = false

var mainContainerImage = !skipImagePulling ? '${containerRegistry}.azurecr.io/research-copilot-main:latest' : 'mcr.microsoft.com/mcr/hello-world'

resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' existing = {
  name: logAnalyticsWorkspaceName
}

resource containerAppEnv 'Microsoft.App/managedEnvironments@2023-11-02-preview' = {
  name: '${prefix}-containerAppEnv-${uniqueId}'
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${uamiId}': {}
    }
  }
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsWorkspace.properties.customerId
        sharedKey: logAnalyticsWorkspace.listKeys().primarySharedKey
      }
    }
  }
}

resource mainContainerApp 'Microsoft.App/containerApps@2023-11-02-preview' = {
  name: '${prefix}-main-${uniqueId}'
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${uamiId}': {}
    }
  }
  properties: {
    managedEnvironmentId: containerAppEnv.id
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: true
        targetPort: 80
        transport: 'auto'
      }
      registries: [
        {
          server: '${containerRegistry}.azurecr.io'
          identity: uamiId
        }
      ]
    }
    template: {
      scale: {
        minReplicas: 1
        maxReplicas: 1
      }
      containers: [
        {
          name: 'ui'
          image: mainContainerImage
          resources: {
            cpu: json('0.5') // bicep has no float literals; 0.5 is the minimum viable CPU for the UI
            memory: '1Gi'
          }
          env: [
            {
              name: 'API_BASE_URL'
              value: apiBaseUrl
            }
          ]
        }
      ]
    }
  }
}

output mainContainerAppUrl string = mainContainerApp.properties.latestRevisionFqdn
