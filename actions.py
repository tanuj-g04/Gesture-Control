import comtypes
import screen_brightness_control as sbc
import pyautogui
import numpy as np

class VolumeController:
    def __init__(self):
        comtypes.CoInitialize()
        from pycaw.pycaw import AudioUtilities
        devices = AudioUtilities.GetSpeakers()
        self.volume = devices.EndpointVolume
        self.vol_range = self.volume.GetVolumeRange()
    
    def change_volume(self, direction):
        current = self.volume.GetMasterVolumeLevel()
        step = 1.5
        if direction == "up":
            new = min(current + step, self.vol_range[1])
        else:
            new = max(current - step, self.vol_range[0])
        self.volume.SetMasterVolumeLevel(new, None)

class BrightnessController:
    def __init__(self):
        comtypes.CoInitialize()
    
    def change_brightness(self, direction):
        brightness=sbc.get_brightness(display =0)[0]
        step = 5
        if direction == "up":
            new = min(brightness + step, 100)
        else:
            new = max(brightness - step, 0)
        sbc.set_brightness(new, display=0)

class MouseController:
    def __init__(self):
        self.screen_w=1920
        self.screen_h=1080
        self.prev_x = 0
        self.prev_y = 0
        self.smoothing = 1

    # def move(self, x,y ,frame_w, frame_h):
        # screen_x = np.interp(x, [150, frame_w-150], [0, 1920])
        # screen_y = np.interp(y, [150, frame_h-150], [0, 1080])
        # curr_x = self.prev_x  + (screen_x - self.prev_x) / self.smoothing
        # curr_y = self.prev_y + (screen_y - self.prev_y) / self.smoothing
        # pyautogui.moveTo(curr_x, curr_y)
        # self.prev_x, self.prev_y = curr_x, curr_y
        
    def move(self, x, y, frame_w, frame_h):
        screen_x = np.interp(x, [100, frame_w - 100], [0, self.screen_w])
        screen_y = np.interp(y, [100, frame_h - 100], [0, self.screen_h])

        dist = ((screen_x - self.prev_x) ** 2 + (screen_y - self.prev_y) ** 2) ** 0.5

        # fast movement -> low smoothing; slow -> high smoothing
        factor = np.interp(dist, [0, 200], [8, 1.5])

        curr_x = self.prev_x + (screen_x - self.prev_x) / factor
        curr_y = self.prev_y + (screen_y - self.prev_y) / factor

        pyautogui.moveTo(curr_x, curr_y)
        self.prev_x, self.prev_y = curr_x, curr_y
    
    def click(self):
        pyautogui.click()
