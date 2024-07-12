import os
import sys
import json
import time
import asyncio
from pathlib import Path
from itertools import cycle
from datetime import datetime
from difflib import get_close_matches

# Discord Modules
import discord
from discord import app_commands
from discord.ext import commands, tasks

'''
This the Discord version of the Iris chatbot.
10 July 2024 N34R

<<->> hic sunt dracones <<->>
'''

# Settings
bot_prompt = "Iris: "
user_prompt = ">> "
default_notfound_error = "I don't know how to respond. Please teach me or type [SKIP]."
default_iris_thank = "Thank you! I learnt a new thing."

space = "     "
# Utils
now = datetime.now()
login_time = now.strftime("%Z %d/%b/%Y %H:%M:%S")
logfile = Path("D:\\IRIS.log")

# Colour Code Functions
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))

os.system('title ProjectIRIS Central Controller')

# Client Settings
intents = discord.Intents.all()
client = commands.AutoShardedBot(command_prefix=".", help_command=None, intents=intents)
script_dir = Path(__file__).parent

# Bot Status
status_cycle = ["with papa", "Minecraft"]
status = cycle(status_cycle)

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

# Connect
@client.event
async def on_ready():
    logfile = Path("D:\\IRIS.log")
    if logfile.is_file():
        logfile = open(r"D:\\IRIS.log", "a")
        prYellow(f"[{login_time}] [INFO] Log file exists in file path.")
    else:
        logfile = open(r"D:\\IRIS.log", "a")
        logfile.write(f"Project IRIS Console Log \nCreated on {login_time} \n<->=============================<->")
        prYellow(f"[{login_time}] [INFO] Log file does not exist.")
        prYellow(f"[{login_time}] [INFO] New log file created.")

    for server in client.guilds:
        await client.tree.sync(guild=discord.Object(id=server.id))
    change_status.start()
    prYellow(f"[{login_time}] [INFO] Iris has logged in.")
    logfile.write(f"\n[{login_time}] [INFO] Iris has logged in.")
    prRed('<=>--------------------------------<=>')
    prLightGray(f"{space}Logged in as {client.user}")
    prLightGray(f"{space}User ID: {client.user.id}")
    prLightGray(f"{space}Logged in at {login_time}")
    prLightGray(f"{space}Discord Version: {discord.__version__}")
    prLightGray(f"{space}Python Version: {sys.version}")
    prRed('<=>--------------------------------<=>')

    server = len(client.guilds)
    server_count = int(server)

    prLightGray(f"{space}Connected to")
    prLightGray(f"{space}{server_count} Discord Guilds")
    prRed('<=>--------------------------------<=>')
    guild_number = 0
    for guild in client.guilds:
      guild_number = guild_number + 1
      prLightGray(f"{space}[{guild_number}] {guild} | ID:{guild.id} | {guild.owner}")
    prRed('<=>--------------------------------<=>')


# Load knowledge base
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        data: dict = json.load(file)
    return data


# Save new response to knowledge base
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


# Find prompt that is 60% similar to input
def find_best_match(user_prompt: str, prompts: list[str]) -> str | None:
    matches: list = get_close_matches(user_prompt, prompts, n=1, cutoff=0.6)
    return matches[0] if matches else None


# Get the response for the prompt if found
def get_response_for_prompt(prompt: str, knowledge_base: dict) -> str | None:
    for p in knowledge_base["prompts"]:
        if p["prompt"] == prompt:
            return p["response"]


# Load Channel JSON
json_file_path = script_dir / 'channels.json'
def load_channel_json():
    with open(json_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# Function to check if channel ID exists in JSON
def is_channel_id_in_json(channel_id, json_data):
    for channel_name, channel_info in json_data["channels"].items():
        if channel_info["channel_id"] == channel_id:
            return True
    return False

channel_data = load_channel_json()


# Function to get file_name by channel_id
def get_file_name_by_channel_id(channel_id, json_data):
    for channel_name, channel_info in json_data["channels"].items():
        if channel_info["channel_id"] == channel_id:
            return channel_info["file_name"]
    return None


learning_mode = {}

# Main Function
async def main(user_prompt, file_path):
    knowledge_base = load_knowledge_base(file_path)
    user_id = user_prompt.author.id
    channel_id = user_prompt.channel.id

    # Skip processing if the bot is in learning mode for this user in this channel
    if learning_mode.get(user_id) == channel_id:
        return

    best_match = find_best_match(user_prompt.content, [p["prompt"] for p in knowledge_base["prompts"]])

    if best_match:
        response = get_response_for_prompt(best_match, knowledge_base)
        await user_prompt.channel.send(response)
        print(response)
    else:
        await user_prompt.channel.send(default_notfound_error)
        print(default_notfound_error)

        def check(m):
            return m.author == user_prompt.author and m.channel == user_prompt.channel

        learning_mode[user_id] = channel_id  # Set learning mode

        try:
            new_message = await client.wait_for('message', check=check, timeout=60.0)
            new_response = new_message.content

            if new_response.lower() != "skip":
                knowledge_base["prompts"].append({"prompt": user_prompt.content, "response": new_response})
                save_knowledge_base(file_path, knowledge_base)
                await user_prompt.channel.send(default_iris_thank)
                print(default_iris_thank)
        except asyncio.TimeoutError:
            await user_prompt.channel.send("Timed out waiting for a response.")
        finally:
            del learning_mode[user_id]  # Reset learning mode

# Listen to messages
@client.event
async def on_message(message):
    # Skip if author is self
    if message.author.id == client.user.id:
        return

    # Skip if message starts with >
    if message.content.startswith(">"):
        return

    channel_id_to_check = message.channel.id
    if is_channel_id_in_json(channel_id_to_check, channel_data):
        pass
    else:
        return

    print(f"{message.author.name} {user_prompt}{message.content}")

    # Knowledge base directory
    knowledgebase_folder = "Knowledgebase"
    knowledgebase_file = get_file_name_by_channel_id(message.channel.id, channel_data)
    current_directory = os.getcwd()
    file_path = os.path.abspath(os.path.join(current_directory, knowledgebase_folder, knowledgebase_file))
    await main(message, file_path)


## Run Program
if __name__ == "__main__":
    token = "token"
    client.run(token)
    main()
