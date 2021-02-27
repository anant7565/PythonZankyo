from tkinter import *
from tkinter import filedialog
import pygame
import random

loop=Tk()

pause_state = False
shuffle_state = [False, []]

def addsongs():
    addedsongs= filedialog.askopenfilenames(initialdir="\Audio",title="Pick Song",filetypes=(("mp3 Files","*.mp3"),))
    for song in addedsongs:
        l=((song.split('/'))[-1]).split('.')
        playground.insert(END,str(l[0]))

def playsong():
    song = playground.get(ACTIVE)
    playground.selection_set(ACTIVE, last = None)
    song = '/Users/pramodkhandelwal/github/PythonZankyo/Audio/' + song + '.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops = 0)

def stopsong():
    pygame.mixer.music.stop()
    playground.selection_clear(ACTIVE)
    playground.activate(0)



def pausesong():
    global pause_state

    if pause_state:
        pygame.mixer.music.unpause()
        pause_state = False

    else:
        pygame.mixer.music.pause()
        pause_state = True

def nextSong():

        next_song = (playground.curselection())[0] + 1
        x = playground.size()
        if next_song == x:
            next_song = 0


        playground.selection_clear(0,END)
        playground.activate(next_song)
        playground.selection_set(next_song, last = None)
        playsong()

def previousSong():
    pre_song = (playground.curselection())[0] - 1
    if pre_song == -1:
        pre_song = playground.size() - 1


    playground.selection_clear(0,END)
    playground.activate(pre_song)
    playground.selection_set(pre_song, last = None)
    playsong()

def randomSongs():
    l = list(range(playground.size()))

    random.shuffle(l)
    return l


def shuffle():
    global shuffle_state
    if shuffle_state[0]:
        shufbt.config(text = "Shuffle and relax")
        playbt["state"] = "normal"
        pausebt["state"] = "normal"
        prevbt["state"] = "normal"
        nextbt["state"] = "normal"
        stopbt["state"] = "normal"
        shuffle_state[0],shuffle_state[1] = False,[]
        stopsong()

    else :
        shuffle_state[0], shuffle_state[1] = True, randomSongs()
        shufbt.config(text = "Manual mode")
        playbt["state"] = "disabled"
        pausebt["state"] = "disabled"
        prevbt["state"] = "disabled"
        nextbt["state"] = "disabled"
        stopbt["state"] = "disabled"

        playinLoop(shuffle_state[1])


def playinLoop(songslist):
    for i in songslist:
        playground.selection_clear(0,END)
        playground.activate(i)
        playground.selection_set(i, last = None)
        playsong()


def Rem1():
    playground.delete(playground.curselection()[0])
    pygame.mixer.music.stop()

def Clearplaylist():
    playground.delete(0,END)
    pygame.mixer.music.stop()

def Themesetter(loop,playground,playbt,pausebt,nextbt,prevbt,stopbt,colscheme):
    if colscheme=="MONOCHROME":
        loop.configure(bg="#454545")
        playground.config(bg="#999999",fg="#ffffff",selectbackground="#707070",selectforeground="#ffffff")
        playbt.config(bg="#999999")
        pausebt.config(bg="#999999")
        prevbt.config(bg="#999999")
        nextbt.config(bg="#999999")
        stopbt.config(bg="#999999")

    if colscheme=="Glacier":
        loop.configure(bg="#20c3d0")
        playground.config(bg="#b9e8ea",fg="#000000",selectbackground="#86d6d8",selectforeground="#000000")
        playbt.config(bg="#20c3d0")
        pausebt.config(bg="#20c3d0")
        prevbt.config(bg="#20c3d0")
        nextbt.config(bg="#20c3d0")
        stopbt.config(bg="#20c3d0")

    if colscheme=="Autumn Leaves" :
        loop.configure(bg="#98482b")
        playground.config(bg="#a64b29",fg="#ffffff",selectbackground="#853619",selectforeground="#ffffff")
        playbt.config(bg="#98482b")
        pausebt.config(bg="#98482b")
        prevbt.config(bg="#98482b")
        nextbt.config(bg="#98482b")
        stopbt.config(bg="#98482b")

    if colscheme=="Spring" :
        loop.configure(bg="#54862e")
        playground.config(bg="#9ac37b",fg="#ffffff",selectbackground="#72a24e",selectforeground="#ffffff")
        playbt.config(bg="#54862e")
        pausebt.config(bg="#54862e")
        prevbt.config(bg="#54862e")
        nextbt.config(bg="#54862e")
        stopbt.config(bg="#54862e")

    if colscheme=="Summer" :
        loop.configure(bg="#F3872F")
        playground.config(bg="#ffcc99",fg="#000000",selectbackground="#ff944d",selectforeground="#000000")
        playbt.config(bg="#F3872F")
        pausebt.config(bg="#F3872F")
        prevbt.config(bg="#F3872F")
        nextbt.config(bg="#F3872F")
        stopbt.config(bg="#")







loop.title("Zankyo Player")
loop.iconbitmap("Graphics/ZankyoIcon2.ico")
loop.geometry("500x400")
loop.configure(bg="#F3872F")
playground=Listbox(loop,bg='#ffcc99',fg="#000000",width=80,bd=5,selectbackground="#ff944d",selectforeground="#000000")
playground.pack(pady=10)
pygame.mixer.init()
playimg=PhotoImage(file="Graphics/Playb.png")
pauseimg=PhotoImage(file="Graphics/Pauseb.png")
nextimg=PhotoImage(file="Graphics/Nextb.png")
previmg=PhotoImage(file="Graphics/Prevb.png")
stopimg=PhotoImage(file="Graphics/Stopb.png")

imagespace=Frame(loop)
imagespace.pack()
playbt=Button(imagespace,image=playimg,borderwidth=0,bg="#F3872F",command=playsong)
pausebt=Button(imagespace,image=pauseimg,borderwidth=0,bg="#F3872F",command=pausesong)
prevbt=Button(imagespace,image=previmg,borderwidth=0,bg="#F3872F",command=previousSong)
nextbt=Button(imagespace,image=nextimg,borderwidth=0,bg="#F3872F",command=nextSong)
stopbt=Button(imagespace,image=stopimg,borderwidth=0,bg="#F3872F",command=stopsong)
shufbt=Button(imagespace,text = "Shuffle and relax",borderwidth=0,bg="#F3872F",command=shuffle)
prevbt.grid(row=0,column=0)
playbt.grid(row=0,column=1)
pausebt.grid(row=0,column=2)
stopbt.grid(row=0,column=3)
nextbt.grid(row=0,column=4)
shufbt.grid(row=0,column=5)

menu1=Menu(loop)
loop.config(menu=menu1) # sort of like main menu widget
#For adding songs
dropaddmenu=Menu(menu1) #a menu we need
menu1.add_cascade(label="+Songs",menu=dropaddmenu) #add a cascade menu to the main widget and call it dropadd menu
dropaddmenu.config(bg="#ffffff")
dropaddmenu.add_command(label="Add songs To The Playlist",command=addsongs)

dropremovemenu=Menu(menu1)
menu1.add_cascade(label= "-Songs",menu=dropremovemenu)
dropremovemenu.add_command(label="Remove Song",command=Rem1)
dropremovemenu.add_command(label="Clear Playlist",command=Clearplaylist)
dropremovemenu.config(bg="#ffffff")

Themes=Menu(menu1)
menu1.add_cascade(label= "Themes",menu=Themes)
Themes.add_command(label="Monochrome",command = lambda: Themesetter(loop,playground,playbt,pausebt,nextbt,prevbt,stopbt,"MONOCHROME"))
Themes.config(bg="#ffffff")
Themes.add_command(label="Glacier",command=lambda: Themesetter(loop,playground,playbt,pausebt,nextbt,prevbt,stopbt,"Glacier"))
Themes.add_command(label="Autumn Leaves",command=lambda: Themesetter(loop,playground,playbt,pausebt,nextbt,prevbt,stopbt,"Autumn Leaves"))
Themes.add_command(label="Spring",command=lambda: Themesetter(loop,playground,playbt,pausebt,nextbt,prevbt,stopbt,"Spring"))
Themes.add_command(label="Summer",command=lambda: Themesetter(loop,playground,playbt,pausebt,nextbt,prevbt,stopbt,"Summer"))
loop.mainloop()
