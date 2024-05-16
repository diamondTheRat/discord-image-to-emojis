import requests
from PIL import Image
import base64
from io import BytesIO
import time

################################################################################
# IF YOU WANT THIS TO WORK ON A DISCORD BOT THEN THE TOKEN SHOULD BE LIKE THIS #
#                       "Bot THE_BOTS_TOKEN"                                   #
################################################################################
discord_token = "YOUR TOKEN" # dont share this with anyone u dum dum rat


image_name = "image.png" # the image you want to convert, probably only works with png
channel_id = "channel id"
guild_id = "guild id" # you need permissions to manage emojis
delete_all_emojis = False # this deletes the emojis from the server

# the limit for this is a bit bigger than 50 for width and not that limited for height
output_size = (50, int(50 * img.height / img.width)) # keeps the width/height ratio and makes it 50 long




url = f"https://discord.com/api/v9/guilds/{guild_id}/emojis"
headers = {
    "Authorization": discord_token
}

duo = Image.open("duo.png")


def delete(_id: str):
    url = f"https://discord.com/api/v9/guilds/{guild_id}/emojis/{_id}"
    response = requests.delete(url, headers=headers)
    failed = response.status_code > 301
    while failed:
        time.sleep(3)
        response = requests.delete(url, headers=headers)
        failed = response.status_code > 301

def get_emojis():
    url = f"https://discord.com/api/v9/guilds/{guild_id}/emojis"
    response = requests.get(url, headers=headers)
    return response.json()

def purge():
    for emoji in get_emojis():
        delete(emoji["id"])

#####################################################
# EDIT THIS IF YOU WANT IT TO USE A DIFFERENT EMOJI #
#####################################################
def create_colored(color):
    new_data = [None] * duo.width * duo.height
    for i, pixel in enumerate(duo.getdata()):
        if pixel not in [(0, 0, 0, 0), (75, 75, 75, 255), (255, 255, 255, 255), (255, 222, 0, 255), (255, 194, 0, 255)]:
            if pixel == (0, 0, 0, 255):
                new_data[i] = (0, 0, 0, 0)
            else:
                new_data[i] = color
        else:
            new_data[i] = pixel

    color_str = "_".join([str(i) for i in color])
    img = Image.new("RGBA", duo.size)
    img.putdata(new_data)

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    image_binary = buffered.getvalue()

    response = requests.post(url, headers=headers, json={"name": color_str,
                                                         "image": f"data:image/png;base64,{base64.b64encode(image_binary).decode('utf-8')}"})
    failed = response.status_code > 301
    while failed:
        time.sleep(3)
        response = requests.post(url, headers=headers, json={"name": color_str, "image": f"data:image/png;base64,{base64.b64encode(image_binary).decode('utf-8')}"})
        failed = response.status_code > 301

def prep(image):
    emojis = [i["name"] for i in get_emojis()]
    for pixel in set(image.getdata()):
        if "_".join([str(i) for i in pixel]) in emojis: continue
        if type(pixel) in (tuple, list) and len(pixel) > 3 and pixel[3] == 0: continue
        create_colored(pixel)

def send(text):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    msg_data = {
            "type": 0,
            "channel_id": channel_id,
            "content": text,
            "attachments": [],
            "embeds": [],
            "timestamp": "2024-05-16T20:56:26.340000+00:00",
            "edited_timestamp": None,
            "flags": 0,
            "components": [],
            "id": "1240769857176211456",
            "author": {
                "id": "1199069471290163202",
                "username": "cheezburgerchomper",
                "avatar": "ecd1eca5ae552d9f367892879587bb3b",
                "discriminator": "0",
                "public_flags": 0,
                "flags": 0,
                "banner": None,
                "accent_color": None,
                "global_name": "CheezburgerChomper",
                "avatar_decoration_data": None,
                "banner_color": None,
                "clan": None
            },
            "mentions": [],
            "mention_roles": [],
            "pinned": False,
            "mention_everyone": False,
            "tts": False,
            "nonce": None,
            "referenced_message": None
        }

    response = requests.post(
        url,
        headers=headers,
        json=msg_data
    )
    failed = response.status_code > 300
    while failed:
        response = requests.post(
        url,
        headers=headers,
        json=msg_data
        )
        failed = response.status_code > 300

def process(image, size):
    image = image.resize(size)
    image = image.convert('P', palette=Image.ADAPTIVE, colors=40).convert("RGBA")
    image.save("rata.png")
    print("preping...")
    prep(image)
    print("done preping")
    data = list(image.getdata())
    rows = [data[i: i + image.width] for i in range(0, image.height * image.width, image.width)]
    emojis = {emoji["name"]: emoji["id"] for emoji in get_emojis()}
    for row in rows:
        message = ""
        for duo in row:
            _id = '_'.join([str(i) for i in duo])
            message += f"<:{_id}:{emojis[_id]}> "
        time.sleep(0.2)
        send(message)

if delete_all_emojis:
    print("began purging")
    purge()
    print("done purging")

img = Image.open(image_name)
process(img, output_size)

