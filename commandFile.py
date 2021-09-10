import script as remote
import multiprocessing
from tkinter import messagebox

flag = True

def run():
    global flag
    if flag :
        try:
            global thread
            thread = multiprocessing.Process(target=remote.mainFunction)
            thread.start()
            flag = False
            messagebox.showinfo("Success Message", "You have started Managing Screenshots")
        except Exception as error :
            messagebox.showerror("Error Message", error)
    else :
        messagebox.showerror("Error Message", "You have already started Managing  your screen shots")


def stop():
    global flag
    if not flag :
        try:
            if thread.is_alive() :
                thread.terminate()
            flag = True
            messagebox.showinfo("Success Message", "SuccesFully Stopped Managing ScreenShots")
        except Exception as error :
            messagebox.showerror("Error Message", "You have not started Managing Screenshots yet")
    else :
        messagebox.showerror("Error Message", "You have not started Managing Screenshots yet")

def stopOnClose() :
    try:
        if thread.is_alive():
            thread.terminate()
        return
    except:
        return
