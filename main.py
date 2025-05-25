import sys
import os
import time
import datetime
import subprocess
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup  # type: ignore
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import wolframalpha
import speech_recognition as sr
import pyaudio  # Required by speech_recognition even if unused directly
import wikipedia
from picamera import PiCamera
import dropbox
from twilio.rest import Client

"""Smart Glasses Assistant
Refactored and bug‑fixed version of the original main.py
Compatible with Raspberry Pi + OLED (SSD1306) + BlueALSA headset.
"""

# ========== Configuration ==========
contacts = {
    "Friend1": "718-822-2909",
    "Friend2": "415-586-7272",
    "Friend3": "316-316-316",
}

# Environment variables keep secrets out of source code
app_id = os.getenv("WOLFRAM_APP_ID", "")
dropbox_access_token = os.getenv("DROPBOX_ACCESS_TOKEN", "")
twilio_account_sid = os.getenv("TWILIO_SID", "")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")

twilio_client: Client | None = None
if twilio_account_sid and twilio_auth_token:
    twilio_client = Client(twilio_account_sid, twilio_auth_token)

# Characters Espeak cannot pronounce cleanly
bad_chars = [";", "|", "(", ")", "+", "=", "1"]

# OLED display initialisation
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=1)

def say(text: str) -> None:
    """Speak text via eSpeak → aplay (default ALSA device)"""
    safe = text.replace(" ", "_")
    os.system(f"espeak {safe} -ven+f3 -k5 -s130 --stdout | aplay")

def get_time() -> tuple[str, str]:
    now = datetime.datetime.now()
    return str(now.hour).zfill(2), str(now.minute).zfill(2)

def draw_oled(extra: str = "") -> None:
    """Draw clock + optional message on OLED"""
    h, m = get_time()
    with canvas(device) as draw:
        draw.text((0, 0), h, fill="white")
        draw.text((11, 0), ":", fill="white")
        draw.text((15, 0), m, fill="white")
        if extra:
            draw.text((0, 16), extra[:17], fill="white")  # 128x64 -> ~17 chars / line

# ========== I/O helpers ==========

def listen(seconds: int = 4) -> str:
    """Record audio via arecord and return Google‑ASR transcript"""
    draw_oled("…")
    os.system(f"arecord -d {seconds} -f cd -t wav test.wav")
    r = sr.Recognizer()
    try:
        with sr.AudioFile("test.wav") as src:
            audio = r.record(src)
        return r.recognize_google(audio).lower()
    except Exception as e:
        print("ASR error:", e)
        return ""

def send_sms(person: str, message: str) -> None:
    if not twilio_client:
        say("Twilio not configured")
        return
    if person not in contacts:
        say("Contact not found")
        return
    twilio_client.messages.create(
        body=message,
        from_="+YourTwilioNumber",  # Replace with verified Twilio number
        to=contacts[person],
    )

# ========== External info ==========

def query_wolfram(query: str) -> str | None:
    if not app_id:
        return None
    try:
        client = wolframalpha.Client(app_id)
        res = client.query(query)
        answer = next(res.results).text.split("\n", 1)[0]
        for c in bad_chars:
            answer = answer.replace(c, "")
        return answer
    except Exception:
        return None

def get_weather() -> str:
    answer = query_wolfram("current temperature in San Francisco")
    return answer or "Weather unavailable"

# ========== Camera / Dropbox ==========

def _next_counter(path: str) -> int:
    if not os.path.exists(path):
        return 1
    with open(path) as f:
        return int(f.read().strip() or 0) + 1

def _save_counter(path: str, value: int) -> None:
    with open(path, "w") as f:
        f.write(str(value))

def capture_photo() -> None:
    idx = _next_counter("img.txt")
    filename = f"img{idx}.jpg"
    with PiCamera() as cam:
        cam.start_preview()
        time.sleep(5)
        cam.capture(filename)
        cam.stop_preview()
    _save_counter("img.txt", idx)
    if dropbox_access_token:
        dbx = dropbox.Dropbox(dropbox_access_token)
        dbx.files_upload(open(filename, "rb").read(), f"/SmartGlassesAPI/{filename}")
    say("image saved")

def record_video(duration: int = 30) -> None:
    vid_idx = _next_counter("vid.txt")
    raw = f"vid{vid_idx}.h264"
    mp4 = raw.replace(".h264", ".mp4")
    with PiCamera() as cam:
        cam.start_recording(raw)
        time.sleep(duration)
        cam.stop_recording()
    _save_counter("vid.txt", vid_idx)
    subprocess.run(["MP4Box", "-add", raw, mp4], check=False)
    if dropbox_access_token:
        dbx = dropbox.Dropbox(dropbox_access_token)
        dbx.files_upload(open(mp4, "rb").read(), f"/SmartGlassesAPI/{mp4}")
    say("video saved")

# ========== Startup ==========

def greet() -> None:
    hour = datetime.datetime.now().hour
    if hour < 12:
        say("good morning")
    elif hour < 20:
        say("good afternoon")
    else:
        say("good evening")
    say("how may i help you")

# ========== Main ==========

def main() -> None:
    greet()
    while True:
        draw_oled()
        command = listen()
        if not command:
            continue

        if "exit" in command:
            break
        elif "news" in command:
            try:
                news_url = "https://news.google.com/news/rss"
                soup_page = soup(urlopen(news_url).read(), "xml")
                for item in soup_page.findAll("item")[:3]:
                    say(item.title.text)
                    time.sleep(1)
                draw_oled("News done")
            except Exception as e:
                print("News error:", e)
        elif "sms" in command:
            say("who to send")
            person = listen()
            say("message")
            msg = listen()
            send_sms(person, msg)
            draw_oled("SMS sent")
        elif "time" in command:
            h, m = get_time()
            say(h)
            say(m)
            draw_oled("Time")
        elif "weather" in command:
            weather = get_weather()
            say(weather)
            draw_oled(weather)
        elif "picture" in command:
            capture_photo()
            draw_oled("Photo OK")
        elif "video" in command:
            record_video()
            draw_oled("Video OK")
        else:
            answer = query_wolfram(command)
            if answer:
                say(answer)
                draw_oled(answer)
            else:
                try:
                    summary = wikipedia.summary(command, sentences=1)
                    say(summary)
                    draw_oled(summary)
                except Exception:
                    say("I didn't understand that")
                    draw_oled("Unknown cmd")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
