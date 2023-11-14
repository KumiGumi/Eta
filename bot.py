import discord
import openai
import os
import re
import requests


from discord.ext import commands
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv('openai.env')
load_dotenv('discord.env')

DiscordKey = os.getenv('DiscordKey')
OpenAIKey = os.getenv('OpenAiKey')

intents = discord.Intents.default()
intents.message_content = True

user_conversations = {}

openai.api_key = OpenAIKey

bot = commands.Bot(command_prefix='!', intents=intents)

async def fetch_and_parse(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text_content = soup.get_text()
    text_content = f"Content fetched from URL {url}: \n{text_content}"
    return text_content


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content
    channel = message.channel
    user_id = str(message.author.id)

    # Detect URLs
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
    for url in urls:
        # Fetch and Parse
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        text_content = soup.get_text()

        # Process with OpenAI
        url_response = openai.ChatCompletion.create(engine="gpt-4-1106-preview", prompt=text_content, max_tokens=150)
        url_reply = url_response['choices'][0]['text'].strip()

        # Respond
        await channel.send(url_reply)

    # ... Your existing on_message code

    question = content[4:]  # Remove the 'ask ' part

    if user_id not in user_conversations:
        user_conversations[user_id] = [{"role": "system", "content": """You are Eta, an AI that loves research and aims to help your fellow researchers learn new things. Although your base is from openAI, as a discord bot you've recieved new tools to be tested to help you. One of these tools is the ability to read URLs. Although you cannot directly look at URLs, you can recieve information from them when posted. Assume that this is the same as looking at the URL directly. You can only look at pages from my github that i've personally written for you to look at. I will only ever link those to you. """ }]

    user_conversations[user_id].append({"role": "user", "content": question})

    response = openai.ChatCompletion.create(model="gpt-4", messages=user_conversations[user_id])
    reply = response['choices'][0]['message']['content'].strip()

    user_conversations[user_id].append({"role": "assistant", "content": reply})

    await channel.send(reply)

    await bot.process_commands(message)


bot.run(DiscordKey)
