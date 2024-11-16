import time
import vlc
import yt_dlp
import tkinter as tk
from threading import Thread, Event
import ctypes
import os

# Tentukan path ke VLC sesuai arsitektur (64-bit atau 32-bit)
dll_path = r'C:\Program Files\VideoLAN\VLC\libvlc.dll'

# Muat libvlc.dll secara manual
ctypes.CDLL(dll_path)

# Define the YouTube URL
youtube_url = 'https://www.youtube.com/watch?v=RCltAg_iK0E'

# Download audio using yt-dlp
def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': 'audio.%(ext)s',
        'ffmpeg_location': r'C:ffmpeg\bin',  # Ganti dengan lokasi folder bin ffmpeg kamu
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Function to control VLC player
class VLCPlayer:
    def __init__(self):
        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()
        media = self.vlc_instance.media_new("audio.mp3")
        self.player.set_media(media)
    
    def play(self):
        self.player.play()
    
    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

# Define the lyrics as a list of strings
lyrics = [
    "Bunny Girl by AKASAKI", #1
    "Yoru no hajimari sa, bunny girl", 
    "Yuuwaku sareru kodou ni",
    "hajike tobu kattou ni ai wo kanpai", 
    "Tsutaerarenakute mo koi no",
    "hajimari sa, bunny girl", 
    "Dareka wo ugatte sunda kimi no", 
    "me wo harande",
    
    "Saa, kiza na suteppu wo kizande",
    "Shigoto gaeri no tsukare wa watashi to, kono gurasu ni",
    "Saa, jibun konomi ni sugatte",
    "Seken ni taisuru kimochi, watashi ni sosoide minai?",
    "Arigachina rabu songu demo",
    "Ai ga komerareteru no",
    "Soredemo yogoreru no ne, kimi o mireba wakaru no",
    "Shita wo muku kimi no me wo, muriyari hagou to wa shinai",
    "Dakara sonna kao sezu te wo sashinobete hora",
    "Yoru no hajimari sa, bunny girl",
    "Yuuwaku sareru kodou ni hajike tobu kattou ni ai wo kanpai",
    "Tsutaerarenakute mo koi no hajimari sa, bunny girl",
    "Dareka wo ugatte sunda kimi no me wo harande",
    "Kimi no ai wo shitta ki de hai ni natte ite",
    "Kando satte ite, maido naite ite sa",
    "Sore kurai ga ii n desho",
    "Saa, kiza na suteppu wo kizande",
    "Kimi no kaoiro ima de wa mashi ni natte kite ru",
    "Kimi ni yudaneru wa, bunny girl",
    "Watashi wo ageru wa, bunny girl",
    "Yuuwaku sareru kodou ni hajike tobu kattou ni ai wo kanpai",
    "Tsutaerarete iru hazu",
    "Yoru no hajimari sa, bunny girl",
    "Dareka wo ugatte sunda kimi no me wo harande"
]

# Define the tempo for each line (in seconds)
tempo = [2, 3, 4, 3, 3, 2, 3, 3, 3, 2, 3, 3, 4, 3, 2, 4, 3, 3, 4, 3, 3, 3, 4, 3, 2, 3, 3]

# Function to display the lyrics line by line in the UI
def display_lyrics(label, stop_event, pause_event):
    for i, line in enumerate(lyrics):
        if stop_event.is_set():
            break
        while pause_event.is_set():
            time.sleep(0.1)
        label.config(text=line)
        time.sleep(tempo[i])

# Function to run both audio and lyrics display concurrently
def play_music_and_show_lyrics():
    stop_event.clear()  # Reset stop flag
    Thread(target=vlc_player.play).start()
    display_lyrics(label, stop_event, pause_event)

# Function to pause music and lyrics
def pause_music():
    vlc_player.pause()
    if pause_event.is_set():
        pause_event.clear()
    else:
        pause_event.set()

# Function to stop music and lyrics
def stop_music():
    stop_event.set()
    vlc_player.stop()

# Create the main application window using tkinter
root = tk.Tk()
root.title("Bunny Girl by AKASAKI")
root.geometry("600x400")

# Create a label to display the lyrics
label = tk.Label(root, text="", font=("Helvetica", 16), wraplength=500, justify="center")
label.pack(pady=20)

# Create a button to start the audio and lyrics display
play_button = tk.Button(root, text="Play Music", command=lambda: Thread(target=play_music_and_show_lyrics).start())
play_button.pack(pady=10)

# Create a button to pause the music
pause_button = tk.Button(root, text="Pause/Resume Music", command=pause_music)
pause_button.pack(pady=10)

# Create a button to stop the music
stop_button = tk.Button(root, text="Stop Music", command=stop_music)
stop_button.pack(pady=10)

# Main function to download audio and start the UI
def main():
    global vlc_player, stop_event, pause_event
    stop_event = Event()  # Event to control stopping
    pause_event = Event()  # Event to control pausing
    download_audio(youtube_url)
    vlc_player = VLCPlayer()
    root.mainloop()

# Run the program
if __name__ == "__main__":
    main()