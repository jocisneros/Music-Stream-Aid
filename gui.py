import tkinter as tk
from tkinter import StringVar
from PIL import Image
from PIL.ImageTk import PhotoImage
import webbrowser
import spotify_api_interpreter as sp_api_int
from spotify_data import User


def window_preset(master):
    master.title("j0zee TwitchBot")
    master.iconbitmap(r"assets//bot_logo.ico")
    master.geometry("500x500")


root = tk.Tk()
home_image = PhotoImage(file=r"assets//background_placeholder.png")
sp_login_image = PhotoImage(file=r"assets//spotify_login.png")
temp_art = PhotoImage(file=r"assets//temp_album.png")
song = StringVar()
user = None

FONT_SIZE = 10
TYPE_FACE = "Roboto"
# Rate at which the GUI is updated: Every 0.1s
UPDATE_SPEED = 100


def update_current_song():
    if user:
        song.set(user.get_current_track().track_info())


def repeater(master):
    update_current_song()
    root.after(UPDATE_SPEED, repeater, master)


class StartGUI:
    def __init__(self, master: tk.Tk):
        self.root = master
        self.login_frame = tk.Frame(master)
        self.login_frame.pack()

        self.home_image = tk.Label(self.login_frame, image=home_image)
        self.home_image.pack(side=tk.TOP)

        self.sp_login = tk.Button(self.login_frame, bg="#191414", image=sp_login_image, relief="solid",
                                  command=self.spotify_login)
        self.sp_login.pack(side=tk.TOP)

    def spotify_login(self) -> None:
        self.hide_home_frame()
        webbrowser.open(sp_api_int.auth_url)
        status = "NOT_RECEIVED"
        while status == "NOT_RECEIVED" or not status:
            with open("_auth_code.txt", "r") as file:
                status = file.read().strip()
        with open("_auth_code.txt", "w") as file:
            file.write("NOT_RECEIVED")
        self.login_frame.destroy()
        HomeGUI(self.root, status)

    def hide_home_frame(self) -> None:
        for widget in self.login_frame.winfo_children():
            widget.destroy()


class HomeGUI:
    def __init__(self, master, auth_code):
        self.root = master
        master.geometry("632x500")

        # Frame Declarations: User, Middle, and Queue
        self.user_frame = tk.Frame(master, bg="#2d2d2d")
        self.user_frame.grid(row=0)
        self.queue_frame = tk.Frame(master, bg="#2d2d2d")
        self.queue_frame.grid(row=1)

        global user, song
        user = User(auth_code)

        # Label and Button Declarations for User Frame
        tk.Label(self.user_frame, text="Current User:", bg="#1e1e1e", fg="white", width=22,
                 font=f"{TYPE_FACE} {FONT_SIZE}").grid(row=0)
        user_name = tk.Label(self.user_frame, text=f"{user.get_display_name()}", bg="#2d2d2d", fg="white",
                             font=f"{TYPE_FACE} {FONT_SIZE + 1}")
        user_name.grid(row=1)
        tk.Label(self.user_frame, text="Current Song", bg="#1e1e1e", fg="white",
                 width=65, font=f"{TYPE_FACE} 10").grid(row=2, column=1, columnspan=2)
        song_label = tk.Label(self.user_frame, width=45, textvariable=song, anchor="w", font=f"{TYPE_FACE} {FONT_SIZE}")
        song_label.grid(row=3, column=1, padx=5)
        album_art_label = tk.Label(self.user_frame, image=temp_art)
        album_art_label.grid(row=3, padx=5, pady=5)
        song_popout = tk.Button(self.user_frame, text="Popout Current Song", font=f"{TYPE_FACE} {FONT_SIZE}",
                                command=self.song_popout)
        song_popout.grid(row=3, column=2, padx=5)

        # Label and Button Declarations for Queue Frame
        tk.Label(self.queue_frame, text="Requested Queue", width=65, bg="#1e1e1e", fg="white",
                 font=f"{TYPE_FACE} {FONT_SIZE}").grid(row=0)
        scrollbar = tk.Scrollbar(self.queue_frame)
        scrollbar.grid(row=1)

    def song_popout(self):
        popout = tk.Toplevel(self.root)
        popout.title("Song")
        popout.iconbitmap(r"assets//bot_logo.ico")
        tk.Label(popout, textvariable=song, bg="#00ff00", fg="white", font=f"{TYPE_FACE} {30}", width=45,
                 anchor="w").pack()


if __name__ == "__main__":
    StartGUI(root)
    root.mainloop()
