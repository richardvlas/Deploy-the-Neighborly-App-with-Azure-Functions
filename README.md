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



