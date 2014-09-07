global hostName
global userName
global password
global dbName
global connectionString

hostName = "localhost"
userName = "root"
password = "afroninja#123" #VITAL TO CHANGE THIS VALUE TO SOMETHING DIFFERENT BEFORE DEPLOYMENT
dbName = "rcprep"

connectionString = "mysql://" + userName + ":" + password + "@" + hostName + "/" + dbName
