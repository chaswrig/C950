# Package delivery program. Delivers 40 packages around SLC area in under 140 miles and earlier than 5pm.
import csv
from HashTable import HashTable
from datetime import *

# Prompt to start program.
input("Press enter key to start the simulation.")
print("")

# This block reads through the CSV file and adds the packages to a list in memory
# List is used to populate hash table only
with open('package_file.csv') as csv_package_file:
    readCSV = csv.reader(csv_package_file, delimiter=',')
    packages = []
    for row in readCSV:
        package_id = row[0]
        package_address = row[1]
        package_city = row[2]
        package_state = row[3]
        package_zip = row[4]
        package_deadline = row[5]
        package_mass = row[6]
        package_notes = row[7]
        package_status = ''

        package = [package_id, package_address, package_city, package_state, package_zip,
                   package_deadline, package_mass, package_notes, package_status]

        packages.append(package)

    csv_package_file.close()

# Adds hash table with same number of buckets as items in list. Scalable with a variable format.
ht1 = HashTable(40)

# Sets status to at hub
for package in packages:
    package[8] = "At the Hub"

# Sets status "Delayed" for those that were delayed
packages[6][8] = "Delayed. Will not arrive until at hub until 9.05 am"
packages[9][8] = "Wrong address. Will not update until 10.20 am"
packages[25][8] = "Delayed. Will not arrive until at hub until 9.05 am"
packages[28][8] = "Delayed. Will not arrive until at hub until 9.05 am"
packages[32][8] = "Delayed. Will not arrive until at hub until 9.05 am"

# Update the header for status reports
packages[0][8] = "Time Delivered"

# Adds packages to the hash table
for i in range(len(packages)):
    if packages[i] is packages[0]:  # skips the header line
        continue
    else:
        ht1.addItem(packages[i])

# Imports distance list from CSV file
# Code block provided by course instructor
distances_list = []
with open("distance_table.csv", 'r') as csv_distance_file:
    readCSV = csv.reader(csv_distance_file, delimiter=',')
    for row in readCSV:
        distances_list.append(row)

    csv_distance_file.close()

# Builds dictionary for distances
dictionary = {}
i = 0
for distance in distances_list:
    dictionary[distance[0]] = i
    i += 1

# Set the clock to 8AM
start_time = datetime(2020, 1, 18, 8, 0, 0, 0)
truck_current_time = datetime(2020, 1, 18, 8, 0, 0, 0)

truck_total_distance = 0.0  # Global variable to track how far truck has traveled.

# Which packages will go on which truck
truck_list = [1, 7, 13, 14, 15, 16, 19, 20, 21, 29, 30, 31, 34, 37, 39, 40]  # All 'together' and by 9/10.30 items
truck2_list = [3, 6, 18, 25, 28, 32, 36, 38]
truck3_list = [2, 4, 5, 8, 9, 10, 11, 12, 17, 22, 23, 24, 26, 27, 33, 35]

# For this program I'm only using one truck. I assume "Truck 2" is the second trip.
trips = [truck_list, truck2_list, truck3_list]

truck = []  # The "truck" is just a list of packages (a list of lists)

# Runs through each trip in order.
for trip in trips:

    # Loads the truck with the listed packages.
    for item in trip:
        truck.append(packages[item])
        print("Package #" + packages[item][0] + " loaded to Truck.")

    print("")

    # Change package statuses to "En Route" once loaded on truck.
    for package in truck:
        package[8] = "En Route"

    # Start each trip at hub.
    current_location = distances_list[1][0]
    print("Starting Time: " + str(truck_current_time))
    print("Starting Location: " + current_location)

    # If there are items in the truck the program tries to find nearest neighbor.
    while len(truck) != 0:
        # Get Truck's next location
        next_location = distances_list[dictionary[truck[0][1]]][0]  # first item in truck
        next_package_id = truck[0][0]
        distance_to_next = 99.0  # High enough number to ensure that any comparisons in this sim are lower.

        for package in truck:
            # Holder used to compare locations
            temp_next_location = package[1]
            # Finds the distance to the next place. If table is blank, swaps them and looks again.
            if distances_list[dictionary[temp_next_location]][dictionary[current_location]] == "":
                temp_distance = float(distances_list[dictionary[current_location]][dictionary[temp_next_location]])
            else:
                temp_distance = float(distances_list[dictionary[temp_next_location]][dictionary[current_location]])
            # Compare locations, keep the closest.
            if temp_distance < distance_to_next:
                distance_to_next = temp_distance
                next_location = temp_next_location
                next_package_id = packages[int(package[0])]

        # Informs user of the next package to be delivered, its location, and its distance.
        print("Next Package: " + str(next_package_id))
        print("Distance to next location: " + str(distance_to_next))

        # "Moves" the truck to the next location and "delivers" the package.
        # Formula == 18 MPH / 60 MIN == 60 MIN / 18 MILE == DIVIDE BY 18 == 3 MIN 20 SECONDS PER MILE
        segment_time = distance_to_next * 3.33
        truck_current_time += timedelta(minutes=(int(segment_time)))
        truck_total_distance += distance_to_next
        current_location = distances_list[dictionary[next_location]][0]
        # Updates the package's status.
        ht1.updateItem(int(next_package_id[0]), "Delivered at " + str(truck_current_time))
        print("Package delivered at " + str(truck_current_time))
        print("")
        truck.remove(next_package_id)

        # Print status screens at given intervals.
        if truck_current_time >= datetime(2020, 1, 18, 9, 20) and truck_current_time <= datetime(2020, 1, 18, 9, 25):
            print("Status as of " + str(truck_current_time) + ":")
            for package in packages:
                print(package)
            print("")

        if truck_current_time >= datetime(2020, 1, 18, 10, 20) and truck_current_time <= datetime(2020, 1, 18, 10, 25):
            print("Status as of " + str(truck_current_time) + ":")
            for package in packages:
                print(package)
            print("")

        if truck_current_time >= datetime(2020, 1, 18, 12, 45) and truck_current_time <= datetime(2020, 1, 18, 13, 00):
            print("Status as of " + str(truck_current_time) + ":")
            for package in packages:
                print(package)
            print("")

    # Takes the truck back to the hub when empty and gives status updates.
    if len(truck) == 0:
        next_location = distances_list[1][0]
        distance_to_next = float(distances_list[dictionary[current_location]][1])
        truck_total_distance += distance_to_next
        current_location = distances_list[dictionary[next_location]][0]
        print("All packages on Truck have been delivered.")
        print("Returning to hub. The distance to the hub is " + str(distance_to_next) + " miles.")
        print("Truck has returned to the hub having travelled a total of " + str(truck_total_distance) + " miles.")
        print("The truck left the hub at " + str(start_time) + ".")
        print("The truck returned at " + str(truck_current_time) + ".")
        print("")
        start_time = truck_current_time

print("All packages delivered by " + str(truck_current_time))
print("The truck traveled a total of " + str(truck_total_distance) + " miles.")
print("")

# Final status screen
print("Final Status:")
for package in packages:
    print(package)
print("")

# Package lookup
check_status = True
while check_status is True:
    print("You can look up a package by entering the package ID.")
    package_lookup = input("Enter a package ID:")
    hour_lookup = input("Enter an hour between 0 and 23:")
    minute_lookup = input("Enter minutes between 0 and 59:")
    time_lookup = datetime(2020, 1, 18, int(hour_lookup), int(minute_lookup))

    for package in packages:
        if package[0] == package_lookup:
            if time_lookup < datetime.strptime(package[8][13:], "%Y-%m-%d %H:%M:%S"):
                print("Package ID: " + package[0] + "\tAddress: " + package[1] + " " + package[2] + ", " + package[3] + " " + package[4])
                print("Due By: " + package[5])
                print("Package weight: " + package[6])
                print("Special Notes: " + package[7])
                print("Status: Package en route. Will not be delivered until " + package[8][13:] + ".")
            else:
                print(package)

    look_again = str.upper(input("Would you like to look again? Enter \'Y\' or \'N\'"))
    if look_again == "Y":
        check_status = True
    elif look_again == "N":
        print("Have a good day.")
        check_status = False
    else:
        print("Invalid input. Goodbye.")
        check_status = False
