# TwitAPItoSQL
Obtains tweet data from Twitter API and populates table in SQL database hosted in Azure.

# Steps

### Set up development environment
Download required software: Python and Visual Studio Code (VSC).

Set up a Virtual Environment (VE) in VSC using:
```
python -m venv envName
```

Point Python interpreter to your VE (the interpreter automatically points to the Global Environment) by adding the file path to Python in your VE folder with *python.defaultInterpreterPath* in the settings.JSON file. To open settings.JSON file in VSC,	open Command Palette and search + click ‘Preferences: Open workspace settings’, and then click the top right icon ('Open Settings (JSON)’).

Automatically activate the VE when opening the Python terminal by changing *python.terminal.activateEnvironment* to true within the settings.JSON file. Make sure your developer settings on your local device are set to permit the running of PowerShell scripts without signing.

Having done this, your settings.JSON file should now contain the following code:

```
{
"python.defaultInterpreterPath": "C:\\filePathToVirtualEnvironment\\virtual_environment\\Scripts\\python"
, "python.terminal.activateEnvironment": true 
}
```


Download required Python modules using pip install. Here, you will need the following modules: requests (to make API request), os (for access tokens), pandas (for data frame creation), json (for managing JSON output from GET request), base64 (for key generation), pyodbc (to connect to SQL), numpy (for list manipulation), and time (for delaying GET requests).

### Create Twitter app
Apply for Developer Access on twitter, create an App in the developer’s portal and note down the API Key, API Secret, Bearer Token, and App ID. This information will be used to send a GET request to Twitter in Python.

### Create Azure SQL database
In Azure portal, create a server and a database. Make sure to add your IP address to the server in the server’s firewall setting. Note down the server’s name, you will need this to connect to Azure SQL database (db) from your device. 

### Create and populate SQL table from Python
See apiSQL.py file for Python code that makes GET request and uses the JSON output to populate an SQL table with tweet data.

### Query table
Open Microsoft SQL Server Management Studio (SSMS) on your local device and connect to your Azure db. To connect to Azure SQL db from your local device in SSMS, ensure that your firewall allows outgoing TCP communication on TCP port 1433.

In SSMS you can query your table. See some example SQL query code in the SQLquery file.
