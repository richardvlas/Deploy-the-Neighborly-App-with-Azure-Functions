# Deploy the Neighborly App with Azure Functions

## Project Overview
In this project, I am going to build an app called "Neighborly". Neighborly is a Python Flask-powered web application that allows neighbors to post advertisements for services and products they can offer.

The Neighborly project is comprised of a front-end application that is built with the Python Flask micro framework. The application allows the user to view, create, edit, and delete the community advertisements.

The application makes direct requests to the back-end API endpoints. These are endpoints that we will also build for the server-side of the application.

You can see an example of the deployed app below.

![final app](images/final-app.png)

## Dependencies
You will need to install the following locally:

* [Pipenv](https://pypi.org/project/pipenv/)
* [Visual Studio Code](https://code.visualstudio.com/download)
* [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
* [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
* [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

On Mac, you can do this with:

```bash
# install pipenv
brew install pipenv

# install azure-cli
brew update && brew install azure-cli

# install azure function core tools 
brew tap azure/functions
brew install azure-functions-core-tools@3
```

## Project Instructions
In case you need to return to the project later on, it is suggested to store any commands you use so you can re-create your work.

I have written all commands to create Azure resources (as described in the next section) into a bash file that you can run from the root of the project as follows:

```bash
source azure_resources.sh
```

### I. Creating Azure Function App

We need to set up the Azure resource group, region, storage account, and an app name before we can publish.

1. Create a resource group, and use this resource group to create the following resources.

2. Create a storage account (within the previously created resource group and region).

3. Create an Azure Function App within the resource group, region and storage account.
   * Note that app names need to be unique across all of Azure.
   * Make sure it is a Linux app, with a Python runtime.

4. Create a CosmosDB account for MongoDB API.

5. Create a MongoDB database in CosmosDB account and two collections:
   1. `advertisements`
   2. `posts`
  
   Note that we will use `_id` field for indexing.
  
6. Get the cosmosDB connection string and preserve it somewhere in your local. Also, save the value of the CosmosDB's connection string in the Function App's >> Application settings variables. This step will connect the two services.

7. Import Sample Data into MongoDB collection.
    * Install [MongoDB Community Edition](https://docs.mongodb.com/manual/administration/install-community/) CLI tool in your local. For example, MacOS users may use:
      
      ```bash
      # get the mongodb library
      brew tap mongodb/brew
      brew install mongodb-community@5.0
      # check if mongoimport lib exists
      mongoimport --version
      ```
      
    * Import the data from the `./sample_data/` directory for Ads and Posts to initially populate your database. Note that both JSON files - `sampleAds.json` and `samplePosts.json` have multiple documents contained in a single JSON file. Each document has its own `_id` field as an identifier.
    
      ```bash
      # Import data into `advertisements` collection
      mongoimport --uri $cosmosdbConnectionString --db $mongoDBDatabaseName --collection $adsCollectionName --file='./sample_data/sampleAds.json' --jsonArray
      ```
      
      Repeat the same command for the `posts` collection.
      
8. **Update your Functions** 
  
    Hook up your connection string into the NeighborlyAPI server folder. You will need to replace the `url` variable with your own connection string you copy-and-pasted in the last step, along with some additional information.
    
    * Tip: Check [out this post](https://docs.microsoft.com/azure/cosmos-db/connect-mongodb-account?WT.mc_id=udacity_learn-wwl) if you need help with what information is needed.
    * Go to each of the `__init__.py` files in getPosts, getPost, getAdvertisements, getAdvertisement, deleteAdvertisement, updateAdvertisement, createAdvertisements and replace your connection string. You will also need to set the related `database` and `collection` appropriately. See an example below:
        
        ```python
        # inside getAdvertisements/__init__.py

        def main(req: func.HttpRequest) -> func.HttpResponse:
            logging.info('Python getAdvertisements trigger function processed a request.')

            try:
                # copy/paste your primary connection url here
                #-------------------------------------------
                url = "Your connection string" 
                #--------------------------------------------

                client=pymongo.MongoClient(url)

                database = client['Your MongoDB database name'] # Feed the correct key for the database name to the client
                collection = database['Collection name'] # Feed the correct key for the collection name to the database

                ... [other code omitted]
        ```
        
        Make sure to do the same step for the other 6 HTTP Trigger functions.

9. **Deploy your Functions**
  
    1. Test it out locally first. You may have to create a local environment and install all `requirements.txt` dependencies before you run the functions:

        ```bash
        # cd into NeighborlyAPI
        cd NeighborlyAPI

        # install dependencies
        pipenv install

        # go into the shell
        pipenv shell

        # test func locally
        func start
        ```
    
        You may need to change `"IsEncrypted"` to `false` in `local.settings.json` if this fails.

        At this point, Azure functions are hosted in `localhost:7071`. You can use the browser or Postman to see if the `GET` request works. For example, go to the browser and type in:

        ```bash
        # example endpoint for all advertisements
        http://localhost:7071/api/getadvertisements

        #example endpoint for all posts
        http://localhost:7071/api/getposts
        ```
    
    2. Now you can deploy functions to Azure by publishing your function app.
        
        ```bash
        # cd into NeighborlyAPI
        cd NeighborlyAPI

        # install dependencies
        pipenv install

        # go into the shell
        pipenv shell

        # deploy Azure Functions
        func azure functionapp publish funcapp1379128
        ```
       
       The result may give you a live url in this format, or you can check in Azure portal for these as well:
       
       Expected output if deployed successfully:
       
       ```bash
       Functions in <APP_NAME>:
          createAdvertisement - [httpTrigger]
              Invoke url: https://<APP_NAME>.azurewebsites.net/api/createadvertisement

          deleteAdvertisement - [httpTrigger]
              Invoke url: https://<APP_NAME>.azurewebsites.net/api/deleteadvertisement

          getAdvertisement - [httpTrigger]
              Invoke url: https://<APP_NAME>.azurewebsites.net/api/getadvertisement

          getAdvertisements - [httpTrigger]
              Invoke url: https://<APP_NAME>.azurewebsites.net/api/getadvertisements

          getPost - [httpTrigger]
              Invoke url: https://<APP_NAME>.azurewebsites.net/api/getpost

          getPosts - [httpTrigger]
              Invoke url: https://<APP_NAME>.azurewebsites.net/api/getposts

          updateAdvertisement - [httpTrigger]
              Invoke url: https://<APP_NAME>.azurewebsites.net/api/updateadvertisement
       ```
       
       > **Note**: It may take a minute or two for the endpoints to get up and running if you visit the URLs.
       
       Save the function app url `https://<APP_NAME>.azurewebsites.net/api/` since you will need to update that in the client-side of the application.


        









