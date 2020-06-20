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
song = StringVar()
queue_frame = tk.Frame(root)

album_art = tk.Label()
user = None


def update_current_song():
    global user
    if user:
        song.set(user.get_current_track().track_info())


def repeater(master):
    update_current_song()
    root.after(100, repeater, master)


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
        master.geometry("1000x500")

        # Frame Declarations: User, Middle, and Queue
        self.user_frame = tk.Frame(master, bg="#191414")
        self.user_frame.grid(row=0, columnspan=10)
        self.middle_frame = tk.Frame(master, bg="#191414", width=200, height=500)
        self.middle_frame.grid(row=0, column=11)
        self.queue_frame = tk.Frame(master, bg="#191414")
        self.queue_frame.grid(row=0, column=30, columnspan=10)

        global user, song
        user = User(auth_code)

        # Label and Button Declarations
        tk.Label(self.user_frame, text="Current User:").grid(row=0, column=1)
        user_name = tk.Label(self.user_frame, text=f"{user.get_display_name()}")
        user_name.grid(row=1, column=1)
        tk.Label(self.queue_frame, text="Current Song").grid(row=0, column=11)
        song_label = tk.Label(self.queue_frame, textvariable=song)
        song_label.grid(row=1, column=11)

        song_popout = tk.Button(self.queue_frame, text="Popout Current Song")
        song_popout.grid(row=1, column=12)


if __name__ == "__main__":
    StartGUI(root)
    root.mainloop()
