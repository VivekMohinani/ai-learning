from pymongo import MongoClient
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from array import array

from random import uniform, randrange


# Functions
def getCpuTime(cpuNum):
    match cpuNum:
        case 1:
            return 10
        case 2:
            return 20
        case 3:
            return 30
        case 4:
            return 40
        case 5:
            return 50
        case _:
            return "CPU num error"


def getGpuTime(gpuNum):
    match gpuNum:
        case 1:
            return 100
        case 2:
            return 200
        case 3:
            return 300
        case 4:
            return 400
        case 5:
            return 500
        case _:
            return "GPU num error"


def getRamTime(ramNum):
    match ramNum:
        case 1:
            return 50
        case 2:
            return 60
        case 3:
            return 70
        case 4:
            return 80
        case 5:
            return 90
        case _:
            return "RAM num error"


def getMemTime(memNum):
    match memNum:
        case 1:
            return 600
        case 2:
            return 700
        case 3:
            return 800
        case 4:
            return 900
        case 5:
            return 1000
        case _:
            return "MEM num error"


def getNetLagTime(netLagNum):
    match netLagNum:
        case 1:
            return 300
        case 2:
            return 600
        case 3:
            return 900
        case 4:
            return 1200
        case 5:
            return 1500
        case _:
            return "NET LAG num error"


def randFloatGen():
    return round(uniform(0.95, 1.05), 2)


def randMetricValGen():
    val = randrange(1, 6)
    return val


def calculateSpeed(total):
    return total * randFloatGen()


def editTupleVal(index, t, newVal):
    converted_list = list(t)
    converted_list[index] = newVal
    return t(converted_list)


def extractTotalSpeedFromTuple(t):
    # Tuple structure
    resource_name = 0
    resource_num = 1
    resource_speed = 2

    total_speed = 0
    for entry in t:
        total_speed += entry[resource_speed]
    return total_speed


def printDataFormatted(data):
    for entry in data:
        print(entry)
        for resource in entry:
            print(resource)
        print()


def formatData(t, speed):
    # Tuple structure
    resource_name = 0
    resource_num = 1
    resource_speed = 2

    formatted_data = []
    for entry in t:
        new_tuple = (
            entry[resource_name],
            entry[resource_num]
        )
        formatted_data.append(new_tuple)

    # round to the nearest ms
    formatted_data.append(("speed", round(speed)))
    return formatted_data


def generateData(amount):
    entries = []
    for entry in range(amount):
        cpu_num = randMetricValGen()
        gpu_num = randMetricValGen()
        ram_num = randMetricValGen()
        mem_num = randMetricValGen()
        net_lag_num = randMetricValGen()

        # store data: name, num, speed
        split_speeds = [
            ("cpu", cpu_num, getCpuTime(cpu_num)),
            ("gpu", gpu_num, getGpuTime(gpu_num)),
            ("ram", ram_num, getRamTime(ram_num)),
            ("mem", mem_num, getMemTime(mem_num)),
            ("net_lag", net_lag_num, getNetLagTime(net_lag_num))
        ]

        # output data for private validation.
        # printDataFormatted(split_speeds)

        speed = calculateSpeed(extractTotalSpeedFromTuple(split_speeds))
        formatted_data = formatData(split_speeds, speed)

        entries.append(formatted_data)
    return entries


# Data comes in as a list(list(resources,values/speed,value)
def storeData(fData, collection):
    # Tuple structure
    cpu = 0
    gpu = 1
    ram = 2
    mem = 3
    net_lag = 4
    speed = 5

    key = 0
    val = 1

    documents = []

    for entry in fData:
        new_document = {
            entry[cpu][key]: entry[cpu][val],
            entry[gpu][key]: entry[gpu][val],
            entry[ram][key]: entry[ram][val],
            entry[mem][key]: entry[mem][val],
            entry[net_lag][key]: entry[net_lag][val],
            entry[speed][key]: entry[speed][val]
        }
        documents.append(new_document)
        # print(f"new_document = {new_document}")
    # print(documents)
    return collection.insert_many(documents)


def genAndStoreData(entries):
    # Mongo Setup
    client = MongoClient('localhost', 27017)  # Replace with your MongoDB server and port
    db = client['inoJam']  # Replace with your database name
    collection = db['modelingData2']  # Replace with your collection name

    # Data Setup and Storage
    data = generateData(entries)
    response = storeData(data, collection)

    client.close()
    return response


# MAIN
def main():
    default_val = 100
    ids = genAndStoreData(default_val).inserted_ids


if __name__ == "__main__":
    main()
