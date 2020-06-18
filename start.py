from multiprocessing import Process
import app
from gui import AppGUI


def start_gui() -> AppGUI:
    return AppGUI()


def start_web() -> None:
    app.app.run()


if __name__ == "__main__":
    Process(target=start_gui).start()
    Process(target=start_web).start()
