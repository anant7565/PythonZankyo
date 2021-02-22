from tkinter import *
from tkinter import filedialog
import pygame

loop=Tk()
def addsong():
    addedsong= filedialog.askopenfilename(initialdir="\Audio",title="Pick Song",filetypes=(("mp3 Files","*.mp3"),))
    l=addedsong.split('/')
    s=l[len(l)-1]
    l=s.split(".")
    playground.insert(END,str(l[0]))


loop.title("Zankyo Player")
loop.iconbitmap("Graphics\\ZankyoIcon2.ico")
loop.geometry("500x400")
loop.configure(bg="#ffb366")
playground=Listbox(loop,bg="#ffcc99",fg="#000000",width=80,bd=5,selectbackground="#ff944d",selectforeground="#000000")
playground.pack(pady=10)
pygame.mixer.init()
playimg=PhotoImage(file="Graphics\\Playb.png")
pauseimg=PhotoImage(file="Graphics\\Pauseb.png")
nextimg=PhotoImage(file="Graphics\\Nextb.png")
previmg=PhotoImage(file="Graphics\\Prevb.png")
stopimg=PhotoImage(file="Graphics\\Stopb.png")
imagespace=Frame(loop)
imagespace.pack()
playbt=Button(imagespace,image=playimg,borderwidth=0,bg="#ffb366")
pausebt=Button(imagespace,image=pauseimg,borderwidth=0,bg="#ffb366")
prevbt=Button(imagespace,image=previmg,borderwidth=0,bg="#ffb366")
nextbt=Button(imagespace,image=nextimg,borderwidth=0,bg="#ffb366")
stopbt=Button(imagespace,image=stopimg,borderwidth=0,bg="#ffb366")
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
dropaddmenu.add_command(label="Add A Song To The Playlist",command=addsong)
loop.mainloop()
