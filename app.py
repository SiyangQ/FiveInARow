from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from datetime import datetime
from time import sleep
from threading import Thread
import sys

ROWNUM = 19
KEYS = ("space", "Return")

autoCheckWin = True

round = 0

def UpdateTimerLabel():
    global lblBlackTime, lblWhiteTime, round

    try:
        lblBlackTime.configure(text="Player 1 time remaining：%02d:%02d" % (blackTime // 60, blackTime % 60))
        lblWhiteTime.configure(text="Player 2 time remaining：%02d:%02d" % (whiteTime // 60, whiteTime % 60))
    except Exception as e:
        round += 1

def timer():
    initialRound = round

    global whiteTime, blackTime

    while round == initialRound:
        sleep(1)
        if initialRound%2 == 0: 
            blackTime -= 1
            if (blackTime) <= 0:
                messagebox.showinfo("Player 1's time is over", "Player 1's timer is over. Player 2 WON")
                root.destroy()
        else: 
            whiteTime -= 1
            if (whiteTime) <= 0:
                messagebox.showinfo("Player 2's time is over", "Player 2's timer is over. Player 1 WON")
                root.destroy()
        UpdateTimerLabel()

def startTimer():
    timerThread = Thread(target=timer)
    timerThread.start()

def checkWin(i, j, player):
    # check +x direction
    x = 1
    count = 1
    while buttons[i][j + x]["text"] == player:
        count += 1
        x += 1
    
    x = -1
    while buttons[i][j + x]["text"] == player:
        count += 1
        x -= 1
    
    if count >= 5:
        if player == "b": messagebox.showinfo("Game Over", "Player 1 WON")
        else:messagebox.showinfo("Game Over", "Player 2 WON")
        root.destroy()

    # check +y direction
    x = 1
    count = 1
    while buttons[i + x][j]["text"] == player:
        count += 1
        x += 1
    
    x = -1
    while buttons[i + x][j]["text"] == player:
        count += 1
        x -= 1
    
    if count >= 5:
        if player == "b": messagebox.showinfo("Game Over", "Player 1 WON")
        else:messagebox.showinfo("Game Over", "Player 2 WON")
        root.destroy()

    # check +x+y direction
    x = 1
    count = 1
    while buttons[i + x][j + x]["text"] == player:
        count += 1
        x += 1
    
    x = -1
    while buttons[i + x][j + x]["text"] == player:
        count += 1
        x -= 1
    
    if count >= 5:
        if player == "b": messagebox.showinfo("Game Over", "Player 1 WON")
        else:messagebox.showinfo("Game Over", "Player 2 WON")
        root.destroy()

    # check +x-y direction
    x = 1
    count = 1
    while buttons[i - x][j + x]["text"] == player:
        count += 1
        x += 1
    
    x = -1
    while buttons[i - x][j + x]["text"] == player:
        count += 1
        x -= 1
    
    if count >= 5:
        if player == "b": messagebox.showinfo("Game Over", "Player 1 WON")
        else:messagebox.showinfo("Game Over", "Player 2 WON")
        root.destroy()
    
def endTurn():
    global round
    round += 1

def buttonClicked(location):

    coor = int(location)
    i = coor // ROWNUM
    j = coor % ROWNUM

    if round%2 == 0:
        buttons[i][j].configure(image=blackImg, state=DISABLED, text="b")
        if autoCheckWin: checkWin(i, j, "b")
    else: 
        buttons[i][j].configure(image=whiteImg, state=DISABLED, text="w")
        if autoCheckWin: checkWin(i, j, "w")
    
    endTurn()
    startTimer()

def createButton(window, buttonImg):
    newButton = Button(window, image=buttonImg, bg="gray70", activebackground="gray70", borderwidth=0, command=lambda: buttonClicked(newButton["text"]))
    return newButton

def drawBoard(window, normalImg, dotImage):
    buttons = []
    for i in range(ROWNUM):
        row = []
        for j in range(ROWNUM):
            if (i == 3 or i == 9 or i == 15) and (j == 3 or j == 9 or j == 15): img = dotImage
            else: img = normalImg
            newButton = createButton(window, img)
            newButton.configure(text = str(i*ROWNUM + j))
            newButton.grid(row=i, column=j)
            row.append(newButton)
        buttons.append(row)
    return buttons

def redrawBoard(window, normalImg, dotImage):
    global buttons
    for row in buttons:
        for button in row:
            button.grid_forget()
    buttons.clear()
    return drawBoard(window, normalImg, dotImg)

def settings():
    top = Toplevel()
    top.title("Settings")
    top.iconbitmap("res/icon.ico")

    Label(top, text="Player 1 turn end:").grid(row=0, column=0, pady=(10,0), padx=10)
    EtyBlack = Entry(top, width=15)
    EtyBlack.grid(row=0, column=1, pady=(10,0), padx=10)
    EtyBlack.insert(0, "space")
    Label(top, text="Player 2 turn end:").grid(row=1, column=0, pady=(10,0), padx=10)
    EtyWhite = Entry(top, text="Return", width=15)
    EtyWhite.grid(row=1, column=1, pady=(10,0), padx=10)
    EtyWhite.insert(0, "Return")
    Button(top, text="Confirm", command=top.destroy).grid(row=2, column=0, columnspan=2,pady=10, padx=10)

def startGame():
    startTimer()

def forfeit():
    root.destroy()

def blackEndTurnPressed():
    if round%2 != 0: return

def whiteEndTurnPressed():
    if round%2 == 0: return

root = Tk()
root.title("Five in a Row")
root.iconbitmap("res/icon.ico")
root.resizable(0,0)

root.bind("<space>", blackEndTurnPressed)
root.bind("<Return>", whiteEndTurnPressed)

board = LabelFrame(root, padx = 10, pady = 10)
board.grid(row = 1, column = 0,padx = 10, pady = 10)

# images
normalImg = ImageTk.PhotoImage(Image.open("res/unoccupied.png"))
dotImg = ImageTk.PhotoImage(Image.open("res/dot.png"))
blackImg = ImageTk.PhotoImage(Image.open("res/black.png"))
whiteImg = ImageTk.PhotoImage(Image.open("res/white.png"))

# draw board
buttons = drawBoard(board, normalImg, dotImg)

# top info bar
infoFrame = LabelFrame(root, padx=10, pady = 10)
infoFrame.grid(row=0, column=0)

Button(infoFrame, text="Settings", command=settings).grid(row=0, column=0, padx=5)
Button(infoFrame, text="Start", command=startGame).grid(row=0, column=2, padx=5)
Button(infoFrame, text="Forfeit", command=forfeit).grid(row=0, column=4, padx=5)

# timer setup
blackTime = 1*60
whiteTime = 1*60
lblBlackTime = Label(infoFrame, text="Player 1 time remaining：%02d:%02d" % (blackTime // 60, blackTime % 60))
lblBlackTime.grid(row=0, column=1, padx=5)
lblWhiteTime = Label(infoFrame, text="Player 2 time remaining：%02d:%02d" % (whiteTime // 60, whiteTime % 60))
lblWhiteTime.grid(row=0, column=3, padx=5)

root.mainloop()