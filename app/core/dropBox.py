import dropbox
from pathlib import Path

# مقدار توکن Dropbox را از فایل env بخوان
import os
from dotenv import load_dotenv

load_dotenv()  # فایل .env حاوی DROPBOX_TOKEN

DROPBOX_TOKEN = "sl.u.AGVx8cPcvUqvJ303eA3vfKq54bwIkNCrniPMaFsVAnq6sTCaScU5byQDx1GVoAFWuseZuMRpf41-lIsMqNnOLWfde993wHn_a4irw4krrOinN9Bpwg44paQtExUTaNZ3JXOnoLejt5DYjjPZWZD-Tp9c6diHB1eGPjSJbqqWuUteJLLQKf513oIAmRCf1ODhGFyLRuL0hHC_C9esRjjVoPB8ek6wR1-wgEJkdwHwRX7CXDlm2-SnRGnTnHLDjUTqsPAdTzKm-1_vpMVLWNhdaRJYb05EUNIJ0b7PSncgqG2wH-bF64Q1wX3s43PnqZ2DPjk8x3v7lvxMjxB71YgsyShQofXCMzus1GE8q7fMviZ5MISetWB3ro2AvKuxsOvVfFdby-X35BtgGCxwxTWJnPeGrgwSvol5JnqVcCgZrqmgFZbQx1UK_VqgHhl2QqEOJv-nz4EQkr6lEcd3deHSkqKk-bO0pmy5kHpqVP5hAvMcXGYheYgrsT0iGZoN6Sad_S8u_Bpbg8ASRoxfkTXbyMygo5GUeqi1geZWVcgDdv2zQ2LVtDiiy2llR32YGGncuAvdNAcj3uICZuNYZmQWsPzyc5-hgyb0lzEMCIHE4ZvY0SmYFBWq9-7hXDv3M2CCHjYY_uwO9pSAJckU99pz9_tGKsNMEsT9mgc5eiEc8OHeXt0e8lxL7269o7-XYmNb7QLUJ0TGcCYUVUSHrCUP_zx0K_Qwm0asuLz9Kj7GAqjxZAd2UhP1e_rzD6s-kXIgEo-FJVseP86wQeUrwemh2zAHDaEpeLpb1s_DZ1cWVE-psHbI6fSxIk1De1mf0X1Wf-3Pl235grs8zprwuzB0FpKxS1mRQTSzCI7mb5mZAceueux73Bt0ZqNKjycgrTSysN-07mUtgTf3GcjWfSSfuT_EE748dQuj3Y3-Bs4Q6by2yZ6yXCzNVX36t7nmCxpSxZGsFfIqae-rjcc8u_0_teowMvJe85b5Fug6i-kV8qndmItynamvgzffOt6xI-f266Cii7r8K5T0IkgncYqjlwx-58GQgbbd5XpG6PM4RmaKT1NOZNwKKboz-t57HVlNT3bvE4bMDCfT_luRGfRJc7MX1vWPtfMBYROxkQTTLip5eY8FDWJKfENU4nb1hA_FIBztxHtumj5hGz7FeYtv6kj4UIwHEoAy3grM3j2jqffRUT1snvy8F7kaIU2PAIFAnTZrLMVgH8OPu3K_RWQWZ-WWudsb6rrYLN8nKYA80ifgI6fpMPzYCbL7thkiuHxBG7xh2A8cpLTqE4djJw3FeSxYVXnCKXOJgx8eVYLbsYUFjnnMJTtAcAuRUjTiwMgm_e0"
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
