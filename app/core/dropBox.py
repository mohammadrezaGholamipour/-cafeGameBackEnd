import dropbox
from pathlib import Path

# مقدار توکن Dropbox را از فایل env بخوان
import os
from dotenv import load_dotenv

load_dotenv()  # فایل .env حاوی DROPBOX_TOKEN

DROPBOX_TOKEN = "sl.u.AGUns_rlcbChdGRix624q21nOZGK6EwejVQCL2WufBrNmRkHOQ-VoajSwkRAwjngAdotZEUODkTEvF7LQpytVAoRoBY0-s1ibU2Sxyb6Pl8Q8AzVRabCQ7sZ1R4eTMZuS9u3uzYyM-3ZUZ2IKjyoJtPJAL-1KNGlk7_g1ImtDOE9Mf54C6bCZtgNndNT6mlgE5Z3W9m_GadsOToBFs7Xpidfmza5J7kv7ZY5p9fawZqb6EXXt_qQyhe3cQ-mOLWzvKbangVIU0ffiTM5YyjmBlijAzk8GpmdLZxmkC0Qbz2OQOAWC-A1l0awwZ23p_yDLJ4j-0p-h3N2znBiiTohvwLzH6Hc3Si7DrgeaLSXt7F7MRnfOaKTd68d-mINXIwS88o5iJYrX92X58AfZfxoWlVNHWbqyi0qCzmnP8L-GWXfv_tUBv_mkHb0SafPiR7l-DMvwjCojGRBoQK21Uy8CEFuwvddEUvYtM6V7b43pi_KiWyZVypNvLHwx832HOZrsBtulXuKSd8K2uNJ8I0cipnt-aFniq4mhIywxAQBmHb5mcI9bnJAAHg1k__FFiOmkwKdTNBfLoD3TZhkU8nEdV1ICuEyK_CuMaDmrOPK_HD0FxQptCwe3EpE9PzzLhF0DZieRk89DmUzs0oQMLytcwXQ94XxWZCpHJIz5d_OD9PIPdey5jrar-lnDEWnPJiIcBnOgkIid4V59KGJlnbPteI8u-N911ZhIkP4WTsZpbB7KDnJf4bwQy-FIDGN2vKD-EmVD8n93lRNsDSchgCMPZMrQKpzp5fv1Xi-jknZa8oHPqQNGcnrVqSDlBbJkaF-yxBrzlghLYuNEhCfBg4PVRs4HtMhAzKd5by7304uiUHeDcMe0AR10ZLZ2aV5SLLBG6EntEtd_V_e8VYdmvcG2rPPcF55w4VvjXgi9xatWCpn2mdvhjkWMpY4ud7854WS3Pcy4n8guLOoxYfKtkHOQgSL6ceIzIfjo91uCBYHHwrR5vXDP4YtOBEGwWAYVfxhH0CB7VpntiEvxaxKFyT98FSjWRZPhx3tF34lLdlLFgZEpeDm1FafgvJ4Tcf8qMgxdDF9LXVjrZt2fWeoD3jkvP0H5Eou7lN9yBqo5uu5gvOa9xsRSU7NGcp6FqbIbBg6dfqkJL3zWodZu4bw0rQAHoOWUqQ3UtNyd6SPk7lCTpBi7rPEuVUV-wfQHvQ_BxLahFKYaTiIGTH0uvliSiJgcAqTwHToFQIFfnTCcoQyTRE_yEewVBxjF2lLR3BSPu53IXe2ZgDxjt3OoUZI9QqjIfS4NS4DfT-1DUdLv4ErXI1RDDUV9FYWM_flEj4AKFRue50"
DROPBOX_DB_PATH = "/cafeGame.db"  # مسیر فایل SQLite روی Dropbox
LOCAL_DB_PATH = Path("cafeGame.db")  # مسیر دیتابیس لوکال

dbx = dropbox.Dropbox(DROPBOX_TOKEN)


def download_db():
    """دریافت دیتابیس از Dropbox به local"""
    LOCAL_DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    try:
        metadata, res = dbx.files_download(DROPBOX_DB_PATH)
        with open(LOCAL_DB_PATH, "wb") as f:
            f.write(res.content)
        print("Database downloaded successfully!")
    except dropbox.exceptions.ApiError as e:
        print("Failed to download database:", e)
        # اگر فایل روی Dropbox وجود نداشت، دیتابیس local خالی ساخته شود
        if not LOCAL_DB_PATH.exists():
            LOCAL_DB_PATH.touch()
            print("Created empty local database.")


def upload_db():
    """آپلود دیتابیس لوکال روی Dropbox"""
    with open(LOCAL_DB_PATH, "rb") as f:
        try:
            dbx.files_upload(
                f.read(),
                DROPBOX_DB_PATH,
                mode=dropbox.files.WriteMode.overwrite  # همیشه جایگزین نسخه قبلی می‌کنه
            )
            print("Database uploaded successfully!")
        except dropbox.exceptions.ApiError as e:
            print("Failed to upload database:", e)
