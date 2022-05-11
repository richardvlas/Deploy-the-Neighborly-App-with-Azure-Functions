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
    
    2. Now you can deploy functions to Azure by publishing your function app. The command for deploying your function to Function App using CLI is:
        
        ```bash
        # cd into NeighborlyAPI
        cd NeighborlyAPI

        # install dependencies
        pipenv install

        # go into the shell
        pipenv shell

        # deploy Azure Functions
        func azure functionapp publish functionapp1379128
        ```
        
        If Azure cannot find your function, ensure that the current `local.settings.json` file contains all settings from the `Functions App` >> `Settings` >> `Configuration` in the portal.


       
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


### II. Deploying the client-side Flask web application

1. First we are going to update the Client-side `settings.py` with local API endpoints to test the front end with local functions. Navigate to the `settings.py` file in the `NeighborlyFrontEnd/` directory and uncomment the local `API_URL` variable:

    ```bash
    # Inside file settings.py

    # for production
    # API_URL = "https://<APP_NAME>.azurewebsites.net/api"


    # for local host if Azure functions served locally
    API_URL = "http://localhost:7071/api"
    ```

    Test the local functions through the locally deployed webapp by running:

    ```bash
    # cd into NeighborlyFrontEnd
    cd NeighborlyFrontEnd

    # install dependencies
    pipenv install

    # go into the shell
    pipenv shell

    # test the webapp locally
    python app.py   
    ```

2. We are going to update the Client-side `settings.py` with published API endpoints. Navigate to the settings.py file in the NeighborlyFrontEnd/ directory and specify the `API_URL` from Azure function app:
    
    ```bash
    # Inside file settings.py

    # for production
    API_URL = "https://functionapp1379128.azurewebsites.net/api"


    # for local host if Azure functions served locally
    # API_URL = "http://localhost:7071/api"
    ```
    
    Deploy your client-side application to the Azure Web App service. Name your web app different than the function app deployed in the previous step, or else you will erase your API.
    
    ```bash
    # if your virtual environment is deactivate, go again into the shell
    pipenv shell

    # export variable so the Azure stack knows which entry point to start your Flask app.
    export FLASK_RUN=app.py

    # deploy the webapp 
    az webapp up \
        --resource-group resourcegroup1379128 \
        --name neighborlywebapp \
        --sku F1 \
        --verbose
    ```

### III. CI/CD Deployment

1. **Create a Dockerfile**
    
    A [Dockerfile](https://docs.docker.com/engine/reference/builder/) is a text document that contains all the commands a user could call on the command line to assemble an image. Executing the following command will create a Dockerfile to an existing function project:
    
    ```bash
    func init --docker-only --python
    ```
    
    Ensure that the auto-generated Dcokerfile contains the `pip install -r requirements.txt` command.

2. **Build the image using the Dockerfile**

    This step is also called Containerising the App. It needs Docker installed on your local machine. Using the command, you will build and tag an image
    
    ```bash
    # SYNTAX 
    # docker build -t <name:tag> <path>
    docker build -t $imageName:$imageTag .
    
    # List all images
    docker images
    
    # Tag the image with the same name as the ACR respository else the push will fail.
    # SYNTAX 
    # docker tag <name:tag> <ACR-respository>.azurecr.io/<name:tag>
    docker tag $imageName:$imageTag $containerRegistry.azurecr.io/$imageName:$imageTag
    ```
    
    where,
      * `<name:tag>` is a name and optionally a tag in the 'name:tag' format and
      * `<path>` refers to the directory containing the Dockerfile.

    Once your image is ready on your local machine, you can test the application.
    
    ```bash
    docker run -p 7071:7071 -it $imageName:$imageTag
    ```
    
    `-p` maps the host's 7071 port to the container's 7071 port.
    
3. **Create Azure Container Registry Respository and Push the Image**
    
    After testing, you will want to push the image to a remote repository, Azure Container Registry, so that Azure Kubernetes service can download your image and run containers out of it.
    
    **Azure Container Registry** (ACR) is a managed, private Docker registry service. Think of it as a repository for all of your Docker images.

    Create a Azure Container Registry, and push your image.
    
    ```bash
    # Needs 'az login'
    # Create a repository in ACR service
    az acr create --resource-group $resourceGroup --name $containerRegistry --sku Basic
    az acr login --name $containerRegistry
    ```
    
    In the Azure portal, navigate to the `Container Registry service` >> `Settings` >> `Access Keys` and enable the `Admin user`.
    
    Login to your ACR registry from your local terminal:
    
    ```bash
    # Use the Admin user credentials (Username and Password) copied from Container Registry service >> Settings >> Access Keys in the portal
    docker login $containerRegistry.azurecr.io
    ```
    
    Push the image to Azure Container Registry.
    
    ```bash
    docker push $containerRegistry.azurecr.io/$imageName:$imageTag
    ```
    
    View the newly pushed image in the ACR respository
    
    ```bash
    az acr repository list --name $containerRegistry --output table
    ```
    
4. **Create a Kubernetes Cluster**
    
    You should have a $containerRegistry ready before creating a Kubernetes cluster using the command below:
    
    ```bash
    # Create an Azure Kubernetes cluster
    az aks create \
    --name $AKSCluster \
    --resource-group $resourceGroup \
    --node-count 2 \
    --generate-ssh-keys \
    --attach-acr $containerRegistry \
    --location $location
    ```
    
    This should return a JSON object with your AKS deployment information.
    
    Now, get your credentials for AKS
    
    ```bash
    # Get credentials for your container service and merge as current context in /Users/<username>/.kube/config
    az aks get-credentials \
    --name $AKSCluster \
    --resource-group $resourceGroup
    ```
    
    Verify the connection to your cluster and view the cluster nodes using:
    
    ```bash
    kubectl get nodes
    #Example output:
    #NAME                                STATUS   ROLES   AGE     VERSION
    #aks-nodepool1-38114521-vmss000000   Ready    agent   3m47s   v1.21.9
    #aks-nodepool1-38114521-vmss000001   Ready    agent   3m45s   v1.21.9
    ```
    
5. **Deploy the App to Kubernetes**
   
   Build the image and deploy the Function to Kubernetes:
   
   ```bash
   func kubernetes deploy --name $functionApp --registry $containerRegistry
   ```
   The deploy command will:
   * Use the Dockerfile to build a local image for the function app.
   * The local image will be tagged and pushed to the $containerRegistry
   * Create a deploy.yml manifest file and applied to the cluster that defines a Kubernetes Deployment resource.
   * Creates a Secrets file containing environment variables imported from your local.settings.json file.

   Check your deployment:
   
   ```bash
   kubectl config get-contexts
   ```
   
### IV. Event Hubs and Logic App
   
   1. **Create a Logic App** 
      
      With Azure Logic Apps and the SendGrid connector, you can automate tasks and workflows that send emails. In this section, you'll utilize SendGrid with the Logic App Designer that watches for an HTTP trigger. When the HTTP request is triggered, you send yourself an email notification.
      
      * [Create an integration workflow with Azure Logic Apps on Azure portal](https://docs.microsoft.com/en-us/azure/logic-apps/quickstart-create-first-logic-app-workflow)
      * [Create a request trigger in Logic app](https://docs.microsoft.com/en-us/azure/connectors/connectors-native-reqres)
   
      1. **SendGrid API Key Set Up**
          
          * Create a SendGrid Account [here](https://sendgrid.com/). You can use the free service, which is enough for our purposes.
          * Login and generate a SendGrid Key. Your API key is located [here](https://app.sendgrid.com/settings/api_keys). Create an API Key. This will be your key for integration with Azure Logic App, so save this key.

          * Now that you have created your key, make sure you also activate your Sender Authentication with the email. Go to the SendGrid navigation bar, scroll to the bottom and select `Settings` >> `Sender Authentication` list item. Select `Single Verification` option.
          
          * Create a new sender email in order to activate your SendGrid. This is because SendGrid would like you to be an actual person, and not a bot, to meet compliance regulations.
          
          * Go to your email Inbox and open the SendGrid email verification to complete the sender authentication process.

          Great! Now you have permissions you need to use SendGrid service with its API key for Logic App.


      2. **Create the Logic App Workflow**
          Next, you'll use the Logic App Designer with an http request trigger.
          * Login to the [Azure Portal](https://portal.azure.com/).
          * Go to Resources and create a `Logic App`, then select **Go to resource**
          * The designer's template page opens to show an introduction video and commonly used triggers.
          * Select `Blank Logic App` template.
          * After you select the template, the designer shows an empty workflow.
          * A workflow always starts with a single trigger, which specifies the condition to meet before running any actions in the workflow. Each time the trigger fires, Azure Logic Apps creates and runs a workflow instance. The request built-in trigger we are going to se creates a manually callable endpoint that can handle only inbound requests over HTTPS. When a caller sends a request to this endpoint, the Request trigger fires and runs the logic app
          * In the search box, enter `http request` as your filter. From the triggers list, select the `When an HTTP request is received` trigger.
          * Now, add another action as the next step in your workflow. Under the trigger, select Next step so that you can find the action that you want to add. In our case search for `sendgrid` and select `Send email(V4)` action.
          * Add a new connection using the API key from earlier and click `Create`.
          * Fill in the missing to/from and body fields for the email, such as `This is a HTTP trigger test`.
          * For the subject, write `test from logic app designer`, or whatever subject you would like. You could use a throwaway email or send it to your email account to test.
          * When you're done, save your logic app. On the designer toolbar, select Save. This step generates the URL to use for sending the request that triggers the logic app. To copy this URL, select the copy icon next to the URL.
          * To test your logic app, send an HTTP request to the generated URL. For example, you can use a tool such as [Postman](https://www.getpostman.com/) to send the HTTP request. 


   2. Create a namespace for event hub in the portal. You should be able to obtain the namespace URL.
      
      An Event Hubs namespace provides a unique scoping container, in which you create one or more event hubs. 
      
      [Create an event hub using Azure portal](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-create)
   
   3. Add the connection string of the event hub to the Azure Function.

      The connection string for a namespace has the following components embedded within it,

      - `FQDN` = the FQDN of the Event Hubs namespace you created (it includes the Event Hubs `namespace name` followed by `servicebus.windows.net`)
         
      - `SharedAccessKeyName` = the name you chose for your application's SAS keys
          
      - `SharedAccessKey` = the generated value of the key.
      
      The connection string for a namespace looks like:
      
      ```bash
      Endpoint=sb://<NamespaceName>.servicebus.windows.net/;SharedAccessKeyName=<KeyName>;SharedAccessKey=<KeyValue>
      ```
      
      The connection string for an event hub has an additional component in it. That's, `EntityPath=<EventHubName>`.

      ```bash
      Endpoint=sb://<NamespaceName>.servicebus.windows.net/;SharedAccessKeyName=<KeyName>;SharedAccessKey=<KeyValue>;EntityPath=<EventHubName>
      ```
      
      
      Add the connection string to the `local.settings.json` file under `EventHubConnectionString` key and reference it in the `function.json` file of `EventHubTrigger` function
      
      ```bash
      {
        "scriptFile": "__init__.py",
        "bindings": [
          {
            "type": "eventHubTrigger",
            "name": "event",
            "direction": "in",
            "eventHubName": "eventhubrvl",
            "connection": "EventHubConnectionString"
          }
        ]
      }
      ```

### V. Cleaning Up Your Services

Clean up and remove all services, or else you will incur charges.

```bash
az group delete --name $resourceGroup
```
   

   


    
    

    
    
    

    














