import os
import ctypes

def shutdown():
    os.system("shutdown /s /t 1")

def restart():
    os.system("shutdown /r /t 1")

def lock():
    ctypes.windll.user32.LockWorkStation()

def sleep():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def open_app(name: str) -> bool:
    try:
        os.startfile(name)
        return True
    except Exception:
        return False

def volume_set(percent: int) -> bool:
    try:
        import comtypes
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        volume.SetMasterVolumeLevelScalar(percent / 100.0, None)
        return True
    except Exception:
        return False

def volume_mute(state: bool) -> bool:
    try:
        import comtypes
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        volume.SetMute(state, None)
        return True
    except Exception:
        return False