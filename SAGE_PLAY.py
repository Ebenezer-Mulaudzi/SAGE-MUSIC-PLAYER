import os
import pickle
import tkinter as tk
from pygame import mixer
from tkinter import filedialog
from tkinter import PhotoImage


class Player(tk.Frame):

    def __init__(self, main):
        super().__init__(main)
        self.main = main 
        self.pack()

        mixer.init()

        if os.path.exists("songs.pickle"):
            with open("songs.pickle", "rb") as f:
                self.playlist = pickle.load(f)
        else:
            self.playlist = []

        self.current = 0
        self.paused = True
        self.played = False

        self.createFrames()
        self.trackWidgets()
        self.contolWidgets()
        self.tracklistWidgets()

    def createFrames(self):
        self.track = tk.LabelFrame(self, text="Song Track",
                    font=("calibri",15,"bold"),bg="black", fg="teal",
                    bd=5,relief=tk.GROOVE)

        self.track.config(width=410, height=300)
        self.track.grid(row=0, column=1)

        self.tracklist = tk.LabelFrame(self, text=f"Track List - {len(self.playlist)}",
                    font=("calibri",15,"bold"),bg="black", fg="teal",
                    bd=5,relief=tk.GROOVE)

        self.tracklist.config(width=250, height=580)
        self.tracklist.grid(row=0, column=2 )

        self.controls = tk.LabelFrame(self,font=("calibri",15,"bold"),bg="black", fg="teal",
                    bd=2,relief=tk.GROOVE)

        self.controls.config(width=410, height=80)
        self.controls.grid(row=0, column=0)

    def trackWidgets(self):
        self.canvas = tk.Label(self.track, image=bgImg)
        self.canvas.config(width=626, height=626)
        self.canvas.grid(row=0, column=0)

        self.songtrack = tk.Label(self.track, font=("calibri",15,"bold"),bg="black",fg="teal")
        self.songtrack["text"] = "SAGE MP3 PLAYER"
        self.songtrack.config(width=30, height=1)
        self.songtrack.grid(row=1, column=0)

    def contolWidgets(self):
        self.loadSongs = tk.Button(self.controls, image=loadSongs, command=self.loadMusic)
        self.loadSongs.grid(row=0, column=0)

        self.prev = tk.Button(self.controls, image=prev, command=self.prevSong)
        self.prev.grid(row=1, column=0)

        self.next = tk.Button(self.controls, image=next, command=self.nextSong)
        self.next.grid(row=3, column=0)

        self.pause = tk.Button(self.controls, image=pause, command=self.pauseSong)
        self.pause.grid(row=2, column=0)
        
        #VOLUME

        #self.volume = tk.Label(self.controls, font=("calibri",12))
        #self.volume.grid(row=4,column=1)
        #self.volumeUp = tk.Button(self.controls, text="+", font=("calibri",12),fg="teal",width=4,height=4, command=increaseVolume).grid(row=4,column=0,sticky="W")
        #self.volumeDown = tk.Button(self.controls, text="-", font=("calibri",12),fg="teal",width=4,height=4, command=decreaseVolume).grid(row=4,sticky="E")
        
        self.volume = tk.DoubleVar()
        self.slider = tk.Scale(self.controls, from_=0, to=10,orient=tk.HORIZONTAL, command=self.changeVolume)
        self.slider["variable"] =self.volume
        self.slider.set(5)
        self.slider.grid(row=4,column=0)


    def tracklistWidgets(self):
        self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0,column=1,rowspan=10,sticky="ns")

        self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE, height=30, width=29,
                    yscrollcommand=self.scrollbar.set, selectbackground="sky blue",bg="black", fg="teal")
        self.enumerateSongs()
        self.config(height=22)
        self.bind("<Double-1>", self.playSong)
        self.scrollbar.config(command=self.list.yview)
        self.list.grid(row=0, column=0, rowspan=10)

    def enumerateSongs(self):
        for index, song in enumerate(self.playlist):
            self.list.insert(index, os.path.basename(song))
    
    def loadMusic(self):
        self.songlist = []
        filePath = filedialog.askdirectory()
        for root_, dirs, files in os.walk(filePath):
            for file in files:
                if os.path.splitext(file)[1] == ".mp3":
                    path = (root_ + '/' + file).replace('\\','/')
                    self.songlist.append(path)
        
        with open("songs.pickle","wb") as f:
            pickle.dump(self.songlist, f)

        self.playlist = self.songlist
        self.tracklist["text"] = f"PlayList - {str(len(self.playlist))}"
        self.list.delete(0,tk.END)
        self.enumerateSongs()

    def playSong(self, event=None):
        if event is not None:
            self.current = self.list.curselection()[0]
            for i in range(len(self.playlist)):
                self.list.itemconfigure(i, bg="white")

        mixer.music.load(self.playlist[self.current])
        self.songtrack["anchor"] = "w"
        self.songtrack["text"] = os.path.basename(self.playlist[self.current])

        self.pause["image"] = play
        self.paused = False
        self.played = True
        self.list.activate(self.current)
        self.list.itemconfigure(self.current, bg="sky blue")
        
        mixer.music.play()

    def pauseSong(self):
        if not self.paused:
            self.paused =True
            mixer.music.pause()
            self.pause["image"] = pause
        else:
            if self.played == False:
                self.playSong()
            self.paused = False
            mixer.music.unpause()
            self.pause["image"] = play

    def prevSong(self):

        if self.current > 0:
            self.current -= 1 
        else:
            self.current = 0
        self.list.itemconfigure(self.current + 1, bg='white')
        self.playSong()

    def nextSong(self):
        if self.current < len(self.playlist) - 1:
            self.current += 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current - 1, bg='white')
        self.playSong()

    def changeVolume(self, event=None):
        self.v = self.volume.get()
        mixer.music.set_volume(self.v / 10)




master = tk.Tk()
master.geometry("1040x690")
master.wm_title("SAGE M PLAYER")
master.wm_resizable(width=False, height=False)

bgImg = PhotoImage(file="Images/SAGE1.png")
next = PhotoImage(file="Images/end.png")
prev = PhotoImage(file="Images/skip-to-start.png")
play = PhotoImage(file="Images/circled-play.png")
pause = PhotoImage(file="Images/circled-pause.png")
loadSongs = PhotoImage(file="Images/numbered-list.png")
increaseVolume = PhotoImage(file="Images/high-volume.png")
decreaseVolume = PhotoImage(file="Images/medium-volume.png")
muteVolume = PhotoImage(file="Images/mute.png")

app = Player(main=master)
app.mainloop()
