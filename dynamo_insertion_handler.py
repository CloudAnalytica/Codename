'''
        Title:          DynamoDBFunctions.py
        Author:         Daniel Ng
        Purpose:        Various functions to manipulate DynamoDB
        
        Future:         Probably need to add Put, Delete, and get functions
'''
import boto3
import datetime


'''
        Purpose: Creates a DyanmoDB table.
        Specify the tableName and keyName.
        
        Future add ons:
            * We can add more intricate specifications later 
              on if needed.
'''
def createDynamoDBTable(tableName, keyName):
        dynamodb = boto3.resource('dynamodb')

        print('ATTEMPTING TO CREATE DYNAMODB TABLE:', tableName)

        # Create the DynamoDB table.
        table = dynamodb.create_table(
            TableName=tableName,
            KeySchema=[
                {
                    'AttributeName': keyName,
                    'KeyType': 'HASH' #Hash key
                },
                {
                    "AttributeName": "timestamp",
                    "KeyType": "RANGE"
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': keyName,
                    'AttributeType': 'S'
                },
                {
                "AttributeName": "timestamp",
                "AttributeType": "S"
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName=tableName)

        # Print out some data about the table.
        print(table.item_count)
        
        
        
'''
        Purpose: Puts an item onto a table
        Specify which table you want to put your item into.
        It will overwrite items with the same key.
        
'''
def putItem(tableName, item):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tableName)
    print('PUTTING ITEM INTO DYNAMODB TABLE:\t%s' %(table.name))
    table.put_item(Item = item)
    print('PUT EXECUTED')
    
    
'''    
creates an instance of node item
'''
def createItem(node):
    nodeInfo = node.getNodeDictionary()
    networkInfo = node.getNetworkDictionary()
    cpuInfo = node.getCPUList()
    fsInfo = node.getFileSystemList()
    date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    item = {
        'timestamp':        date,
        # Nodes
        'nodeName':         nodeInfo['nodeName'],
        'chefEnv':          nodeInfo['chefEnv'],
        'cloudEnv':         nodeInfo['cloudEnv'],
        'dateCreated':      nodeInfo['dateCreated'],
        'platform':         nodeInfo['platform'],
        'platformVersion':  nodeInfo['platformVersion'],
        'platformFamily':   nodeInfo['platformFamily'],
        'upTime':           nodeInfo['upTime'],
        # Interface
        'interface':        networkInfo['interface'],
        'privateIP': networkInfo['privateIP'],
        'publicIP':  networkInfo['publicIP'],
        'netMask':          networkInfo['netMask'],
        'state':            networkInfo['state'],
        'localHostname':    networkInfo['localHostname'],
        'publicHostname':   networkInfo['publicHostname'],
        'defaultGateway':   networkInfo['defaultGateway'],
        # CPU, structure subject to change
        'cores':            cpuInfo[0]['cores'],
        'vendor':          cpuInfo[0]['vendor'],
        'speed':            cpuInfo[0]['speed'],
        'model':            cpuInfo[0]['model'],
        # Filesystem, structure subject to change
        'device':           fsInfo[0]['device'],
        'mountPoint':       fsInfo[0]['mountPoint'],
        'size':             fsInfo[0]['size'],
        'used':             fsInfo[0]['used'],
        'available':        fsInfo[0]['available'],
        'percentUsed':      fsInfo[0]['percentUsed'],
    }
    print('CREATING ITEM: \n', item)
    return item