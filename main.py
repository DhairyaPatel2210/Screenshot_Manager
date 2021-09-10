from tkinter import *
from tkinter.ttk import *
import commandFile as cf
import dbManager as db
from functools import partial
from multiprocessing import freeze_support
freeze_support()


# This is the second screen where i will ask to go into addition
# of source path or adding time data
def addDataScreen():
    frame = Frame(root,width=980, height=540)
    addSourceButton = Button(frame, text='Add Source Path', style="TButton", command=lambda : deletingFrame(frame,"addDataScreen","addSource"))
    addTimeButton  = Button(frame, text='Add Time', style="TButton", command=lambda : deletingFrame(frame,"addDataScreen","addTime"))
    backButton = Button(frame, text='Back', style="TButton",command = lambda : deletingFrame(frame,"addDataScreen","home"))
    addSourceButton.place(relx=0.5,rely=0.4, anchor='center')
    addTimeButton.place(relx=0.5,rely=0.5, anchor='center')
    backButton.place(relx=0.5,rely=0.6, anchor='center')
    frame.pack(fill=None, expand=False)

# This function will be called when user click on submit button from addSource screen
def submitFunc(source_entry,frame, comingScreen) :
    db.addSourceData(source_entry.get())
    reset(frame, comingScreen)


# This function will be called when user click on submit button from addTime screen
def submitTimeFunc(initialTextOnMenu,initialNumber,initialNumber2,initialNumber3,initialNumber4,source_entry,initial,ending,frame,comingScreen) :
    db.addTimeData(initialTextOnMenu.get(), initialNumber.get(),
                   initialNumber2.get(), initialNumber3.get(), initialNumber4.get(), source_entry.get(), initial.get(),
                   ending.get())
    reset(frame, comingScreen)


# This is the screen where it will ask to enter source data
def addSource():
    frame = Frame(root, width=980, height=540)
    label = Label(frame, text='Add Source Path',  font=('verdana', 16, 'bold'))
    backButton = Button(frame, text='Back', style="TButton", command=lambda: deletingFrame(frame, "addSource","addDataScreen"))
    source_entry = Entry(frame, width=23, font="MontSerrat 14 bold", textvariable = StringVar )
    submitButton = Button(frame, text='Submit', style="TButton", command= lambda : submitFunc(source_entry,frame,"addSource"))
    resetButton = Button(frame, text='Reset', style="TButton", command=lambda: reset(frame, "addSource"))
    source_entry.place(relx=0.6, rely =0.5, anchor='center')
    label.place(relx=0.35, rely=0.5, anchor='center')
    submitButton.place(relx=0.65, rely=0.6, anchor='center')
    resetButton.place(relx=0.45, rely=0.6, anchor='center')
    backButton.place(relx=0.25, rely=0.6, anchor='center')
    frame.pack(fill=None, expand=False)


# This function is used to reset the data that is typed in the form
def reset(frame, comingScreen) :
    frame.pack_forget()
    if comingScreen == "addSource" :
        addSource()
    elif comingScreen == "addTime" :
        addTime()


# This fucntion is used to create frame for the form where user will enter
# Time, Day and folder path details
def addTime() :
    dayOptions = ["","Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    timeOption = [1,2,3,4,5,6,7,8,9,10,11,12]
    timeFrameOption = ["","AM", "PM"]
    minuteOption = []
    for time in range(61):
        minuteOption.append(time)
    frame = Frame(root, width=980, height=540)
    dayLabel = Label(frame, text='Day',  font=('verdana', 16, 'bold'))
    timeLabel = Label(frame, text='Time', font=('verdana', 16, 'bold'))
    toLabel = Label(frame, text='To', font=('verdana', 16, 'bold'))
    # ================ Dropdown of days ===============
    initialTextOnMenu = StringVar()
    initialTextOnMenu.set("Monday")
    dayDropdown = OptionMenu( frame , initialTextOnMenu , *dayOptions)
    # ================ Dropdown of startingHour ===============
    initialNumber = IntVar()
    initialNumber.set(1)
    timeDropDown = OptionMenu( frame , initialNumber , *timeOption)
    # ================ Dropdown of startingMinute ===============
    initialNumber2 = IntVar()
    initialNumber2.set(1)
    minuteDropDown = OptionMenu(frame, initialNumber2, *minuteOption)
    # ================ Dropdown of AM-PM ===============
    initial = StringVar()
    initial.set("AM")
    initialFrame = OptionMenu(frame, initial, *timeFrameOption)
    # ================ Dropdown of endingHour ===============
    initialNumber3 = IntVar()
    initialNumber3.set(1)
    timeDropDown2 = OptionMenu( frame , initialNumber3 , *timeOption)
    # ================ Dropdown of endingMinute ===============
    initialNumber4 = IntVar()
    initialNumber4.set(1)
    minuteDropDown2 = OptionMenu(frame, initialNumber4, *minuteOption)
    # ================ Dropdown of AM-PM ===============
    ending = StringVar()
    ending.set("AM")
    endingFrame = OptionMenu(frame, ending, *timeFrameOption)
    # ================ Source Section ===============
    sourceLabel = Label(frame, text='Add Folder Path', font=('verdana', 16, 'bold'))
    source_entry = Entry(frame, width=23, font="MontSerrat 14 bold", textvariable=StringVar)
    # ================ Submit and Back button ===============
    submitButton = Button(frame, text='Submit', style="TButton", command=lambda: submitTimeFunc(initialTextOnMenu,
                        initialNumber,initialNumber2,initialNumber3,initialNumber4,source_entry,initial,ending,frame,"addTime"))
    backButton = Button(frame, text='Back', style="TButton",command=lambda: deletingFrame(frame, "addTime", "addDataScreen"))
    # ================ Reset Button ===============
    resetButton = Button(frame, text='Reset', style="TButton",command=lambda: reset(frame, "addTime"))
    # ================ Placement of each setion ===============
    dayLabel.place(relx=0.3, rely=0.35, anchor='center')
    dayDropdown.place(relx=0.42, rely=0.35, anchor='center')
    timeLabel.place(relx=0.3, rely=0.45, anchor='center')

    timeDropDown.place(relx=0.4, rely=0.45, anchor='center')
    minuteDropDown.place(relx=0.45, rely=0.45, anchor='center')
    initialFrame.place(relx=0.5,rely=0.45,anchor='center')
    toLabel.place(relx=0.55, rely=0.45, anchor='center')
    timeDropDown2.place(relx=0.6, rely=0.45, anchor='center')
    minuteDropDown2.place(relx=0.65, rely=0.45, anchor='center')
    endingFrame.place(relx=0.7, rely=0.45, anchor='center')
    sourceLabel.place(relx=0.235, rely=0.55, anchor='center')
    source_entry.place(relx=0.52, rely=0.55, anchor='center')
    submitButton.place(relx=0.65,rely=0.7,anchor='center')
    resetButton.place(relx=0.45,rely=0.7,anchor='center')
    backButton.place(relx=0.25,rely=0.7,anchor='center')
    # ================ Packing Of Frame ===============
    frame.pack(fill= None, expand=False)

# This function is specifically created to change frames,
# and to change frames we need to delete previous frames so
# this function will do the same.
def deletingFrame(frame,comingScreenName,goingScreenName):
    frame.pack_forget()
    if comingScreenName == "addDataScreen" and goingScreenName == "home":
        mainPage()
    elif comingScreenName == "addSource" and goingScreenName == "addDataScreen":
        addDataScreen()
    elif comingScreenName == "addDataScreen" and goingScreenName == "addSource":
        addSource()
    elif comingScreenName == "addTime" and goingScreenName == "addDataScreen" :
        addDataScreen()
    elif comingScreenName == "addDataScreen"  and goingScreenName == "addTime" :
        addTime()
    elif comingScreenName == "deleteScreen" and goingScreenName == "home" :
        mainPage()
    elif comingScreenName == "deleteScreen" and goingScreenName == "deleteScreen" :
        deleteScreen()


# This function will be called when close button will be called
def closeClick():
    cf.stopOnClose()
    root.destroy()


# This function will delete the data from the database and then it will callback deletescreen
def dltData(i) :
    row = timeList[i]
    day, startingHr, startingMin, startingFrame, endingHr, endingMin, endingFrame, frame = row
    db.deleteData(day,startingHr,startingMin, startingFrame, endingHr, endingMin, endingFrame)
    deletingFrame(frame, "deleteScreen", "deleteScreen")


# This function is screen used to delete the data from database
def deleteScreen() :
    frame = Frame(root)
    frame.pack(fill=BOTH, expand=1)
    my_canvas = Canvas(frame)
    my_canvas.pack(fill=BOTH, side=LEFT, expand=1)

    my_scrollbar = Scrollbar(frame, command=my_canvas.yview, orient=VERTICAL)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))

    second_frame = Frame(my_canvas)
    my_canvas.create_window((0, 0), window=second_frame, anchor='nw')
    Label(second_frame, text='Day', font=('verdana', 16, 'bold')).grid(row=0,column=0,padx=50)
    Label(second_frame, text='Time', font=('verdana', 16, 'bold')).grid(row=0,column=1,padx=250)
    Button(second_frame, text='Back', style="TButton",
           command=lambda: deletingFrame(frame, "deleteScreen", "home")).grid(row=0,column=2,padx=50)

    times = db.getTiming()
    if times != None :
        i=0
        global timeList
        timeList = []
        flag = True
        for row in times :
            flag = False
            day = row[0]
            time = str(row[1]) + ":" +str(row[2]) + " " +row[3] + " TO " + str(row[4]) +  ":" + str(row[5]) + " " + row[6]
            Label(second_frame, text=day, font=('verdana', 12, 'bold')).grid(row=(i+2),column=0,pady=10)
            Label(second_frame, text=time, font=('verdana', 12, 'bold')).grid(row=(i+2),column=1,pady=10)
            alltimingData = [row[0],row[1],row[2],row[3],row[4],row[5],row[6],frame]
            timeList.append(alltimingData)
            Button(second_frame,text='DELETE',command= partial(dltData,i)).grid(row=(i+2),column=2,pady=10)
            i+=1
        if flag :
            Label(second_frame, text='Nothing in there!!', font=('verdana', 16, 'bold')).grid(row=2, column=1, pady=10)
    else :
        Label(second_frame, text='Nothing in there!!', font=('verdana', 16, 'bold')).grid(row=2,column=1,pady=10)

# This function will bring back you to the main screen
def mainPage() :
    style = Style()
    style.configure('TButton', font=('verdana', 16, 'bold'))
    stop_button = Button(root, text='Stop Running ', style='TButton', command=cf.stop)
    start_button = Button(root, text='Start Managing Screen Shots', command=cf.run)
    add_button = Button(root, text="Add Timing to Manage Screen Shots", command= lambda : addDataScreen())
    close_button = Button(root, text="Close App", command=closeClick)
    delete_data_button = Button(root, text="Delete Timing", command=deleteScreen)
    start_button.place(relx=0.5, rely=0.3, anchor='center')
    add_button.place(relx=0.5, rely=0.4, anchor='center')
    stop_button.place(relx=0.5, rely=0.5, anchor='center')
    delete_data_button.place(relx=0.5, rely=0.6, anchor='center')
    close_button.place(relx=0.5, rely=0.7, anchor='center')

# Initialisation of Application
if __name__ == '__main__' :
    root = Tk()
    root.title("ScreenShots Manager")
    root.geometry('980x540')
    root.minsize(980, 540)
    root.maxsize(980, 540)
    photo = PhotoImage(file="./Images/logo.png")
    root.iconphoto(False, photo)
    mainPage()
    root.mainloop()
