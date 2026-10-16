import customtkinter as ctk
from PIL import Image
import os

# Import all your separated frames
from frames.main_menu import MainMenuFrame
from frames.settings import SettingsFrame
from frames.calibration import CalibrationFrame
from frames.ph_calib import PhCalibrationFrame
from frames.n_calib import NCalibrationFrame
from frames.k_calib import KCalibrationFrame
# from frames.start_frame import StartFrame
# from frames.history_frame import HistoryFrame

class SpadeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SPADE OS - Touch Interface")
        self.geometry("800x480")
        self.resizable(False, False)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._load_shared_images()

        self.frames = {}
        # Ensure all frames are listed here
        for F in (MainMenuFrame, SettingsFrame, CalibrationFrame, PhCalibrationFrame, NCalibrationFrame, KCalibrationFrame):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenuFrame")

    def _load_shared_images(self):
        def load_img(filename, size):
            path = os.path.join("assets", filename)
            try:
                return ctk.CTkImage(light_image=Image.open(path), size=size)
            except FileNotFoundError:
                return None

        self.img_leaf = load_img("logo.png", size=(30, 30))
        self.img_battery = load_img("battery_icon.png", size=(35, 20))
        self.img_start = load_img("play_btn.png", size=(60, 60))
        self.img_history = load_img("history_btn.png", size=(60, 60))
        self.img_settings = load_img("settings_btn.png", size=(60, 60))
        self.img_power = load_img("power_btn.png", size=(60, 60))

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = SpadeApp()
    app.mainloop()