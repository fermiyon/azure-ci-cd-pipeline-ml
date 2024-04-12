![Static Badge](https://img.shields.io/badge/python-3.9-blue)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/t/fermiyon/azure-ci-cd-pipeline-ml/build-deploy)

[![CI](https://github.com/fermiyon/azure-ci-cd-pipeline-ml/actions/workflows/pythonapp.yml/badge.svg?branch=main)](https://github.com/fermiyon/azure-ci-cd-pipeline-ml/actions/workflows/pythonapp.yml)
[![Build Status](https://dev.azure.com/odluser257419/flask-ml/_apis/build/status%2Ffermiyon.azure-ci-cd-pipeline-ml?branchName=build-deploy)](https://dev.azure.com/odluser257419/flask-ml/_build/latest?definitionId=1&branchName=build-deploy)

By Selman Karaosmanoglu 

## Date created
11 April 2024

# Azure Machine Learning Operations Project: Deploy a Flask-based ML Application with Integrated CI/CD Pipelines

# Overview

Deploy a Flask-based machine learning application on Azure, with the CI/CD pipelines for streamlined updates and maintenance

## Project Plan
* [Trello board for the project](https://trello.com/b/komPo9UB/project)
* [Spreadsheet for the project plan](https://docs.google.com/spreadsheets/d/1HoSYQIiP7T31eLKW6cnpgNWpM_oNzrgT/edit#gid=744226840)

## Prerequisites
* [an Azure account](https://portal.azure.com)
* [a GitHub account](https://www.github.com)

## Instructions

**Architectural Diagram**
![screenshot](screenshots/diagram.png)


### 1. Run project locally
#### 1.1 Clone (or first fork then clone) the repository and checkout build-deploy-branch

```bash
https://github.com/fermiyon/azure-ci-cd-pipeline-ml.git

git checkout build-deploy
```

You can also fork the repository and clone the forked repository.
#### 1.2 Make sure that you are running python 3.9 in the local

```bash
python --version
```

#### 1.3 Create virtual environment inside the project folder

```bash
python -m venv venv
```

#### 1.4 Activate virtual environment

```bash
source venv/bin/activate
```

(For Windows with Gitbash, replace bin with Scripts in the command)

```bash
source venv/Scripts/activate
```

#### 1.5 Run Makefile
The `make all` command installs the necessary Python packages, performs linting on app.py and runs tests.

```bash
make all 
```

![screenshot](screenshots/2-local-makefile-all-passed.png)

#### 1.6 Run App

```bash
flask run
```

![screenshot](screenshots/1-local-flask-run.png)

#### 1.7 Test in the local

```bash
./make_prediction.sh
```

You should see the following output: 
![screenshot](screenshots/2-local-test.png)

### 2. Information on GitHub actions

GitHub Actions is a tool by GitHub that enables continuous integration and deployment right within a GitHub repository. It can be triggered by various events like push or pull requests. It’s used for tasks like building, testing, and deploying code.

In the project folder, a workflow was already created under ./github/workflows named pythonapp.yml. However if you want to create one, you can follow the following steps.

#### 2.1 Create a GitHub Actions workflow
Click on the actions tab. If you have prior workflows, you can see the workflows there. Now you can create a new workflow.

![screenshot](screenshots/github-actions-new.png)

Set up a workflow yourself.

![screenshot](screenshots/github-actions-new-2.png)

Create a workflow that checks out the code, sets up Python, installs dependencies, lints the code, and runs tests whenever there’s a push or a pull request to the main or build-deploy branches. It’s a standard continuous integration(CI) setup for a Python project. The following yaml file does that.

```yaml
name: CI

on:
  push:
    branches: [ "main", "build-deploy" ]
  pull_request:
    branches: [ "main", "build-deploy" ]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Python
      uses: actions/setup-python@v5.1.0
      with:
        python-version: "3.10"

    - name: Install dependencies
      run: make install

    - name: Run lint
      run: make lint
      
    - name: Run tests
      run: make test
      
      
```
![screenshot](screenshots/github-actions-new-3.png)

Once you have created a workflow, each time you push a commit, an event is triggered that executes the workflow above.

### 3. Create Azure App Service
The following section show how to manually deploy our flask application using Azure App Service and test it via Azure Cloud Shell.
#### 3.1 Open Azure Cloud Shell (or Azure CLI)

Go to https://portal.azure.com and open Azure Cloud Shell.

![screenshot](screenshots/azure-cloud-shell.png)

#### 3.2 Create SSH keygen on Azure Cloud Shell
Create ssh keys

```bash
ssh-keygen -t rsa
```

Look ssh key and copy the key.

```bash
cat .ssh/id_rsa.pub
```

![screenshot](screenshots/azure-ssh-key.png)

#### 3.3 Add the Azure SSH key to GitHub SSH keys
Go to https://github.com/settings/keys and add new SSH key. Paste the SSH key that we copied earlier.

![screenshot](screenshots/git-ssh-key.png)

#### 3.4 Clone the git repo on Azure using the cloud shell
```bash
git clone git@github.com:fermiyon/azure-ci-cd-pipeline-ml.git 
```
![screenshot](screenshots/azure-cli-git-clone.png)
#### 3.5 Create virtual environment of python3.9
```bash
python3.9 -m venv venv
```
![screenshot](screenshots/azure-create-venv.png)

#### 3.6 Activate virtual environment
```bash
source venv/bin/activate
```
![screenshot](screenshots/azure-source-activate.png)
#### 3.7 Checkout to build-deploy branch
```bash
cd azure-ci-cd-pipeline-ml
git checkout build-deploy
```
![screenshot](screenshots/azure-git-checkout.png)
#### 3.8 Run Makefile

```bash
make all
```
![screenshot](screenshots/azure-make-all-1.png)
![screenshot](screenshots/azure-make-all-2.png)

#### 3.9 Create Azure App Service
(This may take up to 10 min.)

Run the following command to create and deploy a web app on Azure.

```bash
az webapp up --resource-group Azuredevops --sku B1 --logs --runtime "PYTHON:3.9" -n your_app_name
```
![screenshot](screenshots/azure-webapp.png)

You can now see the log stream

![screenshot](screenshots/azure-webapp-2.png)

You can also see the log stream via the command below

```bash
az webapp log tail --resource-group Azuredevops --name your_app_name
```

![screenshot](screenshots/azure-webapp-log.png)

#### 3.10 Check Azure App Service
Check the url generated by Azure Web App after successful deployment. Write your own app name instead of your_app_name 

https://your_app_name.azurewebsites.net/

![screenshot](screenshots/azure-websites.png)

#### 3.11 Output of a Test Run on Azure
Open a new Azure cloud shell or close the log stream with `ctrl+c`

Change the current directory to the repository folder. Give execute permissions to the `make_predict_azure_app.sh` file and execute it using the commands below.

Note: Make sure you have the same app name in the the `make_predict_azure_app.sh` file as the name of your web app name we gave it earlier, otherwise it will give error.

![screenshot](screenshots/azure-sh-settings.png)

```bash
cd azure-ci-cd-pipeline-ml/
chmod +x make_predict_azure_app.sh
./make_predict_azure_app.sh
```
![screenshot](screenshots/azure-prediction.png)

### 4. Azure DevOps
Go to dev.azure.com
#### 4.1 Change Azure organization settings policies to allow public projects
![screenshot](screenshots/azure-devops-settings-1.png)

![screenshot](screenshots/azure-devops-settings-2.png)

#### 4.2 Create new Azure DevOps Project
![screenshot](screenshots/azure-devops-create-project.png)

#### 4.3 Create new service connection
Create new service connection under project settings

![screenshot](screenshots/azure-devops-project-settings.png)

![screenshot](screenshots/azure-devops-project-settings-sc.png)

![screenshot](screenshots/azure-devops-project-settings-sc-new.png)

![screenshot](screenshots/azure-devops-project-settings-sc-new-sp.png)

![screenshot](screenshots/azure-devops-project-settings-sc-new-sp-2.png)

#### 4.4 Create new token
Create the token and save it somewhere secure to be used later.

![screenshot](screenshots/azure-devops-token.png)

![screenshot](screenshots/azure-devops-token-create.png)

![screenshot](screenshots/azure-devops-token-create-2.png)

#### 4.5 Add agent pool
Under project settings, add agent pool.

![screenshot](screenshots/azure-devops-project-settings.png)

![screenshot](screenshots/azure-devops-agent-pool.png)

### 5. Create self-hosted agent VM
#### 5.1 Create the VM
Creating the VM via Azure Web Interface

![screenshot](screenshots/azure-create-vm-1.png)

![screenshot](screenshots/azure-create-vm-2.png)

Alternatively you can create via Azure CLI (Do not forget to change the admin password in the command below)

```bash
az vm create --resource-group Azuredevops --name appVM --admin-username devopsagent --admin-password your_password --image Ubuntu2204 --size Standard_DS1_v2 --generate-ssh-keys
```

#### 5.2 Configure the self-hosted agent VM
Connect to the VM via Azure Cloud Shell
```bash
ssh devopsagent@PUBLIC_IP_ADDRESS
```
![screenshot](screenshots/devopsagent-ssh.png)

#### 5.3 Open the instructions of the Agent
In another tab, open project settings -> Agent Pools

![screenshot](screenshots/azure-devops-project-settings.png)

Select the pool we created earlier.

![screenshot](screenshots/devopsagent-agent-pool.png)

Add agent -> linux

![screenshot](screenshots/devopsagent-instructions.png)

Get set-up file URL to be used in curl command

![screenshot](screenshots/devopsagent-url.png)

#### 5.4 Configure the self-hosted agent VM
After a succesfull connection to the VM, configure the VM as a self hosted agent with the following commands.

```bash
sudo snap install docker
sudo groupadd docker
sudo usermod -aG docker $USER
```

Download the linux agent (URL is the URL we copied earlier.) 

```bash
curl -O https://vstsagentpackage.azureedge.net/agent/3.236.1/vsts-agent-linux-x64-3.236.1.tar.gz
```

```bash
mkdir myagent && cd myagent
tar zxvf ~/vsts-agent-linux-x64-3.236.1.tar.gz
```

Run config.sh with following information

Server url is: https://dev.azure.com/your_organization

Agent pool is: the pool name you created before. For example: flask_agent_pool

```bash
./config.sh
```

![screenshot](screenshots/devopsagent-config-sh.png)

Install specific packages on the self-hosted agent VM if necessary (zip etc.)

Run svc

```bash
sudo ./svc.sh install
sudo ./svc.sh start
```

![screenshot](screenshots/devopsagent-svc.png)

Prepare the agent
```bash
sudo apt-get update
sudo apt update
sudo apt-get install build-essential
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
```
Install python 

```bash
sudo apt install python3.9
sudo apt-get install python3.9-venv
sudo apt-get install python3-pip
```

Control python version

```bash
python3.9 --version
```
![screenshot](screenshots/devopsagent-python-version.png)

Install tools for pipeline build steps
```bash
sudo apt-get install python3.9-distutils
sudo apt-get -y install zip
pip install pylint
export PATH=$HOME/.local/bin:$PATH
python3.9 -m venv venv
```
After these steps you can see agent VM in projects agent pool.

![screenshot](screenshots/devopsagent-pool-agent.png)

### 6. Create pipelines on Azure DevOps
#### 6.1 Creating new pipeline
In Azure Devops, in the project, go to Pipelines section and click the new pipeline button. 

![screenshot](screenshots/devops-new-pipeline.png)

Select GitHub

![screenshot](screenshots/devops-new-pipeline-2.png)

You may need to re-enter your GitHub password for confirmation, and if the Azure Pipelines extension is not installed, GitHub will prompt you to install it.

Select the repository.

![screenshot](screenshots/devops-new-pipeline-3.png)

For configuration, select existing yaml file since we have yaml file in our repository. If you don't have yaml file, you can select a starter template.

 If it directly goes to the review pipeline page, edit the pipeline, select build-deploy branch yaml file and click run.- If you encounter env could not find error, edit the pipeline, go to the build-deploy branch and click run.

![screenshot](screenshots/devops-new-pipeline-4.png)

Select build-deploy branch and azure-pipelines.yml file. 

![screenshot](screenshots/devops-new-pipeline-5.png)


In the reviewing pipeline window shown below, update the `pool` name, the name of `azureServiceConnectionId` and `webAppName` that we created earlier.

![screenshot](screenshots/devops-new-pipeline-6.png)

This YAML file is a configuration for a continuous integration and continuous deployment (CI/CD) pipeline in Azure DevOps. It has two stages namely build and deploy.

**Build Stage**: This stage includes a job that runs several tasks:
- Checking Python versions.
- Creating a virtual environment and installing dependencies.
- Running lint tests.
- Archiving the project files into a zip file.
- Uploading the zip file as an artifact.

**Deploy Stage**: This stage depends on the successful completion of the Build stage. 
- It deploys the web app to Azure using the uploaded artifact.

For more information, please check [official Azure Pipeline documentation](https://docs.microsoft.com/en-us/azure/devops/pipelines/ecosystems/python-webapp?view=azure-devops#yaml-pipeline-explained)

```yaml
# Starter pipeline    
# Start with a minimal pipeline that you can customize to build and deploy your code.
# Add steps that build, run tests, deploy, and more:
# https://aka.ms/yaml
trigger:
- main
- build-deploy

# TODO: Replace the agent pool name
pool: flask_agent_pool

variables:
  # TODO: Replace the service connection name as used in the DevOps project settings
  azureServiceConnectionId: 'flask_sc'
  
  # TODO: Specify the value of the existing Web App name
  webAppName: 'flask145'

  # Environment name
  environmentName: 'venv'

  # Project root folder. Point to the folder containing manage.py file.
  projectRoot: $(System.DefaultWorkingDirectory)

stages:
- stage: Build
  displayName: Build stage
  jobs:
  - job: BuildJob
    pool: flask_agent_pool
    steps:       
    - script: |
        python3 --version
        python3.9 --version
      displayName: 'Run a multi-line script'
      
    - script: |
        python3.9 -m venv venv
        source venv/bin/activate
        python --version
        make install
      workingDirectory: $(projectRoot)
      displayName: 'myStep 1'

    - script: |
        source venv/bin/activate
        python --version
        make lint
      workingDirectory: $(projectRoot)
      displayName:  'myStep 2 - Run lint tests'

    - task: ArchiveFiles@2
      displayName: 'myStep 3 - Archive files'
      inputs:
        rootFolderOrFile: '$(projectRoot)'
        includeRootFolder: false
        archiveType: zip
        archiveFile: $(Build.ArtifactStagingDirectory)/$(Build.BuildId).zip
        replaceExistingArchive: true

    - upload: $(Build.ArtifactStagingDirectory)/$(Build.BuildId).zip
      displayName: 'myStep 5 - Upload package'
      artifact: drop
- stage: Deploy
  displayName: 'Deploy Web App'
  dependsOn: Build
  condition: succeeded()
  jobs:
  - deployment: DeploymentJob
    pool: flask_agent_pool
    environment: $(environmentName)
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureWebApp@1
            displayName: 'Deploy Azure Web App : '
            inputs:
              azureSubscription: $(azureServiceConnectionId)
              appName: $(webAppName)
              appType: webAppLinux
              package: $(Pipeline.Workspace)/drop/$(Build.BuildId).zip
```


Note: If the deployment job is paused, it is because it needs permission. You can click on the deployment job and give permission.

![screenshot](screenshots/devops-pipeline-permit.png)

After a successful pipeline run, you can see the result as shown below. 

Pipeline has two jobs as you can see. One is the build job and the following is the deployment job.

![screenshot](screenshots/devops-pipeline-completed.png)

#### 6.2 Check the deployment

After all these steps above, our service is finally deployed. You can check the application URL that we set up earlier: https://your_app_name.azurewebsites.net

![screenshot](screenshots/deployment-succeded.png)

#### 6.3 Test run of the pipeline
Make a change in app.py and push that change to the repository.

![screenshot](screenshots/pipeline-git-push.png)

```bash
git add .
git commit -m "Update h3 text in home function"
git push origin build-deploy
```
After a successful commit, first, GitHub actions workflow run automatically, you can check it from the GitHub repository page shown below

![screenshot](screenshots/pipeline-run-1.png)

Go to the Azure DevOps Pipeline page. You will see that our pipeline is running. It can take up to 15 minutes to build and deploy.

![screenshot](screenshots/pipeline-run-2.png)

![screenshot](screenshots/pipeline-run-3.png)

![screenshot](screenshots/pipeline-run-4.png)

![screenshot](screenshots/pipeline-run-5.png)

Check the webpage after succesful deployment.

![screenshot](screenshots/pipeline-run-deployment.png)


#### 6.4 Output of test run after the deployment
Open Azure Cloud Shell and test the prediction.

```bash
./make_predict_azure_app.sh
```
![screenshot](screenshots/pipeline-run-test-predict.png)

#### 6.5 Output of streamed log files from the deployed application

Run the following command in the Azure Cloud Shell to view the streamed log files

```bash
az webapp log tail --resource-group Azuredevops --name your_app_name
```

![screenshot](screenshots/pipeline-run-log.png)

### 7. Load test
Running load test with locust.

`locustfile.py` is a script for load testing a web application using Locust, an open-source load testing tool. It defines the behaviour of a simulated user on the website. It has two tasks. One is index that simulates opening the home page of the site. The other is predict that simulates a post request to the /predict endpoint of the website sending the json with a data.

#### 7.1 Locust with web interface
You can run this command on your local repository to use the Locust web interface.

```bash
locust -f locustfile.py -H https://your_app_name.azurewebsites.net
```
![screenshot](screenshots/locust-web-run.png)

After running the command, you can open the Locust’s web interface at http://localhost:8089.

![screenshot](screenshots/6-locust-load-test.png)

![screenshot](screenshots/locust-test.gif)

#### 7.2 Locust with the shell

Alternatively you can run Locust without web interface on the Azure Cloud Shell 

```
locust -f locustfile.py --headless -u 10 -r 5 --run-time 30 --host https://your_app_name.azurewebsites.net
```
![screenshot](screenshots/azure-locust.png)

![screenshot](screenshots/azure-locust-2.png)

## Requirements

Language: Python 3.9

Libraries: pandas, flask, scikit-learn, joblib, locust, pylint, pytest, werkzeug (see requirements.txt)

## Enhancements
- The Kubernetes version of the project can be made.
- Azure Pipelines Continous Delivery step can be replaced with GitHub Actions.
- Increase test coverage.


## Demo 
[![Video](https://img.youtube.com/vi/3POgYC7_rk4/0.jpg)](https://www.youtube.com/watch?v=3POgYC7_rk4)



## Credits
Udacity Data Engineer Nanodegree Program
