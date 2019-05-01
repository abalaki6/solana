class nodeClass:
    def __init__(self, public_key, tvu, tpu, storage_addr, rpc, latitude=9, longitude=20, city="Hobbiton", region="Shire", country="Middle Earth"):
>>>>>>> 0d04073b4a623b36a9694ac3a1ab961ddb31001a:visualization/src/server/nodeClass.py
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
        return self.public_key.split(":")[0]

    def as_tuple(self):
        return (self.get_ip_address(), self.longitude, self.latitude, self.city, self.region, self.country, 
        self.ping_time, self.slot_height, self.transaction_count, self.stake_weight, self.public_key, 0, 0, 1)
