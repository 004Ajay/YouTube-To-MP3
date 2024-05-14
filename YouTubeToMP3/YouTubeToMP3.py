import os
import sys
import time
import tkinter
from pytube import YouTube
import customtkinter as ctk
from tkinter import filedialog
import threading

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def select_output_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    if folder_path:
        download_info_label.configure(text=f"Selected folder: {folder_path}")
    else:
        download_info_label.configure(text="No folder selected.")

def download_mp3():
    video_url = url.get()
    filename_text = filename.get()

    try:
        yt = YouTube(video_url)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=folder_path)
        new_file = (f"{folder_path}/{filename_text}.mp3")
        os.rename(out_file, new_file)

        download_info_label.configure(text="MP3 downloaded & saved successfully.")
        
        time.sleep(7)
        root.destroy()

    except:
        download_info_label.configure(text="Download Error.")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("YouTube to MP3")
root.iconbitmap(resource_path("img\\icon.ico")) # app icon (top left corner)
root.geometry("500x250")

win_width = root.winfo_screenwidth()
win_height = root.winfo_screenheight()

frame = ctk.CTkFrame(root, width=win_width/2, height=win_height/2)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

url = ctk.CTkEntry(master=frame, placeholder_text="Enter URL", width=300, fg_color='white', text_color='black')
url.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

filename = ctk.CTkEntry(master=frame, placeholder_text="Enter Filename", width=200, fg_color='white', text_color='black')
filename.place(relx=0.432, rely=0.4, anchor=tkinter.CENTER)

select_output_folder_button = ctk.CTkButton(master=frame, text="Select Output Folder", command=select_output_folder)
select_output_folder_button.place(relx=0.61, rely=0.4, anchor=tkinter.CENTER)

# Deamon=True -> Daemon threads automatically terminate when the main thread (Tkinter's main loop) exits.
download_button = ctk.CTkButton(master=frame, text="Download MP3", command=lambda: threading.Thread(target=download_mp3, daemon=True).start())
download_button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

download_info_label = ctk.CTkLabel(master=frame, text="")
download_info_label.place(relx=0.5, rely=0.63, anchor=tkinter.CENTER)

root.mainloop()