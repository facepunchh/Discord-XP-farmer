import discord
import asyncio
import random
import sys

# SETTINGS, U CAN CHANGE IT IF U WANT

MESSAGES = [
    "lol", "ok", "hmm", "wtf", "??",
    "maybe", "idk", "real", "fr", "same",
    "nuh uh", "wow", "wait", "what?", "yeah",
    "bruh", "well", "kinda", "jesus", "no"
]


DELAY_MIN = 65
DELAY_MAX = 140

# ------------------------------------------------------------

try:
    print("==========================================")
    print("Made by facepunchh")
    print("==========================================")
    TOKEN = input("Your token: ").strip().replace('"', '')
    VOICE_CHANNEL_ID = int(input("ID of the channel (voice): ").strip())
    TEXT_CHANNEL_ID = int(input("ID of the channel (chat): ").strip())
    print("-------------------------")
except ValueError:
    print("Channel IDs must consist only of numbers")
    sys.exit()


# ------------------------------------------------------------

class MySelfBot(discord.Client):
    def __init__(self):
        super().__init__()

    async def on_ready(self):
        print(f'Logged in as: {self.user} (ID: {self.user.id})')
        print(f'Phrases to chat farm: {len(MESSAGES)}')
        print('Starting now..')
        self.loop.create_task(self.join_voice())
        self.loop.create_task(self.auto_chat())

    async def join_voice(self):
        await self.wait_until_ready()
        try:
            channel = self.get_channel(VOICE_CHANNEL_ID)
            if not channel:
                print("VC is not found, check the id")
                return
            await channel.connect(self_deaf=True, self_mute=True)

            print(f"Joined the vc: {channel.name}")
        except Exception as e:
            print(f"Couldn't join the vc: {e}")

    async def auto_chat(self):
        await self.wait_until_ready()
        channel = self.get_channel(TEXT_CHANNEL_ID)

        if not channel:
            print("Channel is not found")
            return

        print(f"Starting farming msgs in: {channel.name}")
        while not self.is_closed():
            try:
                msg = random.choice(MESSAGES)
                async with channel.typing():
                    await asyncio.sleep(random.randint(1, 3))
                await channel.send(msg)
                print(f"Sent: {msg}")

                wait_time = random.randint(DELAY_MIN, DELAY_MAX)
                print(f"Sleeping: {wait_time} seconds")
                await asyncio.sleep(wait_time)

            except Exception as e:
                print(f"Error, waiting: {e}")
                await asyncio.sleep(20)


if __name__ == "__main__":
    try:
        client = MySelfBot()
        client.run(TOKEN)
    except Exception as e:
        print(f"error, make sure that your token is valid: {e}")
