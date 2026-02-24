import dropbox
from pathlib import Path

# مقدار توکن Dropbox را از فایل env بخوان
import os
from dotenv import load_dotenv

load_dotenv()  # فایل .env حاوی DROPBOX_TOKEN

DROPBOX_TOKEN = "sl.u.AGWY1uRigMonI--xDb1HAS2zD5XbxCkXpyMz82OMadadNpDgDNGH8CHgVZ8TOqUWjqSGJXjiomf3sJlsNyCFKR11teTTezqNw6w9iNoIHYZ-W44BqHjW8-vlLDXZviSjWx_MzmerdiskGDnunk0AHcA3fprkfCwinpo1Od99y8lA37I-QmusXsNdysgbc_egXlb-N21NKcVyhhNWOF1f5l2KkRxrv4Ocy_nbt_iOUIS--Y8uHIYbjQ2m3-6XjrItwwSMChIiS6udRuuFQYwr1JW5mx5hDwwreC22dKRwueOzMtfOUQsgCx7lVvycLcAbdzl1NtF4DAL9NJPVbXOfeRkr2Z7WfBuePfd2gxYAhr0s2iUiD58Wpp4kd0VuIxavIf_htmfJDE1dKzbDdNCrhx_kHFlp7cxGiWTOUopQrxQZIm9mQqBxDH89HnrjM2vFUa3ftIPRgT04T7GoxKlLtT8Yw3-WM05pwLySMfkAwhkHFWQbMK5aSUbPvSVaMZGTqae1TVZRWv4aMy6A3pqVtWACsmpNFaMK-hQqS0K_kLe_mX9cRVnYbmAMNeBjOWhD4683iSZX072AAM8uj5cUDFCo7V3N4ysNZRs8iIaY3UokZD72MHLBOYFjaaeVpE3_CFmKkR4VWnDpZ1zVEY87ko9PErhofXSd_AfMpIwOgk65FcJ-5QlbHMdEN3gucG9UO6CJt05Oka3rbdmPOiakll-8YW1XeCYNxbSFW3b55lIAa6El_l1oDJrhRxo9kuWXiuPNFURtg28mGIUxwT2yq1Kh21TguMKdnKStue7apRwSx73dhsErs7Y6-0mUbdTrz92CngjobUTqyxmvtYiVTAlBbRhRmAdIIv2RQTUYwUBcDss2rFU6So3mHypxoo7IUNVLaZp-stDFuNthxRBi7ULsc_f_Ehlt7tqvVtEr14DTajejOhmVBlIbsAJA9-rvw1qfCxqb3hIWUe9NJEbzpOvgReQlQ-gsKD-cADRYfXi3bSRURCYk6aOZyNNfxLsY9xaiPh7mTuZClT2zSCPE9Jcs7adKp9nHJPYyOGLcBfWrLmrbmTHWESBCwVe37Ur3R6hI2xzXV8QwYONMAlyB0qG21vUjY8n2uG9bq5Bpf7G3eRiPAA_NpRZZJXjrA4Ii0uESzSurCDYi4uH-I_c4zWHnvmNbrlmh4W_TnjaDW-6_u3FNEoLWQyhhZUNnFBZVzJPeWgQ3ynty1Em2RpPbgt2y-s10rCrmBg0vPf-AsCYf3Erm67mjxjAA3X0OlvrKy-NHWuyLngxv_G9U_uuLEKihe3DTRnVNkwh33QkxrWf1E-K4FXjStRmRGInvDWjGPsU"
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
