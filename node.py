class node:
    nodeDict = {}
    cpuNum = 0
    cpuList = []
    fileSysNum = 0
    fileSysList = []
    networkDict = {}
    
    #Initializes the class, ensure to clear out previous artifacts int the dictionary
    def __init__(self):
        self.nodeDict = {}
        self.cpuList = []
        self.fileSysList = []
        self.networkDict = {}
   
    #Adds the passed in information to a dictionary that represents the base node information 
    def addNodeInfo(self, name, chef_environment, services_partition, launch, platform, platform_version, platform_family, uptime):
        self.nodeDict = {'nodeName' : name, 'chefEnv' : chef_environment, 'cloudEnv' : services_partition, 'dateCreated' : launch, 'platform' : platform, 'platformVersion' : platform_version, 'platformFamily': platform_family, 'upTime' : uptime}
    
    #Sets the total number of CPUS attached to the system
    def setCPUNum(self, cpu):
        self.cpuNum = cpu
    
    #Adds the passed in information to a new dictionary and appends that dictionary to the list of cpus
    def addCPU(self, vendor_id, model_name, mhz, cores):
        ghz = float(mhz) / 1000.00
        self.cpuList.append({'vendor': vendor_id, 'model' : model_name, 'speed' : str(ghz), 'cores' : cores})

    #Sets the total number of FileSystems attached to the system
    def setFileSystemCount(self):
        self.fileSysNum = len(self.fileSysList)
    
    #Adds the file system information to a new dictionary, and appends that dictionary to the list of file systems 
    def addFileSystem(self, device, mountPt, kb_size, kb_used, kb_available, percent_used):
        totalGB = float(kb_size) / 1000000.00
        usedGB = float(kb_used) / 1000000.00
        availableGB = float(kb_available) / 1000000.00
        self.fileSysList.append({'device' : device, 'mountPoint' : mountPt, 'size' : str(totalGB), 'used' : str(usedGB), 'available' : str(availableGB), 'percentUsed' : percent_used})
        self.setFileSystemCount()

    #Adds the passed in variables into a dictionary that represents the network for the computer
    def addNetworkInfo(self, interface, netmask, default_gateway, state, local_hostname, public_hostname, ipaddress, public_ipv4):
        self.networkDict = {'interface' : interface, 'netMask' : netmask, 
                'defaultGateway' : default_gateway, 'state' : state, 'localHostname' : local_hostname, 
                'publicHostname' : public_hostname, 'privateIP' : ipaddress, 
                'publicIP' : public_ipv4}
     
    #returns the full node dictionary            
    def getNodeDictionary(self):
        return self.nodeDict
    
    #returns the total of the CPU 
    def getCPUCount(self):
        return self.cpuNum
    
    #returns the entire list of dictionaries containing each CPU instance
    def getCPUList(self):
        return self.cpuList
        
    #Returns the number of attached file systems   
    def getFileSystemCount(self):
        return self.fileSysNum
    
    #returns the entire list of dictionaries containing each FileSystem attached
    def getFileSystemList(self):
        return self.fileSysList
    
    #returns the dictionary containing the network information
    def getNetworkDictionary(self):
        return self.networkDict

    #Formatted toString just to view data in lambda 
    def displayNodeInfo(self):
        print('_______________________________________________________________________________________')
        print('Node Info:')
        print('    Name: ' +  self.nodeDict['nodeName'])
        print('    Chef Environment: ' +  self.nodeDict['chefEnv'])
        print('    Cloud Environment: ' +  self.nodeDict['cloudEnv'])
        print('    Date Created: ' + self.nodeDict['dateCreated'])
        print('    Platform: ' +  self.nodeDict['platform'])
        print('    Platform Version: ' +  self.nodeDict['platformVersion'])
        print('    Platform Family: ' +  self.nodeDict['platformFamily'])
        print('    Uptime: ' +  self.nodeDict['upTime'])
        print('')
        
        count = 1
        for cpu in self.cpuList:
            print('CPU ' + str(count) + ': ')
            print('    Vendor: ' + cpu['vendor'])
            print('    Model: ' + cpu['model'])
            print('    Speed: ' + cpu['speed'])
            print('    Cores: ' + cpu['cores'])
            count = count + 1
        
        print()
        count = 1
        for fSys in self.fileSysList:
            print('File System ' + str(count) + ': ')
            print('    Device: ' + fSys['device'])
            print('    Mountpoint: ' + fSys['mountPoint'])
            print('    Total Space: ' + fSys['size'])
            print('    Used Space: ' + fSys['used'])
            print('    Free Space: ' + fSys['available'])
            print('    Percent Used: ' + fSys['percentUsed'])
            count = count + 1
        print()
            
        print('Network Info:')
        print('    Interface: ' +  self.networkDict['interface'])
        print('    Network Mask: ' +  self.networkDict['netMask']) 
        print('    Default Gateway: ' + self.networkDict['defaultGateway'])
        print('    State: ' +  self.networkDict['state'])
        print('    Local Hostname: ' +  self.networkDict['localHostname'])
        print('    Public Hostname: ' +  self.networkDict['publicHostname'])
        print('    Private IP: ' +  self.networkDict['privateIP'])
        print('    Public IP: ' +  self.networkDict['publicIP'])
        print('_______________________________________________________________________________________')
        print()