import websocket
import json
import threading
from flask import Flask

DISCORD_TOKEN = ""
GUILD_ID = ""
VOICE_CHANNEL_ID = ""

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot çalışıyor ve ses kanalına bağlı!"

def start_flask():
    app.run(host='0.0.0.0', port=5000)

def on_open(ws):
    print("Bağlantı başarılı!")
    payload = {
        "op": 2,
        "d": {
            "token": DISCORD_TOKEN,
            "properties": {
                "$os": "linux",
                "$browser": "chrome",
                "$device": "chrome"
            }
        }
    }
    ws.send(json.dumps(payload))
    print("Login payload gönderildi!")

    # Bağlandıktan sonra ses kanalına gir
    join_voice_channel(ws)

def join_voice_channel(ws):
    payload = {
        "op": 4,  # Ses kanalına bağlanma
        "d": {
            "guild_id": GUILD_ID, 
            "channel_id": VOICE_CHANNEL_ID,
            "self_mute": True,  # Mikrofon kapalı
            "self_deaf": True   # Kulaklık kapalı
        }
    }
    ws.send(json.dumps(payload))
    print(f"{VOICE_CHANNEL_ID} kanalına bağlanıldı!")

def on_message(ws, message):
    try:
        data = json.loads(message)
        event_type = data.get("t")
        if event_type == "VOICE_STATE_UPDATE":
            guild_id = data["d"].get("guild_id")
            channel_id = data["d"].get("channel_id")
            print(f"GUILD_ID: {guild_id} - Ses Kanalı ID: {channel_id}")
    except json.JSONDecodeError:
        print("JSON çözümleme hatası!")

def on_error(ws, error):
    print(f"Hata: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"Bağlantı kapandı! Kodu: {close_status_code}, Mesaj: {close_msg}")

def start_ws():
    ws_url = "wss://gateway.discord.gg/?v=10&encoding=json"
    ws = websocket.WebSocketApp(ws_url, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == '__main__':
    threading.Thread(target=start_flask, daemon=True).start()
    start_ws()
