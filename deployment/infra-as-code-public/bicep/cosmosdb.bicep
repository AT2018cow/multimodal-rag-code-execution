
@description('This is the base name for each Azure resource name (6-12 chars)')
param uniqueid string

param namePrefix string ='dev'

@description('The resource group location')
param location string = resourceGroup().location

// variables
// var storageName = 'st${uniqueid}'
var varcosmosdbName = '${namePrefix}-cosmosdb-research${uniqueid}'
// var storageSkuName = 'Premium_LRS'



resource cosmosdb 'Microsoft.DocumentDB/databaseAccounts@2024-02-15-preview' = {
  name: varcosmosdbName
  location: location
  kind: 'GlobalDocumentDB'
  tags: {
    defaultExperience: 'Core (SQL)'
    'hidden-cosmos-mmspecial': ''
  }  
  properties: {
    publicNetworkAccess: 'Enabled'
    enableAutomaticFailover: false
    enableMultipleWriteLocations: false    
    isVirtualNetworkFilterEnabled: false
    virtualNetworkRules: []
    // EnabledApiTypes: 'Sql'
    disableKeyBasedMetadataWriteAccess: false
    enableFreeTier: false
    enableAnalyticalStorage: false
    analyticalStorageConfiguration: {
      schemaType: 'WellDefined'
    }
    // instanceId: 'ca7f27b6-ec47-461d-bb99-5d24a08999da'
    databaseAccountOfferType: 'Standard'
    enableMaterializedViews: false
    defaultIdentity: 'FirstPartyIdentity'
    networkAclBypass: 'None'
    disableLocalAuth: false
    enablePartitionMerge: false
    enablePerRegionPerPartitionAutoscale: false
    enableBurstCapacity: false
    enablePriorityBasedExecution: false
    // defaultPriorityLevel: 'High'    
    minimalTlsVersion: 'Tls12'
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
      maxIntervalInSeconds: 5
      maxStalenessPrefix: 100
    }
    
    locations: [
      {
        // was hardcoded 'Sweden Central' (upstream bug): every Cosmos read/write crossed the Atlantic
        locationName: toLower(location)
        failoverPriority: 0
        isZoneRedundant: false
      }
    ]
    cors: []
    // Serverless removed: per-request billing drops to $0 when idle, which breaks
    // the daily minimum-spend requirement. Provisioned shared throughput below.
    capabilities: []
    ipRules: []
    backupPolicy: {
      type: 'Periodic'
      periodicModeProperties: {
        backupIntervalInMinutes: 240
        backupRetentionIntervalInHours: 8
        backupStorageRedundancy: 'Geo'
      }
    }
    networkAclBypassResourceIds: []
    diagnosticLogSettings: {
      enableFullTextQuery: 'None'
    }
  }
  identity: {
    type: 'None'
  }
}

// SQL database with shared provisioned throughput (800 RU/s ≈ $1.5/day).
// The app (cosmos_helpers.py) creates containers inside this database without
// specifying throughput, so they share the database-level 800 RU/s.
// Database name must match the COSMOS_DB_NAME app setting, which both aca.bicep
// and webapp.bicep set to the cosmosdb account name (varcosmosdbName).
resource cosmosdbSqlDatabase 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-02-15-preview' = {
  name: varcosmosdbName
  parent: cosmosdb
  properties: {
    resource: {
      id: varcosmosdbName
    }
    options: {
      throughput: 800
    }
  }
}

output cosmosdbName string = cosmosdb.name
output cosmosDbUri string = cosmosdb.properties.documentEndpoint
#disable-next-line outputs-should-not-contain-secrets
output cosmosDbKey string = cosmosdb.listKeys().primaryMasterKey
