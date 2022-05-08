# Variables for Azure resources
uniqueId=1379128
resourceGroup="resourcegroup$uniqueId"
location="westeurope"
storageAccount="storageaccount$uniqueId"
functionApp="functionapp$uniqueId"
cosmosDBDatabaseAccount="cosmosdb$uniqueId"
serverVersion="4.0"
mongoDBDatabaseName="mongodb$uniqueId"
adsCollectionName="advertisements"
postsCollectionName="posts"

# Create a resource group
az group create -n $resourceGroup -l $location

# Create a storage account
az storage account create \
    --name $storageAccount \
    --resource-group $resourceGroup \
    --location $location \

# Create a function app
az functionapp create \
    --resource-group $resourceGroup \
    --name $functionApp \
    --storage-account $storageAccount \
    --consumption-plan-location $location \
    --os-type Linux \
    --runtime python \
    --runtime-version 3.8 \
    --functions-version 4

# Create a CosmosDB database account for MongoDB API
az cosmosdb create \
    --name $cosmosDBDatabaseAccount \
    --resource-group $resourceGroup \
    --kind MongoDB \
    --server-version $serverVersion \
    --default-consistency-level Eventual \
    --locations regionName=$location failoverPriority=0 isZoneRedundant=False \
    --enable-free-tier true

# Create a MongoDB API database in CosmosDB account
az cosmosdb mongodb database create \
    --account-name $cosmosDBDatabaseAccount \
    --resource-group $resourceGroup \
    --name $mongoDBDatabaseName

# Create a MongoDB API collection under an Azure Cosmos DB MongoDB database.
az cosmosdb mongodb collection create \
    --account-name $cosmosDBDatabaseAccount \
    --database-name $mongoDBDatabaseName \
    --name $adsCollectionName \
    --resource-group $resourceGroup

# Create a MongoDB API collection under an Azure Cosmos DB MongoDB database.
az cosmosdb mongodb collection create \
    --account-name $cosmosDBDatabaseAccount \
    --database-name $mongoDBDatabaseName \
    --name $postsCollectionName \
    --resource-group $resourceGroup

# Import the data from json files in the ./sample_data/ directory for Ads and Posts to initially populate your database
cosmosdbConnectionString=$(az cosmosdb keys list --name $cosmosDBDatabaseAccount --resource-group $resourceGroup --type connection-strings --query 'connectionStrings[0].connectionString' --output tsv)
mongoimport --uri $cosmosdbConnectionString --db $mongoDBDatabaseName --collection $adsCollectionName --file='./sample_data/sampleAds.json' --jsonArray
mongoimport --uri $cosmosdbConnectionString --db $mongoDBDatabaseName --collection $postsCollectionName --file='./sample_data/samplePosts.json' --jsonArray
