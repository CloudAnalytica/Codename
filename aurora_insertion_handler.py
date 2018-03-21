import node
import pymysql
from datetime import datetime, timezone

#The driving method for connecting to the database and ensures that changes
#are commited and the connection is always closed correctly, and to leave the
#database unchanged if an error occurs.
def connectToAuroraDB(hostName, portNum, userName, passWord, dbName, nodeList):
    try:
        #Establishes the connection to the database using the passed in connections
        conn = pymysql.connect(host = hostName, port = portNum, user = userName, passwd = passWord, db = dbName)
        
        #Goes through each node in the JSON file and inserts the information pulled into the DB
        for node in nodeList:
            nodeDict = node.getNodeDictionary()
            networkDict = node.getNetworkDictionary()
            fileSysList = node.getFileSystemList()
            cpuList = node.getCPUList()
            timestamp = str(datetime.now(timezone.utc))
            nodeName = nodeDict['nodeName']
        
            #inserts the node table info first to grab the nodeID and use it to build the rest of the strings
            insertNodeStr = constructNodeInsert(nodeDict, timestamp)
            nodeID = str(insertNodeTableToDB(insertNodeStr, conn))
        
            #Collects the sql strings to execut, and builds the first insert into line for the multi row entries
            insertNetworkStr = constructNetworkInsert(networkDict, nodeID)
            insertCPUStr = constructCPUInsert(node, cpuList, nodeID)
            insertFileSysStr = constructFileSysInsert(node, fileSysList, nodeID)
        
            #Inserts all of the remaining table information into the database
            insertRemainingNodeToDB(insertNetworkStr, insertCPUStr, insertFileSysStr, conn)
    
    except Exception as e:
        #Rollback any changes that were made before throwing the error
        conn.rollback()
        print('Database Connection was lost.')
        raise e
    finally:
        #Commits all of the changes made to the database and ensures connection is closed
        conn.commit()  
        conn.close()

#Builds the SQL string to insert all of the information to the nodes Table
def constructNodeInsert(nodeDict, timestamp):
    insertIntoNodeTable = ('INSERT INTO nodes (nodeName, chefEnv,cloudEnv, dateCreated, platform, ' 
            + 'platformVersion, platformFamily, upTime, logTime) VALUES (\'' 
            + nodeDict['nodeName'] + '\', \'' + nodeDict['chefEnv'] + '\', \'' 
            + nodeDict['cloudEnv'] + '\', \'' + nodeDict['dateCreated'] + '\', \'' 
            + nodeDict['platform'] + '\', ' + nodeDict['platformVersion'] + ', \'' 
            + nodeDict['platformFamily'] + '\', \'' + nodeDict['upTime'] + '\', \'' 
            + timestamp + '\');')
    return insertIntoNodeTable
    
#Builds the SQL string to insert all of the infomration into the network table
def constructNetworkInsert(networkDict, nodeID):
    insertIntoNetworkTable = ('INSERT INTO network (nodeID, networkInterface, publicIP, privateIP, '
            + 'netMask, defaultGateway, localHostname, publicHostname, interfaceState) VALUES ('
            + nodeID + ', \'' + networkDict['interface'] + '\', \''
            + networkDict['publicIP'] + '\', \'' + networkDict['privateIP'] + '\', \''
            + networkDict['netMask'] + '\', \'' + networkDict['defaultGateway'] + '\', \''
            + networkDict['localHostname'] + '\', \'' + networkDict['publicHostname'] + '\', \''
            + networkDict['state'] + '\');')
    return insertIntoNetworkTable
    
#Builds the base string for the CPU insert string, and loops through each CPU to
#add the values into a multi row insert statement
def constructCPUInsert(node, cpuList, nodeID):
    insertCPUStr = 'INSERT INTO CPU (nodeID, cores, vendor, speed, model) VALUES '
    #Builds each CPU into its own (value1, value2, ...) to add to the sql insert statement
    for i in range(0, node.getCPUCount()):
        insertCPUStr = insertCPUStr + individualCPUInsert(cpuList[i], nodeID)
    if i == node.getCPUCount() - 1:
        insertCPUStr = insertCPUStr + ';'
    else:
        insertCPUStr = insertCPUStr + ', '
    return insertCPUStr
    
#Builds the individual row to add to the multiline sql insert into the CPU table
def individualCPUInsert(cpuDict, nodeID):
    insertIntoCPUTable = ('(' + nodeID + ', ' +
            cpuDict['cores'] + ', \'' +
            cpuDict['vendor'] + '\', ' + cpuDict['speed'] + ', \'' + 
            cpuDict['model'] + '\')')
    return insertIntoCPUTable
    
#Builds the base string for the Filesystem insert string, and loops through each
#filesystem to add the values into a multi row insert statement
def constructFileSysInsert(node, fileSysList, nodeID):
    insertFileSysStr = ('INSERT INTO filesystem (nodeID, device, mountPoint, totalSize, ' +
                    'used, available, percentUsed) VALUES ')
    #Builds each Filesystem into its own (value1, value2, ...) to add to the sql insert statement
    for i in range(0, node.getFileSystemCount()):
        insertFileSysStr = insertFileSysStr + individualFileSysInsert(fileSysList[i], nodeID)
        if i == node.getFileSystemCount() - 1:
            insertFileSysStr = insertFileSysStr + ';'
        else: 
            insertFileSysStr = insertFileSysStr + ', '
                    
    return insertFileSysStr
    
#Builds the individual row to add to the multiline sql insert into the filesystem table
def individualFileSysInsert(fileDict, nodeID):
    insertIntoFilesystemTable = ('(' + nodeID + ', \'' + fileDict['device'] + '\', \'' +
            fileDict['mountPoint'] + '\', ' + fileDict['size'] + ', ' + 
            fileDict['used'] + ', ' + fileDict['available'] + ', \'' + 
            fileDict['percentUsed'] + '\')')
    return insertIntoFilesystemTable
    
#Inserts the nodes table string into the database and returns the nodeID to use in other table inserts
def insertNodeTableToDB(nodeStr, dbConnection):
    cursor = dbConnection.cursor()
    cursor.execute(nodeStr)
    cursor.execute('SELECT LAST_INSERT_ID();')
    idList = cursor.fetchone()
    return idList[0]
    
#Inserts the network, filesystem, and cpu tables sql string into the database
def insertRemainingNodeToDB(networkStr, cpuStr, fileSysStr, dbConnection):
    cursor = dbConnection.cursor()
    cursor.execute(networkStr)
    cursor.execute(cpuStr)
    cursor.execute(fileSysStr)