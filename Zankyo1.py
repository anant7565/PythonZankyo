
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import requests
import pygame
import random
from tkinter.messagebox import showinfo
from lyrics_extractor import SongLyrics
from requests.exceptions import Timeout
import pymongo
import json
import urllib
import base64
from io import BytesIO
from PIL import ImageTk, Image
from mutagen.mp3 import MP3

CLIENT_ID = 'eab56b94c3e8449794b46717080609b9'
CLIENT_SECRET = 'bd23f78d31fb4c7bbdda106db8484151'

AUTH_URL = 'https://accounts.spotify.com/api/token'


auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})


auth_response_data = auth_response.json()


access_token = auth_response_data['access_token']


headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}
BASE_URL = 'https://api.spotify.com/v1/search/'


loop=Tk()

myclt = pymongo.MongoClient("localhost",27017)
mydb = myclt["music"]
col = mydb["users"]
pause_state = False
shuffle_state = [False, []]




def getuser(name):
    if not name:
        showinfo("Window", "Enter name")
        name_entry.delete(0,END)
        return

    query = {"name": name}
    if not col.count_documents(query):
        showinfo("Window", "User not found")
        name_entry.delete(0,END)
        return
    details = col.find(query)
    userplaylist = []
    for i in details:
        userplaylist.extend(i['myplaylist'])
    Clearplaylist()
    for song in userplaylist:
        playground.insert(END,str(song))

def updateuser(name):
    if not name:
        showinfo("Window", "Enter name")
        name_entry.delete(0,END)
        return
    filter = {'name':name}
    if not col.count_documents(filter):
        showinfo("Window", "User not found")
        name_entry.delete(0,END)
        return
    userplaylist = list(playground.get(0,END))
    query = { "$set" : {"myplaylist": userplaylist}}
    col.update_one(filter, query)

def storeuser(name):
    if not name:
        showinfo("Window", "Enter name")
        name_entry.delete(0,END)
        return
    query = {"name": name}
    if col.count_documents(query):
        showinfo("Window", "User already exists")
        name_entry.delete(0,END)
        return
    userplaylist = list(playground.get(0,END))
    if not userplaylist:
        showinfo("Window", "Please provide atlease one song")
        name_entry.delete(0,END)
        return

    user = {"name": name, "myplaylist": userplaylist }
    x = col.insert_one(user)



def onselect(evt):

    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    e2.delete(0,END)
    e2.insert(END,value)

songlen=0
currpos=0

def addsongs():
    addedsongs= filedialog.askopenfilenames(initialdir="/Audio",title="Pick Song",filetypes=(("mp3 Files","*.mp3"),))
    for song in addedsongs:
        l=((song.split('/'))[-1]).split('.')
        playground.insert(END,str(l[0]))

shiftit=0
def playsong():
    global pause_state 
    global songlen
    global currpos
    global shiftit
    if(pause_state):  
        pygame.mixer.music.unpause()
        pause_state=False
    else:  
        song = playground.get(ACTIVE)
        song = f'C:\\Users\\Shreyansh\\Desktop\\SnekPirojekt\\PythonZankyo\\Audio\\{song}.mp3'
        pygame.mixer.music.load(song)
        thissong=MP3(song)
        songlen=int(thissong.info.length)
        m1,s1=divmod(songlen,60)
        if s1>=10:
            lentime.config(text=f'{m1}:{s1}')
        else:
            lentime.config(text=f'{m1}:0{s1}')
        def timemysong():
            
            currpos=int(pygame.mixer.music.get_pos()/1000)
            shiftit=currpos/songlen*100
            timescrub.configure(value=shiftit)
            m2,s2=divmod(currpos,60)
            
            postime.config(text=f'{m2}:{s2}')
            if(currpos==songlen):
                stopsong()
            postime.after(1000,timemysong)
        
        timemysong()
        pygame.mixer.music.play(loops = 0)

def stopsong():
    pygame.mixer.music.stop()
    playground.selection_clear(ACTIVE)
    e2.delete(0,END)
    playground.activate(0)
    

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

def popup_showinfo(message):
    showinfo("Window", message)


def printlyrics(code,arr,song = 'NO LYRICS FOUND'):
    win =Toplevel()
    win.geometry("1500x500")
    win.wm_title('Window')
    T = Text(win)
    S = Scrollbar(win,command=T.yview)

    T.config(yscrollcommand=S.set)

    T.pack(side = LEFT)

    T.insert(END, song)



    URL = arr[0]

    response = requests.get(URL)

    im = Image.open(BytesIO(response.content))
    photo = ImageTk.PhotoImage(im)

    label = Label(win,image=photo)
    label.image = photo
    label.pack()

    Label(win, text = arr[1]).pack()

    Label(win, text = arr[2]).pack()
    Label(win, text = arr[3]).pack()
    Label(win, text = 'Top albums by the artist').pack()
    for i in range(len(arr[4])):
        Label(win, text = arr[4][i]).pack()




def getlyrics(song):

    if (not song):
        popup_showinfo('Please fill the information')
        return

    e2.delete(0,END)
    extract_lyrics = SongLyrics("AIzaSyB_2KRVPtP7AxWwTxKC4C9UecXbQTMASr4","1bf00c72a4acb9c4a")

    song = song
    spotify = requests.get(BASE_URL,params={'q': song, 'limit': 1, 'type': 'track'}, headers=headers)
    spotify_response = spotify.json()
    itunes = 'https://itunes.apple.com/search?term='+ song +'&limit=1'
    itunes_response= requests.get(itunes).json()
    artist_image = spotify_response['tracks']['items'][0]['album']['images'][1]["url"]

    c = 'https://itunes.apple.com/lookup?id='+str(itunes_response['results'][0]["artistId"])+'&entity=album'
    d= requests.get(c).json()

    artist_name = itunes_response['results'][0]['artistName']
    a_sl ='Top tracks on Spotify: ' +spotify_response['tracks']['items'][0]['album']['artists'][0]["external_urls"]['spotify']
    a_al ='Top tracks on Apple Music: ' +itunes_response['results'][0]["artistViewUrl"]
    l = []
    for i in range(1,5):
        l.append(d['results'][i]["collectionName"] + ' : ' + d['results'][i]["collectionViewUrl"] )
    arr = [artist_image, artist_name, a_sl, a_al,l]







    try:
        l = extract_lyrics.get_lyrics(song)
    except:
        popup_showinfo('No lyrics found')
        printlyrics(0,arr)
    else:

        printlyrics(1,arr,l['lyrics'])
def Rem1():
    playground.delete(playground.curselection()[0])
    pygame.mixer.music.stop()

def Clearplaylist():
    playground.delete(0,END)
    pygame.mixer.music.stop()

def Themesetter(scrubFrame,shufbt,imagespace,imagespace1,imagespace2,loop,masterFrame,volumeFrame,playground,playbt,pausebt,nextbt,prevbt,stopbt,postime,lentime,colscheme):
    if colscheme=="MONOCHROME":
        loop.configure(bg="#454545")
        playground.config(bg="#999999",fg="#ffffff",selectbackground="#707070",selectforeground="#ffffff")
        playbt.config(bg="#999999")
        pausebt.config(bg="#999999")
        prevbt.config(bg="#999999")
        nextbt.config(bg="#999999")
        stopbt.config(bg="#999999")
        postime.config(bg="#454545",fg="#ffffff")
        lentime.config(bg="#454545",fg="#ffffff")
        masterFrame.configure(bg="#454545")
        volumeFrame.configure(bg="#454545")
        imagespace.configure(bg="#454545")
        imagespace1.configure(bg="#454545")
        imagespace2.configure(bg="#454545")
        shufbt.configure(bg="#999999")
        scrubFrame.configure(bg="#454545")


    if colscheme=="Glacier":
        loop.configure(bg="#20c3d0")
        playground.config(bg="#b9e8ea",fg="#000000",selectbackground="#86d6d8",selectforeground="#000000")
        playbt.config(bg="#20c3d0")
        pausebt.config(bg="#20c3d0")
        prevbt.config(bg="#20c3d0")
        nextbt.config(bg="#20c3d0")
        stopbt.config(bg="#20c3d0")
        postime.config(bg="#20c3d0")
        lentime.config(bg="#20c3d0")
        masterFrame.configure(bg="#20c3d0")
        volumeFrame.configure(bg="#20c3d0")
        imagespace.configure(bg="#20c3d0")
        imagespace1.configure(bg="#20c3d0")
        imagespace2.configure(bg="#20c3d0")
        shufbt.config(bg="#20c3d0")
        scrubFrame.configure(bg="#20c3d0")

    if colscheme=="Autumn Leaves" :
        loop.configure(bg="#98482b")
        playground.config(bg="#a64b29",fg="#ffffff",selectbackground="#853619",selectforeground="#ffffff")
        playbt.config(bg="#98482b")
        pausebt.config(bg="#98482b")
        prevbt.config(bg="#98482b")
        nextbt.config(bg="#98482b")
        stopbt.config(bg="#98482b")
        postime.config(bg="#98482b",fg="#ffffff")
        lentime.config(bg="#98482b",fg="#ffffff")
        masterFrame.configure(bg="#98482b")
        volumeFrame.configure(bg="#98482b")
        imagespace.configure(bg="#98482b")
        imagespace1.configure(bg="#98482b")
        imagespace2.configure(bg="#98482b")
        shufbt.config(bg="#98482b")
        scrubFrame.configure(bg="#98482b")

    if colscheme=="Spring" :
        loop.configure(bg="#54862e")
        playground.config(bg="#9ac37b",fg="#ffffff",selectbackground="#72a24e",selectforeground="#ffffff")
        playbt.config(bg="#54862e")
        pausebt.config(bg="#54862e")
        prevbt.config(bg="#54862e")
        nextbt.config(bg="#54862e")
        stopbt.config(bg="#54862e")
        postime.config(bg="#54862e",fg="#ffffff")
        lentime.config(bg="#54862e",fg="#ffffff")
        masterFrame.configure(bg="#54862e")
        volumeFrame.configure(bg="#54862e")
        imagespace.configure(bg="#54862e")
        imagespace1.configure(bg="#54862e")
        imagespace2.configure(bg="#54862e")
        shufbt.config(bg="#54862e")
        scrubFrame.configure(bg="#54862e")

    if colscheme=="Summer" :
        loop.configure(bg="#F3872F")
        playground.config(bg="#ffcc99",fg="#000000",selectbackground="#ff944d",selectforeground="#000000")
        playbt.config(bg="#F3872F")
        pausebt.config(bg="#F3872F")
        prevbt.config(bg="#F3872F")
        nextbt.config(bg="#F3872F")
        stopbt.config(bg="#F3872F")
        postime.config(bg="#F3872F")
        lentime.config(bg="#F3872F")
        masterFrame.configure(bg="#F3872F")
        volumeFrame.configure(bg="#F3872F")
        imagespace.configure(bg="#F3872F")
        imagespace1.configure(bg="#F3872F")
        imagespace2.configure(bg="#F3872F")
        shufbt.config(bg="#F3872F")
        scrubFrame.configure(bg="#F3872F")



def volume(x):
  pygame.mixer.music.set_volume(1 - sliderVolume.get())
  currentVolume = pygame.mixer.music.get_volume()
  #sliderText.config(text = int(currentVolume * 100))


def scrub(x):
    global shiftit
    toset=timescrub.get()*songlen/100
    shiftit=toset*100
    timescrub.configure(value=shiftit)
    pygame.mixer.music.set_pos(toset)
    pass
    




loop.title("Zankyo Player")
# loop.iconbitmap("Graphics/ZankyoIcon2.ico")
loop.geometry("900x480")
loop.configure(bg="#F3872F")

masterFrame = Frame(loop)
masterFrame.configure(bg="#F3872F")
masterFrame.pack(pady = 20)

playground=Listbox(masterFrame,bg='#ffcc99',fg="#000000",width=80,bd=5,selectbackground="#ff944d",selectforeground="#000000")
playground.bind('<<ListboxSelect>>', onselect)
playground.grid(row = 0, column = 0)
pygame.mixer.init()
playimg=PhotoImage(file="Graphics\\Playb.png")
pauseimg=PhotoImage(file="Graphics\\Pauseb.png")
nextimg=PhotoImage(file="Graphics\\Nextb.png")
previmg=PhotoImage(file="Graphics\\Prevb.png")
stopimg=PhotoImage(file="Graphics\\Stopb.png")

imagespace=Frame(masterFrame)
imagespace.configure(bg="#F3872F")
imagespace.grid(row = 1, column = 0, pady = 20)

volumeFrame = LabelFrame(masterFrame, text = "Volume")
volumeFrame.grid(row = 0, column = 1, padx = 20)
volumeFrame.configure(bg="#F3872F")
playbt=Button(imagespace,image=playimg,borderwidth=0,bg="#F3872F",command=playsong)
pausebt=Button(imagespace,image=pauseimg,borderwidth=0,bg="#F3872F",command=lambda: pausesong(pause_state))
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


imagespace2=Frame(loop)
imagespace2.configure(bg="#F3872F")
imagespace2.pack()
name = Label(imagespace2, text="Name:").grid(row=7, column = 1)

name_entry = Entry(imagespace2)
name_entry.grid(row=7, column=4)

bt = Button(imagespace2, text="Load Playlist", command=lambda :getuser(name_entry.get()))
bt.grid(row=8, column=2)
bt1 = Button(imagespace2, text="Update Playlist", command=lambda :updateuser(name_entry.get()))
bt1.grid(row=8, column=4)
bt2 = Button(imagespace2, text="Store Playlist", command=lambda :storeuser(name_entry.get()))
bt2.grid(row=8, column=6)
imagespace1=Frame(loop)
imagespace1.configure(bg="#F3872F")
imagespace1.pack()


sn = Label(imagespace1, text="Song Name:").grid(row=4, column = 3)

e2 = Entry(imagespace1)


e2.grid(row=4, column=4)
b = Button(imagespace1, text="Get Lyrics", command=lambda :getlyrics(e2.get()))
b.grid(row=4, column=5)







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
Themes.add_command(label="Monochrome",command=lambda: Themesetter(scrubFrame,shufbt,imagespace,imagespace1,imagespace2,loop,masterFrame,volumeFrame,playground,playbt,pausebt,nextbt,prevbt,stopbt,postime,lentime,"MONOCHROME"))
Themes.config(bg="#ffffff")
Themes.add_command(label="Glacier",command=lambda: Themesetter(scrubFrame,shufbt,imagespace,imagespace1,imagespace2,loop,masterFrame,volumeFrame,playground,playbt,pausebt,nextbt,prevbt,stopbt,postime,lentime,"Glacier"))
Themes.add_command(label="Autumn Leaves",command=lambda: Themesetter(scrubFrame,shufbt,imagespace,imagespace1,imagespace2,loop,masterFrame,volumeFrame,playground,playbt,pausebt,nextbt,prevbt,stopbt,postime,lentime,"Autumn Leaves"))
Themes.add_command(label="Spring",command=lambda: Themesetter(scrubFrame,shufbt,imagespace,imagespace1,imagespace2,loop,masterFrame,volumeFrame,playground,playbt,pausebt,nextbt,prevbt,stopbt,postime,lentime,"Spring"))
Themes.add_command(label="Summer",command=lambda: Themesetter(scrubFrame,shufbt,imagespace,imagespace1,imagespace2,loop,masterFrame,volumeFrame,playground,playbt,pausebt,nextbt,prevbt,stopbt,postime,lentime,"Summer"))
scrubFrame = LabelFrame(masterFrame)
scrubFrame.configure(bg="#F3872F")
scrubFrame.grid(row = 2, column = 0)
sliderVolume = ttk.Scale(volumeFrame, from_ = 0, to = 1, orient = VERTICAL, value = 0, command = volume, length = 100)
sliderVolume.pack(pady = 10)
timescrub=ttk.Scale(scrubFrame,from_=0, to=100, orient=HORIZONTAL,value=0,command=scrub,length=300)
timescrub.pack(pady=20)
postime=Label(scrubFrame,text="0:00",bg="#F3872F")
postime.pack(after=timescrub,pady=2)
lentime=Label(scrubFrame,text="0:00",bg="#F3872F")
lentime.pack(after=postime,pady=2)

loop.mainloop()

