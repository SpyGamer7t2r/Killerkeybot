import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# ───── Telegram Bot Configs ───── #
API_ID = int(getenv("API_ID", "22565342"))
API_HASH = getenv("API_HASH", "75e035926f72f2f4155a6f5f6e64be03")
BOT_TOKEN = getenv("BOT_TOKEN", "7684739810:AAG9p4WZU4-u1s9-JXzU3l9Hig7yCjSb2Yo")
OWNER_ID = int(getenv("OWNER_ID", 7487670897))
LOGGER_ID = int(getenv("LOGGER_ID", -1002781150474))
STRING1 = getenv("STRING_SESSION", "BQFYUd4AC68E3CzCrdtJSCj7EpKfhi_Vy8EVgF-JMFrDJDAsmP98ZNTP28pOPC92xnnpFiyetUyp1H6YoNol0YnG984uWI-WatXAuqoVPYVgLquWC1OR4XEsq-Ex2O3By5anXltoagCT0j_YinmxgpXMwrM2e6aWjHshplknALJ0X6A35QUGpdO5yNpM9wqgjfgLM_160U6LUuiVEoYYv27KacT9Bymc6z8Y73ikcFPsbE_JcfEbT0eWfWvDIOiZBc6x9UbB40XqQGz9qrrwZe9wuBRmv7y-l_VaFUS59wQMkkDJsQGqGBHoTHato4zJ8lA_PN6vOkLBCmbM3F9VYnMrDc8txgAAAAG-K06AAA")
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

# ───── MongoDB ───── #
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://knight4563:knight4563@cluster0.a5br0se.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# ───── Bot Branding ───── #
BOT_NAME = getenv("BOT_NAME", "Killer Key")
BOT_USERNAME = getenv("BOT_USERNAME", "killerkey_bot")
OWNER_USERNAME = getenv("OWNER_USERNAME", "your_username_here")

# ───── Media Duration & Limits ───── #
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 180))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))  # 100MB
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 1073741824))  # 1GB
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))

# ───── Heroku ───── #
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# ───── Git Auto Pull ───── #
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/SpyGamer7t2r/Killerkeybot")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "Bad")
GIT_TOKEN = getenv("GIT_TOKEN", None)

# ───── Support ───── #
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/dark_x_knight_musiczz_support")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/dark_knight_support")

# ───── Spotify ───── #
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", None)

# ───── Assistant Behavior ───── #
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))

# ───── Images (Branding) ───── #
IMG_LINK = "https://graph.org/file/6165bc89f53da9846f83b-61cca9647e63e5f7da.jpg"
START_IMG_URL = getenv("START_IMG_URL", IMG_LINK)
PING_IMG_URL = getenv("PING_IMG_URL", IMG_LINK)
PLAYLIST_IMG_URL = IMG_LINK
STATS_IMG_URL = IMG_LINK
TELEGRAM_AUDIO_URL = IMG_LINK
TELEGRAM_VIDEO_URL = IMG_LINK
STREAM_IMG_URL = IMG_LINK
SOUNCLOUD_IMG_URL = IMG_LINK
YOUTUBE_IMG_URL = IMG_LINK
SPOTIFY_ARTIST_IMG_URL = IMG_LINK
SPOTIFY_ALBUM_IMG_URL = IMG_LINK
SPOTIFY_PLAYLIST_IMG_URL = IMG_LINK

# ───── Bot Internals ───── #
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

# ───── Time Conversion ───── #
def time_to_seconds(time):
    return sum(int(x) * 60**i for i, x in enumerate(reversed(str(time).split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

# ───── URL Validations ───── #
if SUPPORT_CHANNEL and not re.match("(?:http|https)://", SUPPORT_CHANNEL):
    raise SystemExit("[ERROR] - SUPPORT_CHANNEL must start with http:// or https://")

if SUPPORT_CHAT and not re.match("(?:http|https)://", SUPPORT_CHAT):
    raise SystemExit("[ERROR] - SUPPORT_CHAT must start with http:// or https://")
