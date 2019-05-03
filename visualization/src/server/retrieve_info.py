import getopt
import ipapi
import nodeClass
import pymysql
import subprocess
import sys
import time
import os
from pythonping import ping

def explore_network(printInfo=False):
    output = subprocess.check_output("../../../target/debug/visualizer_rust --timeout 2 --network $(dig +short edge.testnet.solana.com):8001", shell=True)

    output = output.decode("utf-8")
    outputArray = output.splitlines()

    nodes = []
    numberOfNodes = int(outputArray[0])

    for node_data_text in outputArray[1:]:
        nodeInfo = [x.strip() for x in node_data_text.split(',')]
        currentNode = nodeClass.nodeClass(nodeInfo[0], nodeInfo[1], nodeInfo[2], nodeInfo[3], nodeInfo[4])
        nodes.append(currentNode)

        if printInfo:
            currentNode.printNodeInfo()

    return nodes

def get_network_info(nodes):
    get_location_info(nodes)
    ping_network(nodes)

def get_location_info(nodes):
    for node in nodes:
        nodeIP = node.get_ip_address()
        
        node.latitude  = ipapi.location(nodeIP, None, 'latitude')
        node.longitude = ipapi.location(nodeIP, None, 'longitude')
        node.city = ipapi.location(nodeIP, None, 'city')
        node.region = ipapi.location(nodeIP, None, 'region')
        node.country = ipapi.location(nodeIP, None, 'country')


def ping_network(nodes):
    for node in nodes:
        ip = node.get_ip_address()
        start = time.time()
        response = os.system("ping -c 1 " + ip)
        pingTime = time.time() - start

        if response == 0:
            node.ping = pingTime * 100
        else:
            node.ping = -1
    
        #responseList = ping(ip)
        #node.ping = responseList.rtt_avg_ms

def connect_to_database():
    connection = pymysql.connect(host='localhost', user="UIUC", password="UIUC_492", db="SOLANA")

    return connection

def upload_to_database(nodes, current_ip_list):
    pass
    connection = connect_to_database()

    with connection.cursor() as cursor:
        for node in nodes:
            ip_address = node.get_ip_address()
            if ip_address in current_ip_list:
                # Just need to update the information
                sql_req = ("UPDATE NODES_TEST "
                "(ip_addr, longitude, latitude, city, region, country, ping_time, "
                "slot_height, transaction_count, stake_weight, "
                "public_key, tvu_addr, tpu_addr, rpc_addr, storage_addr, "
                "map_depth, node_size) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

                cursor.execute(sql_req, node.as_tuple())

            else:
                # Need to insert into the database
                sql_req = ("INSERT INTO NODES_TEST "
                "(ip_addr, longitude, latitude, city, region, country, ping_time, "
                "slot_height, transaction_count, stake_weight, "
                "public_key, tvu_addr, tpu_addr, rpc_addr, storage_addr, "
                "map_depth, node_size) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                cursor.execute(sql_req, node.as_tuple())
                
                current_ip_list.add(node.get_ip_addr())
        cursor.commit()
    connection.close()

def insert_good_name_here(iterations, log_data, sleep_time):
    run_count = 0
    
    current_ip_list = set()

    while True:
        nodes = explore_network()

        get_network_info(nodes)

        if log_data:
            for node in nodes:
                node.printNodeInfo()
                print("")

        #  upload_to_database(nodes, current_ip_list)

        run_count += 1
        if iterations > 0 and run_count >= iterations:
            print(iterations, run_count)
            break
        time.sleep(sleep_time)

if __name__ == "__main__":
    argv = sys.argv[1:]

    # Code from tutorialspoint, python command line arguments page
    try:
        opts, args = getopt.getopt(argv, "hi:lt:", ["help", "iterations=", "log", "time="])
    except getopt.GetoptError:
        print("Invalid arguments. Type --help or -h?")
        sys.exit(2)

    iterations = 0
    log_data = True
    sleep_time = 30

    for opt, arg in opts:
        if opt in ("--help", "-h"):
            print("retrieve_info.py -i <iterations> -l -time <time>")
            print("-i   Iterations is how many times the data is collected. 0 (default) is forever.")
            print("-l   Log data.")
            print("-t   Time between data collection. Default 10 seconds")
            sys.exit(2)
        elif opt in ("-i", "--iterations"):
            iterations = int(arg)
            if iterations < 0:
                print("Iterations must be a positive integer or 0")
                sys.exit(2)
        elif opt in ("-l", "--log"):
            log_data = True
        elif opt in ("-t", "--time"):
            sleep_time = int(arg)
            if sleep_time <= 0:
                print("time must be a non-negative integer")
                sys.exit(2)

    insert_good_name_here(iterations, log_data, sleep_time)

'''
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

'''
