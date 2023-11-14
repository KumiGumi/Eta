import os
import discord
import openai
import re
import requests
from discord.ext import commands
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
print("Current directory:", current_dir)  # Print the current directory

# Construct full path for .env files
discord_env_path = os.path.join(current_dir, 'discord.env')
openai_env_path = os.path.join(current_dir, 'openai.env')

# Load the environment variables
load_dotenv(discord_env_path)
print("Loaded discord.env from:", discord_env_path)  # Confirm the file path
load_dotenv(openai_env_path)
print("Loaded openai.env from:", openai_env_path)  # Confirm the file path


# Retrieve the variables
DiscordKey = os.getenv('DiscordKey')
OpenAIKey = os.getenv('OpenAiKey')

# Print the retrieved values
print("Discord Key:", DiscordKey)
print("OpenAI Key:", OpenAIKey)
