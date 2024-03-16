import time
import tkinter as tk

#Change study minutes to change amount of time
#for pomodoro technique
STUDY_MINUTES = 25 
timeRemaining = 60 * STUDY_MINUTES

#THE FOLLOWING SECTION IS ALL GUI
#initialize window
window = tk.Tk()
window.geometry("640x400")
window.title("Pomodoro")
window.config(bg = '#345')

timeLabel = tk.Label(window, font=("Times New Roman", 20), background="black", foreground="cyan")
timeLabel.place(relx=.5, rely=.5, anchor="center")
timeLabel.config(text = "00:25:00")

#back end of the app
def formatTime(minutes, seconds):
    # Format the time string (00:00)
    if(minutes < 10):
        minuteString = "0" + str(minutes)
    else:
        minuteString = str(minutes)
    
    if(seconds < 10):
        secondString = "0" + str(seconds)
    else:
        secondString = str(seconds)
        
        
    timeString = str(minuteString) + ":" + str(secondString)
    return str(timeString)

def updateTime():
    #global so we can use outside function variables
    global timeRemaining
    
    #recalculate time
    timeRemaining  = timeRemaining - 1
    minutes = timeRemaining // 60
    seconds = timeRemaining % 60
    
    #format the time
    timeString = formatTime(minutes, seconds)
    timeLabel.config(text=timeString)
    
    #update the gui while time > 0
    if(timeRemaining > 0):
        timeLabel.after(1000, updateTime)
    
    
    
    

def gui():
    
    
    updateTime()
    
    window.mainloop()


   



def main():
    gui()

main()
