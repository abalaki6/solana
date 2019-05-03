class nodeClass:
    def __init__(self, public_key, tvu, tpu, storage_addr, rpc, latitude=9, longitude=20, city="Hobbiton", region="Shire", country="Middle Earth", ping=0):
        self.public_key = public_key
        self.tvu = tvu
        self.tpu = tpu
        self.storage_addr = storage_addr
        self.rpc = rpc
        self.latitude = latitude
        self.longitude = longitude
        self.city = city
        self.region = region
        self.country = country
        self.ping = ping
        self.slot_height = 0
        self.transaction_count = 0
        self.stake_weight = 0

    def printNodeInfo(self):
        print("Public Key: ", self.public_key)
        print("TVU: ", self.tvu)
        print("TPU: ", self.tpu)
        print("Storage Address: ", self.storage_addr)
        print("RPC: ", self.rpc)
        print("Latitude: ", self.latitude)
        print("Longitude: ", self.longitude)
        print("City: ", self.city)
        print("Region: ", self.region)
        print("Country: ", self.country)
        print("Ping: ", self.ping)

    def get_ip_address(self):
        return self.tvu.split(":")[0]

    def as_tuple(self):
        return (self.get_ip_address(), self.longitude, self.latitude, self.city, self.region, self.country, 
        self.ping, self.slot_height, self.transaction_count, self.stake_weight, self.public_key, self.tvu, 
        self.tpu, self.rpc, self.storage_addr, 0, 1)
