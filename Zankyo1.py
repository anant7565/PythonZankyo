from tkinter import *
from tkinter import filedialog
import pygame

loop=Tk()

pygame.mixer.init()
def addsongs():
    addedsongs= filedialog.askopenfilenames(initialdir="\Audio",title="Pick Song",filetypes=(("mp3 Files","*.mp3"),))
    for song in addedsongs:
        l=((song.split('/'))[-1]).split('.')
        #s=l[len(l)-1]
        #l=s.split(".")
        playground.insert(END,str(l[0]))

def playsong():
    song = playground.get(ACTIVE)
    song = #song path
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops = 0)

def stopsong():
    pygame.mixer.music.stop()
    playground.selection_clear(ACTIVE)

pause_state = False

def pausesong(is_paused):
    global pause_state
    pause_state = is_paused
    if pause_state:
        pygame.mixer.music.unpause()
        pause_state = False

    else:
        pygame.mixer.music.pause()
        pause_state = True

def nextSong():
    next_song = (playground.curselection())[0] + 1
    song = playground.get(next_song)

    playground.selection_clear(0,END)
    playground.activate(next_song)
    playground.selection_set(next_song, last = None)
    playsong()

def previousSong():
    pre_song = (playground.curselection())[0] - 1
    song = playground.get(pre_song)

    playground.selection_clear(0,END)
    playground.activate(pre_song)
    playground.selection_set(pre_song, last = None)
    playsong()







loop.title("Zankyo Player")
loop.iconbitmap("Graphics/ZankyoIcon2.ico")
loop.geometry("500x400")
loop.configure(bg="#ffb366")

#playlist box
playground=Listbox(loop,bg="#ffcc99",fg="#000000",width=80,bd=5,selectbackground="#ff944d",selectforeground="#000000")
playground.pack(pady=10)

#control buttons
playimg=PhotoImage(file = "Graphics/Playb.png")
pauseimg=PhotoImage(file ="Graphics/Pauseb.png")
nextimg=PhotoImage(file ="Graphics/Nextb.png")
previmg=PhotoImage(file ="Graphics/Prevb.png")
stopimg=PhotoImage(file ="Graphics/Stopb.png")
imagespace=Frame(loop)
imagespace.pack()
playbt=Button(imagespace,image=playimg,borderwidth=0,bg="#ffb366", command=playsong)
pausebt=Button(imagespace,image=pauseimg,borderwidth=0,bg="#ffb366", command=lambda: pausesong(pause_state))
prevbt=Button(imagespace,image=previmg,borderwidth=0,bg="#ffb366", command=previousSong)
nextbt=Button(imagespace,image=nextimg,borderwidth=0,bg="#ffb366", command=nextSong)
stopbt=Button(imagespace,image=stopimg,borderwidth=0,bg="#ffb366", command=stopsong)
prevbt.grid(row=0,column=0)
playbt.grid(row=0,column=1)
pausebt.grid(row=0,column=2)
stopbt.grid(row=0,column=3)
nextbt.grid(row=0,column=4)

menu1=Menu(loop)
loop.config(menu=menu1) # sort of like main menu widget
#For adding songs
dropaddmenu=Menu(menu1) #a menu we need
menu1.add_cascade(label="+Songs",menu=dropaddmenu) #add a cascade menu to the main widget and call it dropadd menu
dropaddmenu.config(bg="#d2a679")
dropaddmenu.add_command(label="Add Songs To The Playlist",command=addsongs)
loop.mainloop()
