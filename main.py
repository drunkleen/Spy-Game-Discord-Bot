from dotenv import load_dotenv
import discord
import asyncio
import random
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX')
TIME_COUNTER_SEC = int(os.getenv('TIME_COUNTER_MIN')) * 60

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents, max_messages=5000)


async def countdown(channel, spy_name, player_count):
    countdown_msg = await channel.send(f"`Countdown: {TIME_COUNTER_SEC} seconds`")
    await countdown_msg.add_reaction("⛔")

    for seconds in range(TIME_COUNTER_SEC - 1, 0, -1):
        await asyncio.sleep(1)
        await countdown_msg.edit(content=f"`Countdown: **{seconds}** seconds`")

        countdown_msg = await channel.fetch_message(countdown_msg.id)
        reaction = discord.utils.get(countdown_msg.reactions, emoji="⛔")
        if reaction and reaction.count >= player_count:
            break

    await asyncio.sleep(1)
    await countdown_msg.edit(content=f"`⏳ **Time is up!**\n` **{spy_name}** was the spy")


@bot.event
async def on_ready():
    print(f"{bot.user} is running ...")


@bot.event
async def on_message(message):
    if not message.content.startswith(PREFIX):
        return

    if message.author == bot.user:
        return

    username = message.author
    user_message = message.content
    channel = message.channel
    user_message = user_message[len(PREFIX):].strip()

    print(f"[{username}] said: '{user_message}' ({channel})")

    if user_message == "start spy" and message.author.voice and message.author.voice.channel:
        try:
            text_to_send = f"User **{message.author}** requested a game.\n`Spy Game Initializing...`"

            embed = discord.Embed(
                title="Spy",
                url="https://github.com/drunkleen/Spy-Game-Discord-Bot",
                description=text_to_send,
                color=0x00FF55
            )
            sent_message = await message.channel.send(embed=embed)

            voice_channel = message.author.voice.channel
            members_in_channel = voice_channel.members

            player_names = [x.name for x in members_in_channel]

            player_list_string = ""

            for name in player_names:
                player_list_string += f"`   - {str(name)}`\n"

            text_to_send += f"\n`⭕ List of Players:`\n{player_list_string}"

            embed = discord.Embed(
                title="Spy",
                url="https://github.com/drunkleen/Spy-Game-Discord-Bot",
                description=text_to_send,
                color=0x00FF55
            )
            await sent_message.edit(embed=embed)

            spy = random.choice(members_in_channel)
            member_index = members_in_channel.index(spy)
            members_in_channel.pop(member_index)

            with open("word_list.txt", "r", encoding="utf-8") as file:
                word_list = file.readlines()
                random_word = random.choice(word_list).strip()

            direct_message = discord.Embed(
                title="Spy Game Started",
                url="https://github.com/drunkleen/Spy-Game-Discord-Bot",
                description="`😈 You're the spy 😈`",
                color=0x5400c2
            )
            await spy.send(embed=direct_message)

            direct_message = discord.Embed(
                title="Spy Game Started",
                url="https://github.com/drunkleen/Spy-Game-Discord-Bot",
                description=f"The word is:`\n**{random_word}**",
                color=0x00FFFF
            )

            for member in members_in_channel:
                await member.send(embed=direct_message)

            embed = discord.Embed(
                title="Spy",
                url="https://github.com/drunkleen/Spy-Game-Discord-Bot",
                description=text_to_send + "\n`✅ Game Started. HF!`",
                color=0x00FF55
            )

            await sent_message.edit(embed=embed)

            await countdown(channel, spy.name, len(player_names))

            embed = discord.Embed(
                title="Spy",
                url="https://github.com/drunkleen/Spy-Game-Discord-Bot",
                description=text_to_send + "\n`✅ Game Ended!`",
                color=0x00FF55
            )

            await sent_message.edit(embed=embed)

        except Exception as e:
            await message.channel.send("Sorry, there was an error!")
            print(e)


bot.run(TOKEN)
