@description('A prefix that will be prepended to resource names')
param namePrefix string = 'dev'

@description('The name of the Vision resource')
param accountsVisionResTstName string = 'vision'

@description('A unique identifier that will be appended to resource names')
param uniqueid string

@description('The location in which all resources should be deployed.')
param location string

var varaccountsVisionResTstName = '${namePrefix}${accountsVisionResTstName}${uniqueid}'






resource cognitiveServicesAccount 'Microsoft.CognitiveServices/accounts@2023-10-01-preview' = {
  name: varaccountsVisionResTstName
  location: location
  sku: {
    name: 'S1'
  }
  kind: 'ComputerVision'
  identity: {
    type: 'None'
  }
  properties: {
    customSubDomainName: varaccountsVisionResTstName
    restore: false
    networkAcls: {
      defaultAction: 'Allow'
      virtualNetworkRules: []
      ipRules: []
    }
    publicNetworkAccess: 'Enabled' // was 'Disabled' upstream with no private endpoint wired up, which broke all Vision calls from the app
  }
}

// output containerRegistryName string = containerRegistry_resource.name
output accountsVisionResTstName string = cognitiveServicesAccount.name
output accountsVisionEndpoint string = cognitiveServicesAccount.properties.endpoint
#disable-next-line outputs-should-not-contain-secrets
output accountsVisionKey string = cognitiveServicesAccount.listKeys().key1
