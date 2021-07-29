import requests

r  = requests.get("https://discord.com/users/@me", headers={"Authorization": "Bot ODQzNDg0NDU5MTEzNzc1MTE0.YKEiHg.cU_8UKufBY5U-13t1C1K1w1MaUY"})
print(f"Response: {r.status_code}\nMessage: {r.text}\n\nHeaders: {r.headers}")