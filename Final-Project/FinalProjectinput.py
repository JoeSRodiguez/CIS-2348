import csv
from datetime import datetime

class Item:
    #this is creating a class to grab all of the information provided by the csv files and making an instance of them
    def __init__(self, itemId, manufacturer, itemType, price=None, serviceDate=None, damaged=False):
        self.itemId = itemId
        self.manufacturer = manufacturer
        self.itemType = itemType
        self.price = price
        self.serviceDate = serviceDate
        self.damaged = damaged

    def isDamaged(self):
        if self.damaged:
            return 'damaged'
        else:
            return ''

#this is used to print out values to str when needed
    def __str__(self):
        return(f"Item ID: {self.itemId}, Manufacturer: {self.manufacturer}, Item Type: {self.itemType}, Price: {self.price}, service Date: {self.serviceDate}, Damaged: {self.damaged}")
    
items = {}
#gets the date for future part of the code


#this is used to read the data off manufacturer list
with open('ManufacturerList.csv', mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        itemId, manufacturer, itemType = row[0], row[1].strip(), row[2].strip()
        damaged = row[3].strip() == 'damaged' if len(row) > 3 else False
        items[itemId] = Item(itemId, manufacturer, itemType, damaged=damaged)

#this is used to read the data off price list
with open('PriceList.csv', mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        item_id, price = row[0], row[1]
        if item_id in items:
            items[item_id].price = price

#this is used to read the data off serviceDate list

with open('ServiceDatesList.csv', mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        item_id, service_date = row[0], row[1]
        if item_id in items:
            items[item_id].serviceDate = service_date  # Correct attribute name


#getting the item manufacturer item as a method instead in order to use in the sorted atribute
def getManufacturer(item):
    return item.manufacturer
#getting the item ID item as a method instead in order to use in the sorted atribute
def getItemId(item):
    return item.itemId

#using this method to sort items based on the manufacturer atribute
sortedItems = sorted(items.values(), key=getManufacturer)


#_________This code below will be used to create the full inventory CSV file____________

#this creates the header on top of the csv file

with open('FullInventory.csv', mode='w', newline = '') as file:
    writer = csv.writer(file)
    writer.writerow(['Item ID', 'Manufacturer', 'Item Type', 'Price', 'Service Date', 'Damaged' ])

#this adds the data onto that header 
    for item in sortedItems:
        writer.writerow([item.itemId, item.manufacturer, item.itemType, item.price, item.serviceDate, item.isDamaged()])

#_________This code below will be used to create the  item Inventory.csv file__________

typeOfItems = {}

#this identifies the item types in order to use them
for item in items.values():
    if item.itemType not in typeOfItems:
        typeOfItems[item.itemType] = []
    typeOfItems[item.itemType].append(item)

#this sorts them based on what they are

for itemType, itemList in typeOfItems.items():
    sortedItems = sorted(itemList, key=getItemId)
    #this is a variable used to create the upcoming
    filename = f'{itemType.capitalize()}Inventory.csv'

    with open(filename, mode="w", newline= '') as file:
        writer = csv.writer(file)
        writer.writerow(['Item ID', 'Manufacturer', 'Price', 'Service Date', 'Damaged' ])
        for item in sortedItems:
            writer.writerow([item.itemId, item.manufacturer, item.price, item.serviceDate, item.isDamaged()])

#_________This code below will be used to create the PastServiceDateInventory.csv file__________

today = datetime.today().date()

# Filter items that are past their service date
pastServiceItems = [
    item for item in items.values()
    if item.serviceDate and datetime.strptime(item.serviceDate, '%m/%d/%Y').date() < today
]

# Sort the items that are past their service date
pastServiceItemsSorted = sorted(pastServiceItems, key=lambda x: datetime.strptime(x.serviceDate, '%m/%d/%Y').date())

# Write the sorted items to the PastServiceDateInventory.csv file
with open('PastServiceDateInventory.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Item ID', 'Manufacturer', 'Item Type', 'Price', 'Service Date', 'Damaged'])
    for item in pastServiceItemsSorted:
        writer.writerow([item.itemId, item.manufacturer, item.itemType, item.price, item.serviceDate, item.isDamaged()])


#_________This code below will be used to create the DamagedInventory.csv file__________

damagedItems = [item for item in items.values() if item.damaged]
damagedItemsSorted = sorted(damagedItems, key=lambda x: float(x.price), reverse=True)

with open('DamagedInventory.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Item ID', 'Manufacturer', 'Item Type', 'Price', 'Service Date'])
    for item in damagedItemsSorted:
        writer.writerow([item.itemId, item.manufacturer, item.itemType, item.price, item.serviceDate])





