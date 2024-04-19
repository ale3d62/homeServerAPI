import json
import requests
from bottle import post, request, run, app
from bottle_cors_plugin import cors_plugin
import socket
import math
import os


#----EDITABLE PARAMETERS----
#HomeServer
serverPort = 8888
receiverPort = 8889


#Set the working directory to the directory of the script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


#Confugure the server to prevent cors policy errors
app = app()
app.install(cors_plugin('*'))



#Returns the system's ip address
def getSystemIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ipAddress = (s.getsockname()[0])
    s.close()
    return ipAddress


#******************************
#---------HTTP METHODS---------
#******************************

#TO DO LIST
#Returns the content of todoList.json
@post('/getTodoList')
def getTodoList():
    with open("todoList.json", 'r') as f:
        jsonData = json.load(f)
        f.close()
    return json.dumps(jsonData)


#Receives a to do list item and deletes it from the todoList.json 
@post('/deleteTodoListItem')
def deleteTodoListItem():
    data = request.json
    itemText = data['itemText']
    with open("todoList.json", 'r+') as f:
        jsonData = json.load(f)
        jsonData['todoList'].remove(itemText)

        #update the json file
        f.seek(0)
        f.truncate()
        json.dump(jsonData, f)

        f.close()


#Receives a to do list item and an edited version of that item.
#Replaces the content of the item at todoList.json with the new version
@post('/editTodoListItem')
def editTodoListItem():
    data = request.json
    print(data)
    itemText = data['itemText']
    itemNewText = data['itemNewText']
    with open("todoList.json", 'r+') as f:
        jsonData = json.load(f)
        itemIndex = jsonData['todoList'].index(itemText)
        jsonData['todoList'][itemIndex] = itemNewText

        #update the json file
        f.seek(0)
        f.truncate()
        json.dump(jsonData, f)

        f.close()


#Receives a to do list item and appends it into todoList.json
@post('/addTodoListItem')
def addTodoListItem():
    data = request.json
    itemText = data['itemText']
    with open("todoList.json", 'r+') as f:
        jsonData = json.load(f)
        jsonData['todoList'].append(itemText)

        #update the json file
        f.seek(0)
        f.truncate()
        json.dump(jsonData, f)

        f.close()



#WALLPAPERS
#Receives a Wallhaven username and a collectionId corresponding to a collection of that user
#Returns a list with the wallpapers filenames of that collection
@post('/getWallpapers')
def getWallpapers():
    data = request.json
    wallhavenUsername = data['wallhavenUsername']
    wallhavenCollectionId = data['wallhavenCollectionId']

    wallNames = []


    #get collection size
    apiResponse = requests.get("https://wallhaven.cc/api/v1/collections/" + wallhavenUsername)
    if("error" in apiResponse.json()):
        print("Error during the api request, check the username and the collection Id")
        return

    collectionSize = 0

    userCollections = apiResponse.json()['data']
    for collection in userCollections:
        if str(collection['id']) == wallhavenCollectionId:
            collectionSize = collection['count']

        #there is a maximum of 24 wallpapers per page
    nCollectionPages = math.ceil(collectionSize % 24)


    for currentPage in range(nCollectionPages):

        apiResponse = requests.get("https://wallhaven.cc/api/v1/collections/" + wallhavenUsername + "/" + wallhavenCollectionId + "?page=" + str(currentPage+1))
        if("error" in apiResponse.json()):
            return json.dumps({"error": wallNames})

        collectionWalls = apiResponse.json()['data']
        for wall in collectionWalls:
            #Obtain the wall name and extension
            wallId = wall["id"]
            wallUrl = wall["path"]
            wallFileExtension = wallUrl.split('.')[-1]
            wallName = "wallhaven-"+wallId+"."+wallFileExtension

            wallNames.append(wallName)

    return json.dumps({"wallpaperNames": wallNames})




if __name__ == '__main__':
    run(host = getSystemIp(), port = serverPort, debug = True)
