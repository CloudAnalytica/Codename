import json_to_node_handler
import node
import pymysql
import aurora_insertion_handler

def lambda_handler(event, context):
    #Specify the bucket name you want to grab the JSON from 
    bucketName = 'b3itzohai'
    
    #Parses the relevant information from the newest JSON file in the bucket specified above
    #returns a list of node objects that represent each instance in the log file
    nodeList = json_to_node_handler.parseJSONfile(bucketName)
    
    #Sends the node handler and the DB information to have the aurora_insertion_handler deal with inserting the info
    hostName = ''
    port = 3306
    user = ''
    passwd = ''
    dbName = ''
    aurora_insertion_handler.connectToAuroraDB(hostName, port, user, passwd, dbName, nodeList)
 
    return('Complete')