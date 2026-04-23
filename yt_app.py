import customtkinter as ctk
from yt_dlp import YoutubeDL
import os
import threading
import subprocess
import sys
from tkinter import filedialog # ফোল্ডার সিলেক্ট করার জন্য

ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("blue")

class YTDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nasrullah's Pro Downloader")
        self.geometry("600x550")

        # ডিফল্ট ডাউনলোড পাথ
        self.download_path = os.path.join(os.path.expanduser('~'), 'Downloads')

        # UI Elements
        self.label = ctk.CTkLabel(self, text="YouTube Video Link:", font=("Arial", 16))
        self.label.pack(pady=10)

        self.link_entry = ctk.CTkEntry(self, width=450, placeholder_text="Paste link here...")
        self.link_entry.pack(pady=5)

        # ডাউনলোড পাথ দেখানোর লেবেল
        self.path_label = ctk.CTkLabel(self, text=f"Path: {self.download_path}", font=("Arial", 10), text_color="gray")
        self.path_label.pack(pady=2)

        # পাথ সিলেক্ট করার বাটন
        self.path_btn = ctk.CTkButton(self, text="Change Folder", fg_color="transparent", border_width=1, command=self.choose_path)
        self.path_btn.pack(pady=5)

        # রেজোলিউশন অপশন
        self.res_var = ctk.StringVar(value="720p")
        self.res_option = ctk.CTkOptionMenu(self, values=["Best", "1080p", "720p", "480p", "Best Audio"], variable=self.res_var)
        self.res_option.pack(pady=10)

        # প্রগ্রেস বার
        self.progress_label = ctk.CTkLabel(self, text="0%")
        self.progress_label.pack(pady=5)
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=5)

        # ডাউনলোড বাটন
        self.download_btn = ctk.CTkButton(self, text="Download Now", command=self.start_download_thread)
        self.download_btn.pack(pady=20)

        # লাইব্রেরি আপডেট বাটন
        self.update_btn = ctk.CTkButton(self, text="Update App Engine", fg_color="orange", text_color="black", command=self.update_engine)
        self.update_btn.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=10)

    def choose_path(self):
        path = filedialog.askdirectory()
        if path:
            self.download_path = path
            self.path_label.configure(text=f"Path: {self.download_path}")

    def update_engine(self):
        def run_update():
            self.status_label.configure(text="Updating Engine... Please wait", text_color="blue")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp", "--break-system-packages"])
                self.status_label.configure(text="Update Successful!", text_color="green")
            except:
                self.status_label.configure(text="Update Failed. Check Internet.", text_color="red")
        
        threading.Thread(target=run_update).start()

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%','')
            try:
                self.progress_bar.set(float(p) / 100)
                self.progress_label.configure(text=f"{p}%")
                self.update_idletasks()
            except: pass
        elif d['status'] == 'finished':
            self.status_label.configure(text="Download Complete!", text_color="green")

    def start_download_thread(self):
        self.download_btn.configure(state="disabled")
        threading.Thread(target=self.download_video).start()

    def download_video(self):
        url = self.link_entry.get()
        if not url:
            self.status_label.configure(text="Please paste a link!", text_color="red")
            self.download_btn.configure(state="normal")
            return

        quality = self.res_var.get()
        fmt = 'bestvideo+bestaudio/best' if quality == "Best" else f'bestvideo[height<={quality.replace("p","")}]+bestaudio/best'

        ydl_opts = {
            'format': fmt,
            'outtmpl': f'{self.download_path}/%(title)s.%(ext)s',
            'progress_hooks': [self.progress_hook],
        }

        try:
            self.status_label.configure(text="Downloading...", text_color="blue")
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            self.status_label.configure(text="Error occurred!", text_color="red")
        finally:
            self.download_btn.configure(state="normal")

if __name__ == "__main__":
    app = YTDownloader()
    app.mainloop()