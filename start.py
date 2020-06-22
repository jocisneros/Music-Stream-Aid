from multiprocessing import Process

from app import app
from gui import root, StartGUI, window_preset, repeater


def start_gui() -> None:
    """Starts Tkinter GUI (gui.py)."""
    window_preset(root)
    StartGUI(root)
    repeater(root)
    root.mainloop()


def start_web() -> None:
    """Starts Flask Web Server (app.py)."""
    app.run()


if __name__ == "__main__":
    Process(target=start_web).start()
    Process(target=start_gui).start()
