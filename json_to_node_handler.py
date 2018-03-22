import boto3
import node
import json
from datetime import datetime, timezone

def parseJSONfile(bucketName, key):
    #Creates the connection to the bucket
    s3_conn = boto3.resource('s3')
    logfile = s3_conn.Object(bucketName, key)
    nodeList = getInstances(logfile)
    return nodeList

#Iterates through each node of the JSON file and launches parse methods
#Will throw an error if newest file is not JSON, otherwise returns a list of nodes
def getInstances(file):
    try:
        file_content = file.get()['Body'].read()
        json_content = json.loads(file_content)
        nodeCount = json_content['results']
        nodeList = []
        for instance in json_content['rows']:
            n = node.node()
            getNodeInfo(instance, n)
            getCPUInfo(instance, n)
            getFileSystemInfo(instance, n)                
            getNetworkInfo(instance, n)
            nodeList.append(n)
        return nodeList
    except Exception as e:
        raise e
    return None
    
    
        
#Parses JSON to collect base Node attributes
def getNodeInfo(instance, node):
    # Launch Time seems to be the same for both resources, not sure this is the correct value
    ec2_conn = boto3.resource('ec2')
    ec2inst = ec2_conn.Instance(instance['automatic']['ec2']['instance_id'])
    #launchTime = str(ec2inst.launch_time)
    launchTime = str(datetime.now(timezone.utc))
    
    node.addNodeInfo(instance['name'], instance['chef_environment'],
            instance['automatic']['ec2']['services_partition'], launchTime, 
            instance['automatic']['platform'], instance['automatic']['platform_version'], 
            instance['automatic']['platform_family'], instance['automatic']['uptime'])
        
#Parses through each CPU attached, and collects necessary attributes
def getCPUInfo(instance, node):
    cpuCount = instance['automatic']['cpu']['total']
    node.setCPUNum(cpuCount)
    for i in range(0, cpuCount):
        cpu = instance['automatic']['cpu'][str(i)]
        node.addCPU(cpu['vendor_id'], cpu['model_name'], cpu['mhz'], cpu['cores'])
        
#Parses through SINGULAR filesystem, and collects necessary attributes
#TODO: Add functionality to iterate through all filesystems when naming scheme is discovered
def getFileSystemInfo(instance, node):
    fileSys = instance['automatic']['filesystem']['by_device']['/dev/xvda2']
    node.addFileSystem('/dev/xvda2', fileSys['mounts'][0], fileSys['kb_size'], 
            fileSys['kb_used'], fileSys['kb_available'], fileSys['percent_used'])
    
#Parses through SINGULAR network, and collects necessary attributes
def getNetworkInfo(instance, node):
    network = instance['automatic']
    ip = network['ipaddress']
    node.addNetworkInfo(network['network']['interfaces']['eth0']['type'],
            network['network']['interfaces']['eth0']['addresses'][ip]['netmask'], 
            network['network']['default_gateway'],
            network['network']['interfaces']['eth0']['state'], network['ec2']['local_hostname'], 
            network['ec2']['public_hostname'], network['ipaddress'], network['cloud']['public_ipv4'])