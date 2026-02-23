import dropbox
from pathlib import Path

# مقدار توکن Dropbox را از فایل env بخوان
import os
from dotenv import load_dotenv

load_dotenv()  # فایل .env حاوی DROPBOX_TOKEN

DROPBOX_TOKEN = "sl.u.AGVG2QVkYL1dsenmpeB3gc6dDpnbYYb9RYudcRu4_ahI8P6M8Y8SQVJjrExNLJVE-vGsdLGBLzQYWy13tE5_24Gl24v5CybbY5qnKcoAAIX0YPaHQERR1DNSzNCrmuaQYmiTDv6y7dpuYSgR586u4pp9VNmZ-k0ROhCUTLlqczwVW2mem9zceA4KtgoCO_6_Wwel8Ef8M7ijcS9JEoznjqqkpn6owFK2uPXMlVX1G_elYj9kj0puyl9rMKZ0PLLxhiOfSP2cZUi61-5BBmHovyzIfyWuFnvRHXmkpS75BSvmTDkdm2mf5xcbwmqa7pKHxCwC7RZrCRKpcIkYnVcxRCoA2Sz97LMIID4GA-cdqfKJ9JaUj1fICN_yOCuVj9hMpZLxfkpJZdJ61vkVZlt6ZmZIXu_1Z_o2Lz7PbqNDLgnmEkcAorbdrCE167OlNvcHJpTgEqIlf556TMUKebYWRn5KI0VldKZA7GQ1uqMFxUJz3PU0VwmzuRaewaEM2UvPQEILvOsqKUGYJ6rcfiG71nVKJNh3FZ4wHcX15MDwmuKyIsNYxxyO26veJ-WsSa5PiujxooGG4xkqJYwnUY0IdCeMaDw4eHpZDhSuLhJGaKt-e9M5CAHsdVET4scOM8XjJFD2g1QY69lLzAi1p_G7V01CfTmfWxkeK8T0a_ELhJf01GTguYb3NQAVTh3YyWUQXoo6cPN5dkZiAq3bHujb107-K-Suwi-Xfn58Eogps3lzSWHh0_RO7u4MUxkQ6h1zH8sbJq-Pss_RbwpnN7BPFTG0hmco5yY_KBN5avlXqNSpmBBtY5A9EptSV4B6O2inrFUP3FoOc5_l-w-MGqggUCpkXNcYboHCiEHvK0jcDjrQTaB_S34-pe3kpMw9T91MyTzZsQ9RfHTAPJBzt63kMqEmEBZKG-FF0ZtXPylUio_JGI354cNDhYnc9E_2ely7jh7mu8ijn4rVkJzlnz17UrXbGLBYXANpwQDTMWQSqPAAbsGZ8DAWJXUorc9lu5-cRx-ss-bqIMBaPHW7Qj4l0E9CsPTVXc5XuEFfIZ6ktRoSM0bsf9_kCZrcoAkSNQec6DfE4Seu_TQDI4l_MaGpZxLJRv-ZgdzlD3rwuxx02aSnA-pYiiJK_ue9qu8UBWK58ljlRJGMVisKyW144F3dwrqEDI4wassgxUVWM9gaB6sAFUsqX7rOdMYMeyxGohEoLI8r07GtyxZF-ET9jNVc--br5e_hvTAWQrCLFHPwCNe4dHbba3Mg3XJDyV74WEmo0YKgLEKvrpNeRSeH0dz9p6bsDmMfyL9j7fTxJkU9FvTzcbLmW7R-TJOPxvmuS-CdgoE"
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
