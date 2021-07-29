import requests
import variables as var

headers = {
    "Authorization": "Bot "+ var.TOKEN
}

r  = requests.get("https://discord.com/users/@me", headers=headers)
print(f"Response: {r.status_code}\nHeaders: {r.headers}")