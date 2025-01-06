import os
import tkinter
import customtkinter
from tkinter import messagebox
import yt_dlp
from datetime import datetime

def download_audio():
    yt_link = link_var.get()
    if not yt_link:
        messagebox.showerror("Error", "Please enter a YouTube link")
        return

    # Get the path to the user's Downloads folder
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

    # Create a unique filename with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(downloads_path, f'%(title)s_{timestamp}.%(ext)s'),
        'progress_hooks': [progress_hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(yt_link, download=False)
            video_title = info_dict.get('title', None)
            link_label.configure(text=video_title)
            ydl.download([yt_link])
        messagebox.showinfo("Success", "Download complete!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def progress_hook(d):
    if d['status'] == 'downloading':
        pbar.set(d['_percent_str'].strip())
    elif d['status'] == 'finished':
        pbar.set("100%")

# System Settings
customtkinter.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

# Create the main window
root = customtkinter.CTk()
root.title("YouTube to MP3 Downloader")
root.geometry("500x300")

# Create and place the widgets
title_label = customtkinter.CTkLabel(root, text="YouTube to MP3 Downloader", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

frame = customtkinter.CTkFrame(root)
frame.pack(pady=20)

link_label = customtkinter.CTkLabel(frame, text="YouTube Link:", font=("Helvetica", 12))
link_label.grid(row=0, column=0, padx=10, pady=10)
link_var = tkinter.StringVar()
customtkinter.CTkEntry(frame, textvariable=link_var, width=350, height=40, font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10)
customtkinter.CTkButton(frame, text="Download", command=download_audio, fg_color="green", text_color="white", font=("Helvetica", 12)).grid(row=2, column=0, pady=20)

pbar = tkinter.StringVar()
pbar.set("0%")
progress_label = customtkinter.CTkLabel(frame, textvariable=pbar, font=("Helvetica", 12))
progress_label.grid(row=3, column=0, pady=10)

# Run the application
root.mainloop()