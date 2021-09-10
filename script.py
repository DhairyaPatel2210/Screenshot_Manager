import os,shutil,time
from datetime import date
import sqlite3
import datetime
from tkinter import *
from tkinter import messagebox



# function will count the total number of present files
def count_files(folder_path):
    counter = 0
    for path in os.listdir(folder_path):
        counter += 1
    return counter


# it will return the file path which is added currently
def fileAtCount(fileNumber, folder_path):
    counter = 0
    for file in os.listdir(folder_path):
        counter += 1
        if counter == fileNumber :
            return file


# it is used to get the current date
def getDate():
    today = date.today()
    currentDate = today.strftime("%b-%d-%Y")
    return currentDate

# It will going to check whether the file with the same name is already created or not
def isFilePresent(dest_folder, file_name) :
    for file in os.listdir(dest_folder) :
        if file == file_name :
            return True
    return False

# this function will rename the file and also move it from source to destination
def renameAndMove(fileCounter,count, folder_path, file_count, dest_folder):
    file = fileAtCount(count,folder_path)
    currentDate = getDate()
    file_path = folder_path + "/" + file
    new_name = folder_path + "/" + str(file_count) + "_" + currentDate + ".png"
    # If file is not present then it will simply add the file at dest_folder
    if not isFilePresent(dest_folder,str(file_count) + "_" + currentDate + ".png") :
        os.rename(file_path, new_name)
        shutil.move(new_name, dest_folder)
        fileCounter += 1
        return fileCounter
    # If There is a File already with the same name then it will simply get the count and add 1 to it
    # and according to that name it will add the file at dest_folder
    else :
        noOfFilesAtNewFolder = count_files(dest_folder)
        file_path = folder_path + "/" + file
        new_name = folder_path + "/" + str(noOfFilesAtNewFolder+1) + "_" + currentDate + ".png"
        os.rename(file_path, new_name)
        shutil.move(new_name, dest_folder)
        fileCounter += 1
        return fileCounter


# This function will create new folder with name current date
def makeFolder(newFolderPath):
    flag = True
    nameList = newFolderPath.split("/")
    i=0
    folderPath = ""
    while i < len(nameList)-1 :
        folderPath = folderPath + nameList[i] + "/"
        i+=1
    folderName = nameList[-1]
    for path in os.listdir(folderPath) :
        if path == folderName :
            flag = False
    if flag :
        os.mkdir(newFolderPath)



# This function will determine whether the script to move files should run or not
def checkTime() :
    lec_time = 0
    lec_date = 0
    current_time = 0


def mainScript(folder_path,dest_folder,totalSec):
    # folder_path = "C:/Users/Dhairya/Pictures/Screenshots"
    # dest_folder = "D:/ScreenShot"
    file_count = 1

    # creating new folder for date
    try:
        new_folder = dest_folder + "/" + getDate()
        makeFolder(new_folder)
        dest_folder = new_folder
    except Exception as error:
        print("error while creating folder",error)

    initial_count = count_files(folder_path)

    # Gaining required time for running loop
    endTime = time.time() + totalSec
    # script running continuously to check new ss is added or not
    while time.time() < endTime:
        count = count_files(folder_path)
        if count > initial_count:
            try:
                file_count = renameAndMove(file_count,count,folder_path, file_count, dest_folder)
            except Exception as inst:
                print(inst)
        time.sleep(2)
    mainFunction()


# This function will time span of any lecture
def getTimeDiff(startingHr, startingMin, endingHr, endingMin) :
    s1 = str(startingHr) + ":" + str(startingMin) + ":00"
    s2 = str(endingHr) + ":" + str(endingMin) + ":00"
    FMT = '%H:%M:%S'
    tdelta = datetime.datetime.strptime(s2, FMT) - datetime.datetime.strptime(s1, FMT)
    return tdelta.total_seconds()


# Function will return the user entered sourcePath
def getSource() :
    try :
        sourceDB = sqlite3.connect('sourceInfo.db')
        sourceData = sourceDB.execute("SELECT * FROM sourceInfo")
        source_folder = ""
        for row in sourceData:
            source_folder = row[1]
        sourceDB.commit()
        sourceDB.close()
        return source_folder
    except :
        return ""

# Function will return the path of the destination folder
def getDest() :
    sourceDB = sqlite3.connect('timeInfo.db')
    tempDay = datetime.datetime.now()
    currentDay = tempDay.strftime("%A")
    tempTime = datetime.datetime.now()
    currentHour = tempTime.hour
    currentMin = tempTime.minute
    # minTime is the variable which will look for the minimum starting time required for starting script
    minTime = 1000000000

    try :
        data = (f"{currentDay}",)
        sql = ''' SELECT * FROM timeInfo
                      WHERE day = ?  
                  '''
        sourceData = sourceDB.execute(sql,data)

        # Below loop will iterate over all the time given by user on that day
        for row in sourceData :
            startingHour = row[1]
            startingMin = row[2]
            endingHour = row[4]
            endingMin = row[5]

            # This if functions are used to convert hours into 24hour format
            if row[3] == "PM" :
                if row[1] == 12 :
                    startingHour = row[1]
                else :
                    startingHour = row[1] + 12
            if row[6] == "PM" :
                if row[4] == 12 :
                    endingHour = row[4]
                else :
                    endingHour = row[4] + 12

            # This is the condition in which we will check if current hour and starting hour will
            # be equal and if there is still time to start loop it will sleep for exactly the same
            # difference
            if currentHour == startingHour :
                if startingMin >= currentMin :
                    diff = startingMin - currentMin
                    print("---------Sleeping for ", 60*diff, "Seconds")
                    time.sleep(60*diff)
                    print("Getting up!!")
                    seconds = getTimeDiff(currentHour, currentMin, endingHour, endingMin)
                    return [row[7],seconds]
                if startingMin < currentMin and currentHour < endingHour :
                    seconds = getTimeDiff(currentHour, currentMin, endingHour, endingMin)
                    return [row[7],seconds]
                if startingMin < currentMin and currentMin < endingMin  :
                    seconds = getTimeDiff(currentHour, currentMin, endingHour, endingMin)
                    return [row[7],seconds]
            if currentHour > startingHour and currentHour < endingHour :
                seconds = getTimeDiff(currentHour, currentMin, endingHour, endingMin)
                return [row[7],seconds]
            if currentHour > startingHour and currentHour == endingHour :
                if currentMin < endingMin :
                    seconds = getTimeDiff(currentHour, currentMin, endingHour, endingMin)
                    return [row[7],seconds]
            if currentHour < startingHour :
                seconds = getTimeDiff(currentHour, currentMin, startingHour, startingMin)
                if seconds < minTime :
                    minTime = seconds
    except:
        print("Probably you didn't added any time right now!!")

    return ["", 0, minTime]


# Still in development phase
def mainFunction() :
    sourceFolder = getSource()
    if sourceFolder == "" :
        time.sleep(2)
        Tk().withdraw()
        messagebox.showerror("Error Message", "You have not Added any Source path, Kindly add it First!!")
        return
    destFolderAndTime = getDest()
    if destFolderAndTime[0] == "" and destFolderAndTime[1] == 0 :
        if not destFolderAndTime[2] ==   1000000000 :
            print("Sleeping for ",destFolderAndTime[2], "Seconds")
            time.sleep(destFolderAndTime[2])
            print("Enough sleeping")
            mainFunction()
    if destFolderAndTime[0] == "":
        time.sleep(0.5)
        Tk().withdraw()
        messagebox.showerror("Error Message", "You have not Added any time for now, Kindly add it First!!")
        return

    print("Calling with ", sourceFolder,destFolderAndTime[0],destFolderAndTime[1])
    mainScript(sourceFolder,destFolderAndTime[0],destFolderAndTime[1])

