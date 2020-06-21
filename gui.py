import tkinter as tk
from tkinter import StringVar
from PIL import Image, ImageColor
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
current_track = None
user = None

FONT_SIZE = 10
TYPE_FACE = "Roboto"
# Rate at which the GUI is updated: Every 0.1s
UPDATE_SPEED = 100
TIME_ELAPSED = 0


def update_current_song():
    global current_track
    if user:
        user_track = user.get_current_track()
        if not current_track or current_track != user_track:
            # print("SONG CHANGE")
            current_track = user_track
            song.set(current_track.track_info())


def token_status():
    global TIME_ELAPSED
    if user:
        TIME_ELAPSED += UPDATE_SPEED
        if TIME_ELAPSED % (user.get_expiration_time() * 10) == 0:
            user.update_token()


def repeater(master):
    update_current_song()
    token_status()
    root.after(UPDATE_SPEED, repeater, master)


def rgb_to_hex(rgb: (int, int, int)) -> str:
    return "#" + "".join(str(hex(color))[2:] if color > 15 else f"0{str(hex(color))[2:]}" for color in rgb)


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
        settings_menu = tk.Menu(popout)
        popout.config(menu=settings_menu)

        edit_menu = tk.Menu(settings_menu)
        settings_menu.add_cascade(label="Edit", menu=edit_menu)

        edit_menu.add_command(label="Change Typeface")
        edit_menu.add_command(label="Change Font")
        edit_menu.add_command(label="Change Background Color", command=self.change_bg_color)
        edit_menu.add_command(label="Change Text Cutout Size")
        popout.title("Song")
        popout.iconbitmap(r"assets//bot_logo.ico")
        self.bg_color = tk.Label(popout, textvariable=song, bg="#00ff00", fg="white", font=f"{TYPE_FACE} {30}",
                                 width=45, anchor="w")
        self.bg_color.pack()

    def change_bg_color(self) -> None:
        color = tk.Toplevel(self.root)
        color.title("Background Color")
        color.iconbitmap(r"assets//bot_logo.ico")
        status = StringVar()
        status.set("Valid")
        red = StringVar()
        green = StringVar()
        blue = StringVar()
        red.set("0")
        green.set("255")
        blue.set("0")
        current_color = self.bg_color["bg"]

        def update_color():
            nonlocal current_color
            current_color = rgb_to_hex((int(red.get()), int(green.get()), int(blue.get())))

        def is_valid_rgb(value: int) -> bool:
            return 0 <= value <= 255 if type(value) is int else False

        def preview_status():
            r, g, b = int(red.get()), int(green.get()), int(blue.get())
            rgb_status = [("R", is_valid_rgb(r)), ("G", is_valid_rgb(g)), ("B", is_valid_rgb(b))]
            if all([c[1] for c in rgb_status]):
                preview.config(bg=rgb_to_hex((r, g, b)))
                status.set("Valid")
            else:
                status_msg = f"Invalid Inputs For: " + ", ".join(f"{c[0]}" for c in rgb_status)
                status.set(status_msg)

        def change_bg_color(bg_label: tk.Label):
            update_color()
            bg_label.config(bg=current_color)
            color.destroy()

        preview = tk.Label(color, width=25, height=10, bg=current_color)
        preview.grid(row=0, rowspan=5)

        # RED
        tk.Label(color, text='R').grid(row=2, column=1)
        red_entry = tk.Entry(color, textvariable=red)
        red_entry.grid(row=2, column=2)

        # GREEN
        tk.Label(color, text='G').grid(row=3, column=1)
        green_entry = tk.Entry(color, textvariable=green)
        green_entry.grid(row=3, column=2)

        # BLUE
        tk.Label(color, text='B').grid(row=4, column=1)
        blue_entry = tk.Entry(color, textvariable=blue)
        blue_entry.grid(row=4, column=2)

        # Color Status
        tk.Label(color, text="Status: ").grid(row=5, column=1)
        tk.Label(color, textvariable=status).grid(row=5, column=2)

        # Preview Color
        tk.Button(color, text="Preview Color", command=preview_status).grid(row=6, column=2, pady=5)

        # Done Button
        tk.Button(color, text="Done",
                  command=(lambda: change_bg_color(self.bg_color))).grid(row=6, column=3, padx=5, pady=5)


if __name__ == "__main__":
    StartGUI(root)
    root.mainloop()
