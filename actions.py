import comtypes
import screen_brightness_control as sbc

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
        brightness=sbc.get_brightness()[0]
        step = 5
        if direction == "up":
            new = min(brightness + step, 100)
        else:
            new = max(brightness - step, 0)
        sbc.set_brightness(new)