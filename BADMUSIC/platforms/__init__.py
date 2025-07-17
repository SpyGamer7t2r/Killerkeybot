from .Apple import Apple
from .Carbon import Carbon
from .JioSavan import Saavn
from .Resso import Resso
from .Soundcloud import SoundCloud
from .Spotify import Spotify
from .Telegram import Telegram
from .Youtube import YouTube


class PlaTForms:
    def __init__(self):
        self.Apple = Apple()
        self.carbon = Carbon()
        self.Saavn = Saavn()
        self.Resso = Resso()
        self.Soundcloud = SoundCloud()
        self.Spotify = Spotify()
        self.telegram = Telegram()
        self.Youtube = YouTube()
