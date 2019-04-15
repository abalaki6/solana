import subprocess
import nodeClass
import ipapi

# gossip_process = subprocess.Popen(["../target/debug/solana-gossip", "--timeout", "5", "--network", "$(dig +short edge.testnet.solana.com):8001"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
# output = gossip_process.communicate()

# output = subprocess.check_output(["../target/debug/solana-gossip", "--timeout", "5", "--network", "$(dig +short edge.testnet.solana.com):8001"], shell=True)

output = subprocess.check_output("../target/debug/visualizer_rust --timeout 2 --network $(dig +short edge.testnet.solana.com):8001", shell=True)


print("\n================\n")

#output = "2\npk1,ss1,tvu1,tpu1,sa1,rpc1\npk2,ss2,tvu2,tpu2,sa2,rpc2\n"
output = output.decode('utf-8')
outputArray = output.splitlines()
#outputArray = output

#print(output)

nodes = []
numberOfNodes = int(outputArray[0])

for i in range(numberOfNodes):
    nodeInfo = [x.strip() for x in outputArray[i+1].split(',')]

    nodeIP = nodeInfo[1].split(':')[0]
    
    lati = ipapi.location(nodeIP, None, 'latitude')
    longi = ipapi.location(nodeIP, None, 'longitude')
    city = ipapi.location(nodeIP, None, 'city')
    region = ipapi.location(nodeIP, None, 'region')
    country = ipapi.location(nodeIP, None, 'country')

    currentNode = nodeClass.nodeClass(nodeInfo[0], nodeInfo[1], nodeInfo[2], nodeInfo[3], nodeInfo[4], lati, longi, city, region, country)
    nodes.append(currentNode)

for i in range(numberOfNodes):
    nodes[i].printNodeInfo()
    print("\n")
