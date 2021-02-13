# HashTable class adapted from Zybooks Chaining Hashtable Example (Data Structures and Algorithms section 7.2.)
class HashTable:

    def __init__(self, size):
        self.table = []
        for i in range(size):
            self.table.append([])

    # Modulo hash function using the package id
    # Adapted from hash table tutorial
    def getHash(self, package_id):
        # A variable could be added to the funciton and in place of '40'
        # to make more or fewer buckets depending on scaling needs.
        return package_id % 40

    def addItem(self, package):
        package_id = int(package[0]) # pulls package id from package
        bucket = self.getHash(package_id) # passes to hash funciton
        bucket_list = self.table[bucket] # identifies which bucket
        # print("Add working.")
        bucket_list.append(package) # places package in bucket

    def searchItem(self, package):
        if package in range(1,41):
            package_id = package
        else:
            print("Package ID out of range. Defaulting to package 40")
            return 40
        bucket = self.getHash(package_id)
        bucket_list = self.table[bucket]

        if bucket_list != []:
            # print("Search working")
            print(bucket_list[0])
        else:
            print("Package not found.")

    def removeItem(self, package):
        package_id = package
        bucket = self.getHash(package_id)
        bucket_list = self.table[bucket]

        if bucket_list != []:
           # print("Remove working.")
           bucket_list.clear()

    # Updates a package's status.
    def updateItem(self, package, status):
        package_id = package
        bucket = self.getHash(package_id)
        bucket_list = self.table[bucket]
        bucket_list[0][8] = status
