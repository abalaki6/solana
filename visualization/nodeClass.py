class nodeClass:
    def __init__(self, public_key, tvu, tpu, storage_addr, rpc, latitude=None, longitude=None, city=None, region=None, country=None):
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

    def get_ip_address(self):
        return self.public_key.split(":")[0]
