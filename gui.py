import tkinter as tk
import webbrowser
from io import BytesIO
from tkinter import StringVar

from PIL import Image, ImageColor
from PIL.ImageTk import PhotoImage

import spotify_modules.spotify_interpreter as sp_api_int
from logger import log_print
from spotify_modules.spotify_data import User

FONT_SIZE = 10
TYPE_FACE = "Roboto"
# Rate at which the GUI is updated: Every 0.1s
UPDATE_SPEED = 100
TIME_ELAPSED = 0

root = tk.Tk()
home_image = PhotoImage(file=r"assets//background_placeholder.png")
sp_login_image = PhotoImage(file=r"assets//spotify_login.png")
sp_logged_in_image = PhotoImage(file=r"assets//spotify_logged_in.png")
twitch_login_image = PhotoImage(file=r"assets//twitch_login.png")
twitch_logged_in_image = PhotoImage(file=r"assets/twitch_logged_in.png")
album_art = PhotoImage(file=r"assets//temp_album.png")
track_title = StringVar()
track_artists = StringVar()
track_album = StringVar()
track_info = StringVar()
art_label = None
current_track = None
user = None


def update_current_track():
    """Keeps track of currently playing track, updating the HomeGUI to reflect any changes."""
    global current_track, art_label, album_art
    if user:
        user_track = user.get_current_track()
        if not current_track or current_track != user_track:
            current_track = user_track
            track_title.set(current_track.get_title())
            track_artists.set(", ".join(current_track.get_artists()))
            track_album.set(current_track.get_album_title())
            track_info.set(current_track.get_track_info())
            if current_track:
                art_image = Image.open(BytesIO(current_track.get_album_art()))
                album_art = PhotoImage(image=art_image.resize((150, 150)))
                art_label.config(image=album_art)
                log_print(f"TRACK CHANGE: Now Playing {track_info.get()}")


def token_status():
    """Refreshes Spotify Access-Token once the expiration time has passed."""
    global TIME_ELAPSED
    if user:
        TIME_ELAPSED += UPDATE_SPEED
        if TIME_ELAPSED % (user.get_expiration_time() * 100) == 0:
            user.update_token()


def repeater(master):
    """Repeats the following commands every UPDATE_SPEED milliseconds."""
    update_current_track()
    token_status()
    root.after(UPDATE_SPEED, repeater, master)


def window_preset(master):
    master.title("Music Stream Aid")
    master.iconbitmap(r"assets//bot_logo.ico")
    master.geometry("500x500")


def rgb_to_hex(rgb: (int, int, int)) -> str:
    """Converts 3-Tuple of rgb int values to hex form, returning in # string form."""
    return "#" + "".join(str(hex(color))[2:] if color > 15 else f"0{str(hex(color))[2:]}" for color in rgb)


class StartGUI:
    # Starting GUI Window,
    #   06/22/2020: Currently displays PlaceHolder image for possible future logo and "Log in with Spotify" button.
    def __init__(self, master: tk.Tk):
        self.root = master
        self.login_frame = tk.Frame(master)
        self.login_frame.grid(row=0)
        self.sp_login_state = False
        self.auth_token = None
        self.twitch_opt = tk.BooleanVar()

        self.home_image = tk.Label(self.login_frame, image=home_image)
        self.home_image.grid(row=0, columnspan=3)

        self.sp_login = tk.Button(self.login_frame, bg="#191414", image=sp_login_image, relief="solid",
                                  command=self.spotify_login)
        self.sp_login.grid(row=1, column=1)

        # Next Button
        tk.Button(self.login_frame, text="Next", command=self.next).grid(row=4, column=2)

        # Twitch Bot Check
        tk.Checkbutton(self.login_frame, text="Enable Twitch Bot?", variable=self.twitch_opt,
                       onvalue=True, offvalue=False, command=self.enable_twitch_login).grid(row=2, column=1)

        # Twitch Login
        self.twitch_login = tk.Button(self.login_frame, bg="#191414", image=twitch_login_image, relief="solid",
                                      command=self._twitch_login)

    def spotify_login(self) -> None:
        """
        When pressed, opens a browser window prompting the user to log-in to spotify,
        providing all details on what information may be used. If logged in, changes
        GUI to HomeGUI.
        """
        webbrowser.open(sp_api_int.auth_url)
        status = "NOT_RECEIVED"
        while status == "NOT_RECEIVED" or not status:
            with open("inter_comm.txt", "r") as file:
                status = file.read().strip()
        with open("inter_comm.txt", "w") as file:
            file.write("NOT_RECEIVED")

        if status.startswith("CODE "):
            self.sp_login.config(image=sp_logged_in_image, borderwidth=0, relief=tk.SUNKEN, command=lambda: None)
            self.auth_token = status[5:]

    def enable_twitch_login(self) -> None:
        if self.twitch_opt.get():
            self.twitch_login.grid(row=3, column=1)
        else:
            self.twitch_login.grid_remove()

    def next(self) -> None:
        if self.auth_token:
            self.login_frame.destroy()
            HomeGUI(self.root, self.auth_token)

    def _twitch_login(self) -> None:
        pass

    # def hide_home_frame(self) -> None:
    #     """Destroys all widgets in login_frame."""
    #     for widget in self.login_frame.winfo_children():
    #         widget.destroy()


class HomeGUI:
    def __init__(self, master, auth_code):
        self.root = master
        master.geometry("756x240")

        # Frame Declarations: User, Middle, and Queue
        self.user_frame = tk.Frame(master, bg="#2d2d2d")
        self.user_frame.grid(row=0)
        separator = tk.Frame(master, bg="#1e1e1e", width=5, height=240)
        separator.grid(row=0, column=1)
        self.queue_frame = tk.Frame(master, bg="#2d2d2d", height=240)
        self.queue_frame.grid(row=0, column=2)

        global user
        user = User(auth_code)

        # Label and Button Declarations for User Frame
        tk.Label(self.user_frame, text="Current User:", bg="#1e1e1e", fg="white", width=22,
                 font=f"{TYPE_FACE} {FONT_SIZE}").grid(row=0)

        user_name = tk.Label(self.user_frame, text=f"{user.get_display_name()}", bg="#2d2d2d", fg="white",
                             font=f"{TYPE_FACE} {FONT_SIZE + 1}")
        user_name.grid(row=1)

        tk.Label(self.user_frame, text="Current Track", bg="#1e1e1e", fg="white", width=45,
                 font=f"{TYPE_FACE} 10").grid(row=2, column=1, columnspan=2)

        # Track Title Labels
        tk.Label(self.user_frame, text="Title: ", anchor="w", bg="#1e1e1e", fg="white", width=10,
                 font=f"{TYPE_FACE} {FONT_SIZE}").grid(row=3, column=1, sticky="w")
        title_label = tk.Label(self.user_frame, textvariable=track_title, anchor="w", bg="#2d2d2d", fg="white",
                               width=35, font=f"{TYPE_FACE} {FONT_SIZE}")
        title_label.grid(row=3, column=2, sticky="w", padx=5)

        # Track Artist Labels
        tk.Label(self.user_frame, text="By: ", anchor="w", bg="#1e1e1e", fg="white", width=10,
                 font=f"{TYPE_FACE} {FONT_SIZE}").grid(row=4, column=1, sticky="w")
        artists_label = tk.Label(self.user_frame, textvariable=track_artists, bg="#2d2d2d", fg="white",
                                 width=35, anchor="w", font=f"{TYPE_FACE} {FONT_SIZE}")
        artists_label.grid(row=4, column=2, sticky="w", padx=5)

        # Track Album Labels
        tk.Label(self.user_frame, text="Album: ", anchor="w", bg="#1e1e1e", fg="white", width=10,
                 font=f"{TYPE_FACE} {FONT_SIZE}").grid(row=5, column=1, sticky="w")
        album_label = tk.Label(self.user_frame, textvariable=track_album, anchor="w", bg="#2d2d2d", fg="white",
                               width=35, font=f"{TYPE_FACE} {FONT_SIZE}")
        album_label.grid(row=5, column=2, sticky="w", padx=5)

        # Track Album Art Label
        global art_label
        art_label = tk.Label(self.user_frame, image=album_art)
        art_label.grid(row=3, padx=5, pady=10, rowspan=4)

        # Track Window Popout
        track_popout = tk.Button(self.user_frame, text="Popout Current Track", font=f"{TYPE_FACE} {FONT_SIZE}",
                                 command=self.track_popout)
        track_popout.grid(row=6, column=2, padx=5, sticky="w")

        # Label and Button Declarations for Queue Frame
        tk.Label(self.queue_frame, text="Requested Queue", bg="#1e1e1e", fg="white", width=35,
                 font=f"{TYPE_FACE} {FONT_SIZE}").grid(row=0)
        scrollbar = tk.Scrollbar(self.queue_frame)
        scrollbar.grid(row=1, sticky="e", ipady=84)

    def track_popout(self):
        """Customizable window popout to view currently playing track."""
        popout = tk.Toplevel(self.root)
        settings_menu = tk.Menu(popout)
        popout.config(menu=settings_menu)

        edit_menu = tk.Menu(settings_menu)
        settings_menu.add_cascade(label="Edit", menu=edit_menu)

        edit_menu.add_command(label="Text Settings")
        edit_menu.add_command(label="Change Background Color", command=self.change_bg_color)
        popout.title("Track")
        popout.iconbitmap(r"assets//bot_logo.ico")

        self.bg_color = tk.Label(popout, textvariable=track_info, bg="#00ff00", fg="white", font=f"{TYPE_FACE} {30}",
                                 width=45, anchor="w")
        self.bg_color.pack()

    def change_bg_color(self) -> None:
        """Provides a window popout to view possible background color changes to the track_popout window."""
        color = tk.Toplevel(self.root)
        color.title("Background Color")
        color.iconbitmap(r"assets//bot_logo.ico")

        status = StringVar()
        red = StringVar()
        green = StringVar()
        blue = StringVar()
        current_color = self.bg_color["bg"]
        bg_rgb = ImageColor.getrgb(current_color)
        status.set("Valid")
        red.set(str(bg_rgb[0]))
        green.set(str(bg_rgb[1]))
        blue.set(str(bg_rgb[2]))

        def update_color():
            """Updates current_color variable to the current red, green, and blue StringVar object values."""
            nonlocal current_color
            colors = red.get(), green.get(), blue.get()
            r, g, b = [int(c) if is_valid_rgb(c) else int(ImageColor.getrgb(preview["bg"])[i])
                       for i, c in enumerate(colors)]
            current_color = rgb_to_hex((r, g, b))

        def is_valid_rgb(value: str) -> bool:
            """Checks if value is a numeric string within RGB 0-255 inclusive boundary."""
            return 0 <= int(value) <= 255 if value.isnumeric() else False

        def preview_status():
            """Updates color preview to match current RGB Entry values if valid."""
            r, g, b = red.get(), green.get(), blue.get()
            rgb_status = [("R", is_valid_rgb(r)), ("G", is_valid_rgb(g)), ("B", is_valid_rgb(b))]
            if all([c[1] for c in rgb_status]):
                preview.config(bg=rgb_to_hex((int(r), int(g), int(b))))
                status.set("Valid")
            else:
                status_msg = f"Invalid Inputs For: " + ", ".join(f"{c[0]}" for c in rgb_status if not c[1])
                status.set(status_msg)

        def change_bg_color(bg_label: tk.Label):
            """Changes background color of Track Popout Window to match supplied valid RGB Entry values."""
            update_color()
            bg_label.config(bg=current_color)
            color.destroy()

        preview = tk.Label(color, width=25, height=10, bg=current_color)
        preview.grid(row=0, rowspan=5)

        # RED
        tk.Label(color, text='R').grid(row=2, column=1)
        tk.Entry(color, textvariable=red).grid(row=2, column=2)

        # GREEN
        tk.Label(color, text='G').grid(row=3, column=1)
        tk.Entry(color, textvariable=green).grid(row=3, column=2)

        # BLUE

        tk.Label(color, text='B').grid(row=4, column=1)
        tk.Entry(color, textvariable=blue).grid(row=4, column=2)

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
