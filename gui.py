import tkinter as tk
from PIL import Image
from PIL.ImageTk import PhotoImage
import webbrowser
import spotify
from threading import Thread


class AppGUI(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.root = tk.Tk()
        self.root.title("j0zee TwitchBot")
        self.root.iconbitmap(r"assets//bot_logo.ico")
        self.root.geometry("500x500")
        self.main_frame = tk.Frame(self.root).grid(row=0)

        sp_login_image = PhotoImage(file=r"assets//spotify_login.png")
        tk.Button(self.main_frame, image=sp_login_image, command=self.spotify_login).grid(row=1)

        home_image = PhotoImage(file=r"assets//background_placeholder.png")
        tk.Label(self.main_frame, image=home_image).grid(row=0)

        self.root.mainloop()

    @staticmethod
    def spotify_login() -> None:
        webbrowser.open(spotify.auth_url)

#AppGUI()