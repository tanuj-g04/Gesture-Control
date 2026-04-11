from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class VolumeController:
    def __init__(self):
        devices=AudioUtilities.GetSpeakers()
        self.volume=devices.EndpointVolume
        self.vol_range=self.volume.GetVolumeRange()

    def set_volume(self, level):
        db=self.vol_range[0] + (level/100)*(self.vol_range[1]-self.vol_range[0])
        self.volume.SetMasterVolumeLevel(db, None)