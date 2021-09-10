import sqlite3
import datetime
from tkinter import messagebox

# This function will time span of any lecture
def getTime(startingHr, startingMin) :
    s1 = str(startingHr) + ":" + str(startingMin) + ":00"
    FMT = '%H:%M:%S'
    return datetime.datetime.strptime(s1, FMT)


# This function's main task is to put source file data into database
def addSourceData(sourcePath) :
    conn = sqlite3.connect('sourceInfo.db')
    # Below cursor is for checking purpose if table is created or not
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sourceInfo'")
    flag = True
    for row in cursor :
        flag = False
        break
    if flag :
        # This will create the table and will add the first entry to it
        data = (1,f"{sourcePath}")
        conn.execute("CREATE TABLE sourceInfo (ID INT, sourcePath TEXT)")
        conn.execute("INSERT INTO sourceInfo (ID, sourcePath) VALUES(?,?)",data)
    else:
        # This will update row with id 1
        data = (f"{sourcePath}",1)
        sql = ''' UPDATE sourceInfo
              SET sourcePath = ?
              WHERE ID = ?'''
        conn.execute(sql,data)
    conn.commit()
    conn.close()


# This function will check that whether you are entering correct time or you are conflicting some lectures
def checkAvailability(row,startingHr, startingMin, startingFrame, endingHr, endingMin, endingFrame):
    flag = True
    if startingFrame == "PM":
        if startingHr == 12:
            startingHr = startingHr
        else:
            startingHr = startingHr + 12
    if endingFrame == "PM":
        if endingHr == 12:
            endingHr = endingHr
        else:
            endingHr = endingHr + 12

    tempStart = row[1]
    tempEnd = row[4]
    if row[3] == "PM" :
        if row[1] == 12 :
            tempStart = row[1]
        else :
            tempStart = row[1] + 12
    if row[6] == "PM" :
        if row[4] == 12 :
            tempEnd = row[4]
        else :
            tempEnd = row[4] + 12
    startingTime = getTime(startingHr,startingMin)
    endingTime = getTime(endingHr, endingMin)
    tempStartingTime = getTime(tempStart,row[2])
    tempEndingTime = getTime(tempEnd,row[5])

    if startingTime >= tempStartingTime and endingTime <= tempEndingTime :
        flag = False
        return flag

    return flag

# This function will store time data passed from the form
def addTimeData(day,initialHr,initialMin,endingHr,endingMin,destPath, startFrame, endFrame) :
    conn = sqlite3.connect('timeInfo.db')
    # Below cursor is for checking purpose if table is created or not
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='timeInfo'")
    flag = True
    for row in cursor:
        flag = False
        break
    if flag:
        # It will create the database and also enter the data into database if table is not already created
        createSql = '''CREATE TABLE timeInfo 
                (day TEXT, 
                 initialHr INT,
                 initialMin INT,
                 startFrame TEXT,
                 endingHr INT,
                 endingMin INT,
                 endFrame TEXT,
                 destPath TEXT
                )
                '''
        conn.execute(createSql)
        data = (day, initialHr, initialMin, startFrame, endingHr, endingMin,  endFrame, destPath)
        insertSql = '''INSERT INTO timeInfo
                        (day, initialHr, initialMin, startFrame, endingHr, endingMin,  endFrame, destPath)
                        VALUES(?,?,?,?,?,?,?,?)                        
                        '''
        conn.execute(insertSql,data)
    else:
        # It will make entry to the created database
        tempData = (day,)
        checkSql = ''' SELECT * FROM timeInfo
                       WHERE day = ? 
                        '''
        cursor = conn.execute(checkSql,tempData)
        checkFlag = True
        for row in cursor :
            if row[1] == initialHr and row[2] == initialMin and row[3] == startFrame and row[4] == endingHr and row[5] == endingMin and row[6] == endFrame :
                checkFlag = False
                messagebox.showinfo("Error Message", "You have already added this time")
                break
            if not checkAvailability(row,initialHr, initialMin, startFrame, endingHr, endingMin, endFrame) :
                checkFlag = False
                messagebox.showinfo("Error Message", "You are Trying to mixup two lecture")
                break

        if checkFlag :
            data = (day, initialHr, initialMin, startFrame, endingHr, endingMin, endFrame, destPath)
            insertSql = '''INSERT INTO timeInfo
                                    (day, initialHr, initialMin, startFrame, endingHr, endingMin,  endFrame, destPath)
                                    VALUES(?,?,?,?,?,?,?,?)                        
                                    '''
            conn.execute(insertSql, data)
    conn.commit()
    conn.close()

def getTiming():
    conn = sqlite3.connect('timeInfo.db')
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='timeInfo'")
    flag = True
    for row in cursor:
        flag = False
        break
    if not flag :
        checkSql = " SELECT * FROM timeInfo"
        cursor = conn.execute(checkSql)
        return cursor
    else:
        conn.commit()
        conn.close()
        return None

def deleteData(day,startingHr,startingMin, startingFrame, endingHr, endingMin, endingFrame):
    conn = sqlite3.connect('timeInfo.db')
    deleteSql = '''DELETE FROM timeInfo
                   Where day = ? and initialHr = ? and initialMin = ? and startFrame = ? 
                    and endingHr = ? and endingMin = ? and endFrame = ?    
                '''
    data = (day,startingHr,startingMin, startingFrame, endingHr, endingMin, endingFrame)
    try :
        conn.execute(deleteSql,data)
    except Exception as e :
        print("ERROR !!!", e)
    conn.commit()
    conn.close()

