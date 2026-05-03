# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #
import time
import os

# ---------- BYTE CONVERTER ----------
def humanbytes(size):
    if not size:
        return "0 B"
    power = 2**10
    n = 0
    Dic_powerN = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}

    while size > power:
        size /= power
        n += 1

    return str(round(size, 2)) + " " + Dic_powerN[n]


# ---------- TIME FORMAT ----------
def time_formatter(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s"


# ---------- SIMPLE PROGRESS BAR ----------
def progress_bar(current, total):
    if total == 0:
        return "[⬡⬡⬡⬡⬡⬡⬡⬡⬡⬡] 0%"

    percent = int((current / total) * 100)
    bar = "⬢" * (percent // 10) + "⬡" * (10 - percent // 10)

    return f"[{bar}] {percent}%"

# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #
