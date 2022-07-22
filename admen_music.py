import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from ttkthemes import themed_tk as theme
from tkinter import filedialog
import tkinter.messagebox as msg
from pygame import mixer
from playsound import playsound
import os
import time
import threading
from mutagen.mp3 import MP3

from utils.music_utilities import get_files_inside_directory_not_recursive, play_sound, is_sound_playing, pause_sounds, stop_sounds, unpause


#=====================================================================FUNCTIONS=======================
#note pygame dont support mp3 file, but playsound support it
while True:
    win = theme.ThemedTk()
    win.set_theme("black")
    win.title("open play music")

    win.geometry("800x650")
    infomu = tk.StringVar()
    main_label = tk.Label(win, width=800, height=730, bg="black")

    menubar = tk.Menu(main_label, bg="black", fg="white")
    win.config(menu=menubar)
    subMenu = tk.Menu(menubar, tearoff=0)

    musiclist = []

    listboxframe = tk.Frame(main_label, width=320, height=730, bg="black")
    list_of_music = tk.Listbox(listboxframe, width=40, height=33, bg="black", fg="white")

    #====================================music info ===========================================
    def start_count(t):
        global paused
        current_time = 0
        while current_time <= t and is_sound_playing():
            if not is_sound_playing():
                continue
            elif is_sound_playing():
                mins, secs = divmod(current_time, 60)
                mins = round(mins)
                secs = round(secs)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                currenttimelabel['text'] = timeformat
                time.sleep(1)
                current_time += 1

    def show_details(song):
        file_data = os.path.splitext(song)

        if file_data[1] == '.mp3':
            audio = MP3(song)
            total_length = audio.info.length
        else:
            a = mixer.Sound(song)
            total_length = a.get_length()

        # div - total_length/60, mod - total_length % 60
        mins, secs = divmod(total_length, 60)
        mins = round(mins)
        secs = round(secs)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        lengthlabel['text'] = timeformat
        t1 = threading.Thread(target=start_count, args=(total_length,))
        t1.start()
    #===============================================================================================
    def set_vol(val):
        volume = float(val) / 100
        mixer.music.set_volume(volume)
        # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1


    muted = tk.FALSE

    def mute_music():
        global muted
        if muted:  # Unmute the music
            mixer.music.set_volume(0.7)
            volume_image_label.configure(image=volume_image)
            scale.set(70)
            muted = tk.FALSE
        else:  # mute the music
            mixer.music.set_volume(0)
            volume_image_label.configure(image=muted_image)
            scale.set(0)
            muted = tk.TRUE


    def info_music(music):
        inf = music.split("/")
        inf = inf[-1]
        infomu.set(inf)

    def play():
        try:
            if is_sound_playing():
                pause_sounds()
                image_play_label.configure(image=image_play)
                statusbar.configure(fg="red")
                statusbar['text'] = 'Music Paused'
                music_playing_info.configure(fg="red")
                infomu.set("Paused")
            elif is_sound_playing() == False:
                #time.sleep(1)
                music_playing_info.configure(fg="white")
                statusbar.configure(fg="white")
                global selected_song
                selected_song = list_of_music.curselection()
                selected_song = int(selected_song[0])
                playing = musiclist[selected_song]
                play_sound(playing)
                image_play_label.configure(image=image_pause)
                image_play_label.image = image_pause
                info_music(playing)
                show_details(playing)
                statusbar['text'] = "Playing music: " + os.path.basename(playing)
        except:
            msg.showerror("song not selected", "please select song")


    def next():
        try:
            global selected_song
            statusbar.configure(fg="white")
            music_playing_info.configure(fg="white")
            selected_song += 1
            stop_sounds()
            playing = musiclist[selected_song]
            play_sound(playing)
            image_play_label.configure(image=image_pause)
            image_play_label.image = image_pause
            info_music(playing)
            show_details(playing)
            statusbar['text'] = "Playing music: " + os.path.basename(playing)
        except:
            selected_song -= 1
            image_play_label.configure(image=image_play)
            statusbar.configure(fg="red")
            music_playing_info.configure(fg="red")
            infomu.set("List of Music Done")
            statusbar['text'] = "List Of Music Done"

    """
    def pause_unpause():
        if is_sound_playing():
            pause_sounds()
        else:
            unpause()"""

    def back():
        try:
            statusbar.configure(fg="white")
            music_playing_info.configure(fg="white")
            global selected_song
            selected_song -= 1
            stop_sounds()
            playing = musiclist[selected_song]
            play_sound(playing)
            image_play_label.configure(image=image_pause)
            image_play_label.image = image_pause
            info_music(playing)
            show_details(playing)
            statusbar['text'] = "Playing music: " + os.path.basename(playing)
        except:
            selected_song += 1
            image_play_label.configure(image=image_play)
            statusbar.configure(fg="red")
            music_playing_info.configure(fg="red")
            infomu.set("List of Music Done")
            statusbar['text'] = "List Of Music Done"


    #===============listboxlabel==================================================================================
    def add_to_playlist(filename):
        filename = os.path.basename(filename)
        index = 0
        list_of_music.insert(index, filename)
        musiclist.insert(index, filename_path)
        index += 1
    def browse_file():
        global filename_path
        filename_path = filedialog.askopenfilename()
        add_to_playlist(filename_path)

        #mixer.music.queue(filename_path)

    def del_song():
        try:
            selected_song = list_of_music.curselection()#seleciona elemento da lista
            selected_song = int(selected_song[0])
            list_of_music.delete(selected_song)
            musiclist.pop(selected_song)
        except:
            msg.showerror("select song", "please select the song")


    list_of_music.pack(side=tk.TOP, fill=tk.Y)

    menubar.add_cascade(label="File", menu=subMenu)
    subMenu.add_command(label="Open", command=browse_file)
    subMenu.add_command(label="Exit", command=win.destroy)

    def about_us():
        msg.showinfo('about admen play music',
        'by Mario Mutondo, [o seu nome]')


    subMenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=subMenu)
    subMenu.add_command(label="About Us", command=about_us)

    botton_frame = tk.Frame(listboxframe, width=320, height=40, bg="black")
    botton_add = tk.Button(botton_frame, text="Add +", bg="black", fg="white", command=browse_file)
    botton_del = tk.Button(botton_frame, text="del -", bg="black", fg="white", command=del_song)

    listboxframe.pack(side=tk.RIGHT, fill=tk.Y)#window principal
    botton_add.pack(side=tk.LEFT, fill=tk.X)
    botton_del.pack(side=tk.RIGHT, fill=tk.X)
    botton_frame.pack(side=tk.TOP, fill=tk.Y, expand=1)#frame de button[del e add]

    plusframe = tk.Frame(listboxframe, width=320, height=40, bg="black")
    #botton_del.pack(side=tk.TOP, fill=tk.Y, padx = (30, 165))
    #===============listboxlabeland===============================================================================

    top_label = tk.Frame(main_label, bg="black", width=480, height=370)
    image = Image.open("Images/pylot.png")
    image = ImageTk.PhotoImage(image)
    main_image_top_label = tk.Label(top_label, image=image, width=480, height=370, bg="black")
    main_image_top_label.image = Image
    main_image_top_label.pack(side=tk.TOP)
    top_label.pack(side=tk.TOP, fill=tk.Y)

    music_info_label =  tk.Frame(main_label, width=480, height=10, bg="black")
    music_playing_info = tk.Label(music_info_label, textvar=infomu, fg="white", bg="black")
    time_music_playing_info = tk.Label(music_info_label, text="----------------------------------------------------------------------------------------",
    fg="white", bg="black")

    volume_image = Image.open("Images/volume.png")
    volume_image = ImageTk.PhotoImage(volume_image)
    muted_image = Image.open("Images/mute.png")
    muted_image = ImageTk.PhotoImage(muted_image)

    scale = ttk.Scale(plusframe, from_=0, to=100, orient=tk.HORIZONTAL, command=set_vol)
    scale.set(70)  #valor padrao de volume quando a musica comecar
    mixer.music.set_volume(0.7)

    volume_image_label = tk.Button(plusframe, image=volume_image, bg="black", command=mute_music)
    volume_image_label.image = volume_image
    volume_image_label.pack(side=tk.LEFT, expand=1, fill=tk.X, padx=(0, 182), pady=(0, 1))
    scale.pack(side=tk.RIGHT, fill=tk.X)
    plusframe.pack(pady=0)

    statusbar = tk.Label(main_label, text="...", relief=tk.SUNKEN, anchor=tk.W, bg='black', fg="white", font='Times 10 italic')
    statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    lengthlabel = tk.Label(music_info_label, text='00:00', fg="white", bg="black", font='Times 10 italic')

    currenttimelabel = tk.Label(music_info_label, text='00:00', fg="white", bg="black", font='Times 10 italic')

    music_playing_info.pack(side=tk.TOP)
    currenttimelabel.pack(side=tk.BOTTOM, fill=tk.X)
    lengthlabel.pack(side=tk.BOTTOM, fill=tk.X)
    time_music_playing_info.pack(side=tk.TOP)
    music_info_label.pack(side=tk.TOP, fill=tk.Y)

    #===============================================================================================================

    bottom_label_frame = tk.Frame(main_label, width=480, height=345, bg="black")
    image_back = Image.open("Images/back.png")
    image_back = ImageTk.PhotoImage(image_back)
    image_back_label = tk.Button(bottom_label_frame, image=image_back, width=35, height=44, bg="black", command=back)
    image_back_label.image = image_back
    image_back_label.pack(fill=tk.X, side=tk.LEFT, padx=(30, 20))

    image_play =  Image.open("Images/play_button.png")
    image_play = ImageTk.PhotoImage(image_play)
    image_play_label = tk.Button(bottom_label_frame, image=image_play, width=64, height=64, bg="black", command=play)
    image_play_label.image = image_play
    image_play_label.pack(fill=tk.X, side=tk.LEFT, padx=(10, 30))

    #==================================pause button=========================================================================
    image_pause = Image.open("Images/pause.png")
    image_pause = ImageTk.PhotoImage(image_pause)
    #=================================next button===========================================================================
    image_next = Image.open("Images/next.png")
    image_next = ImageTk.PhotoImage(image_next)
    image_next_label = tk.Button(bottom_label_frame, image=image_next, width=34, height=44, bg="black", command=next)
    image_next_label.image = image_next
    image_next_label.pack(fill=tk.X, side=tk.LEFT, padx=(10, 30))
    #===================================info button==========================================================================

    bottom_label_frame.pack(side=tk.TOP, expand=1, fill=tk.Y)
    main_label.pack(side=tk.LEFT, fill=tk.Y)
    break

win.mainloop()
