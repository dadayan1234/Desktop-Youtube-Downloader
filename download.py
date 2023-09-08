
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk  # Import the ttk module for themed widgets
from threading import Thread
import yt_dlp

class YoutubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Youtube Video Downloader")

        self.video_url_label = tk.Label(root, text="Video URL:")
        self.video_url_label.pack()

        self.video_url_entry = tk.Entry(root)
        self.video_url_entry.pack()

        self.download_button = tk.Button(root, text="Download", command=self.download_video, bg="green", fg="white")
        self.download_button.pack()

        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack()

    def download_video(self):
        video_url = self.video_url_entry.get()

        if not video_url:
            messagebox.showerror("Error", "Please enter a video URL.")
            return

        ydl_opts = {
            'verbose': True,
            'progress_hooks': [self.update_progress],
	    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }

        self.download_button.config(state="disabled")
        self.progress_bar["value"] = 0

        self.download_thread = Thread(target=self.perform_download, args=(video_url, ydl_opts))
        self.download_thread.start()

    def perform_download(self, video_url, ydl_opts):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            self.progress_bar["value"] = 100
            self.choose_save_directory()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.download_button.config(state="normal")

    def update_progress(self, d):
        if d["status"] == "downloading":
            percent = d["_percent_str"]
            self.progress_bar["value"] = float(percent.strip("%"))

    def choose_save_directory(self):
        save_directory = filedialog.askdirectory()
        if save_directory:
            messagebox.showinfo("Download Complete", f"Video downloaded and saved to: {save_directory}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YoutubeDownloaderApp(root)
    root.mainloop()