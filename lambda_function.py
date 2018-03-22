import json_to_node_handler
import node
import pymysql
import mysql_insertion_handler

def lambda_handler(event, context):
    #Pulls the bucket and log file name from the event trigger 
    bucketName = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print('Log info pulled from : {} IN {}'.format(key, bucketName))
    
    #Parses the relevant information from the newest JSON file in the bucket specified above
    #returns a list of node objects that represent each instance in the log file
    nodeList = json_to_node_handler.parseJSONfile(bucketName, key)
    
    #Sends the node handler and the DB information to have the aurora_insertion_handler deal with inserting the info
    hostName = ''
    port = 3306
    user = ''
    passwd = ''
    dbName = ''
    mysql_insertion_handler.connectToAuroraDB(hostName, port, user, passwd, dbName, nodeList)
 
    return('Complete')