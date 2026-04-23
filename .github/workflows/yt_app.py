import sys

import customtkinter as ctk
from yt_dlp import YoutubeDL
import os
import threading

# অ্যাপের থিম সেটআপ
ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("blue")

# ফাইলের সঠিক পাথ খুঁজে বের করার ফাংশন (বিল্ড করার পর এটি দরকার হয়)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class YTDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Nasrullah's YT Downloader")
        self.geometry("600x450")

        # ক্লাসের ভেতরে আইকন সেট করুন এভাবে:
        try:
            logo_img = ctk.PhotoImage(file=resource_path("logo.png"))
            self.iconphoto(False, logo_img)
        except Exception as e:
            print(f"Logo error: {e}")
                # UI Elements
        self.label = ctk.CTkLabel(self, text="YouTube Video Link:", font=("Arial", 16))
        self.label.pack(pady=10)

        self.link_entry = ctk.CTkEntry(self, width=450, placeholder_text="Paste link here...")
        self.link_entry.pack(pady=5)

        # রেজোলিউশন অপশন
        self.res_label = ctk.CTkLabel(self, text="Select Quality:")
        self.res_label.pack(pady=5)
        
        self.res_var = ctk.StringVar(value="720p")
        self.res_option = ctk.CTkOptionMenu(self, values=["Best", "1080p", "720p", "480p", "Best Audio"], variable=self.res_var)
        self.res_option.pack(pady=5)

        # প্রগ্রেস বার
        self.progress_label = ctk.CTkLabel(self, text="0%")
        self.progress_label.pack(pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        self.download_btn = ctk.CTkButton(self, text="Download Now", command=self.start_download_thread)
        self.download_btn.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=10)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            # শতাংশ হিসাব করা
            p = d.get('_percent_str', '0%').replace('%','')
            try:
                progress_float = float(p) / 100
                self.progress_bar.set(progress_float)
                self.progress_label.configure(text=f"{p}%")
                self.update_idletasks()
            except:
                pass
        elif d['status'] == 'finished':
            self.progress_bar.set(1)
            self.progress_label.configure(text="100%")
            self.status_label.configure(text="Download Complete!", text_color="green")

    def start_download_thread(self):
        # ডাউনলোড শুরু করলে বাটন ডিজেবল করে দেওয়া যাতে বারবার ক্লিক না হয়
        self.download_btn.configure(state="disabled")
        thread = threading.Thread(target=self.download_video)
        thread.start()

    def download_video(self):
        url = self.link_entry.get()
        if not url:
            self.status_label.configure(text="Please paste a link!", text_color="red")
            self.download_btn.configure(state="normal")
            return

        quality = self.res_var.get()
        
        # রেজোলিউশন অনুযায়ী ফরম্যাট সেট করা
        if quality == "Best":
            fmt = 'bestvideo+bestaudio/best'
        elif quality == "Best Audio":
            fmt = 'bestaudio/best'
        else:
            res = quality.replace('p', '')
            fmt = f'bestvideo[height<={res}]+bestaudio/best[height<={res}]'

        download_path = os.path.join(os.path.expanduser('~'), 'Downloads')

        ydl_opts = {
            'format': fmt,
            'outtmpl': f'{download_path}/%(title)s.%(ext)s',
            'progress_hooks': [self.progress_hook],
            'nocheckcertificate': True,
            # আগের কুকিজ সমস্যা এড়াতে নিচের লাইনটি গুরুত্বপূর্ণ
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        try:
            self.status_label.configure(text="Downloading...", text_color="blue")
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}", text_color="red")
        finally:
            self.download_btn.configure(state="normal")

if __name__ == "__main__":
    app = YTDownloader()
    app.mainloop()