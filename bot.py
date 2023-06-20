"""
Stoa Discord Bot — !
"""

# bot.py
import discord, random, asyncio, os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv("C:/Users/xavie/Desktop/Code/Stoa/.env.txt")
TOKEN = os.environ['DISCORD_TOKEN']
GUILD = os.environ['DISCORD_GUILD']

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True

# client = discord.Client(intents=intents)
client = commands.Bot(command_prefix="/", intents=intents)

class MyHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Stoa Commands")        
        channel = self.get_destination()
        await channel.send(embed=embed)

@client.event
async def on_ready():
  for guild in client.guilds:
    if guild.name == GUILD:
      break

  print(f"\n{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})\n")
  members = "\n - ".join([member.name for member in guild.members])
  print(f"Guild Members:\n - {members}")
  channel = client.get_channel(1101997559469322290) # main
  print("\nThe Stoa has been rebuilt — !\n")
  await channel.send("The Stoa has been rebuilt — !")

  try:
    synced = await client.tree.sync()
    print(f"Synced {len(synced)} command(s)")
  except Exception as E:
    print(E)
    
@client.event
async def on_member_join(member):
  channel = client.get_channel(1099064586369511575) # welcome
  print(f"\n - {member.name} has entered the Stoa !")
  await channel.send(f"Welcome to the Stoa — {member.name} !")
  role = discord.utils.get(member.guild.roles, name="Visitors")
  await member.add_roles(role)

@client.event
async def on_message(message):
  greeting = ["Hey", "Hello", "Yo", "Hi"]
  if message.content.lower() in greeting or message.content.capitalize() in greeting:
    replies = ["Hello there! How can I assist you today?", "Welcome back! How was your day?", "Good to see you again! What can I help you with?", f"Hey, {message.author.name}! How are you doing today?", "Glad to have you here! What can I do for you?", f"Hi, {message.author.name}! What brings you to the server today?", "Welcome to the server! Is there anything I can do to assist you?", "Hey there, how's it going?", f"Greetings, {message.author.name}! How can I be of service?", "Hello and welcome! What can I help you with today?"]
    random_reply = random.randrange(len(replies))
    await message.reply(replies[random_reply])

  if 'happy birthday' in message.content.lower():
    if message.author == client.user:
        return
    else:
      await message.channel.send("Happy Birthday!  🥳🎉")
  await client.process_commands(message)

@client.command()
async def vote(ctx, message, time):
    reactions = ["<:Yes:1101982220446609589>", "<:No:1101982232245194832>"]
    embed = discord.Embed(title=f"{ctx.message.author.name}'s Vote", description=message, color=ctx.author.color)
    message = await ctx.send(embed=embed)
    for emoji in reactions:
        await message.add_reaction(emoji)

    interactions = {}
    for emoji in reactions:
        interactions[emoji] = {}

    time = float(time)
    await asyncio.sleep(time * 10)
    message = await ctx.fetch_message(message.id)

    for reaction in message.reactions:
        if str(reaction.emoji) in reactions:
            async for user in reaction.users():
                if user != client.user and user not in interactions[str(reaction.emoji)]:
                    interactions[str(reaction.emoji)].append(user)
                    react_count = reaction.count
                    if react_count(user) > 1:
                        last_reaction = None
                        async for message_reaction in message.reactions:
                            if message_reaction.emoji == reaction.emoji:
                                async for reaction_user in message_reaction.users():
                                    if reaction_user == user:
                                        last_reaction = message_reaction
                                        break
                                break
                        if last_reaction is not None:
                            await message.remove_reaction(reaction.emoji, user)

    sorted_interactions = sorted(interactions.items(), key=lambda x: len(x[1]), reverse=True)
    result = f"Results for {ctx.message.author.name}'s Vote:\n\n"
    for interaction, users in sorted_interactions:
        result += f"{interaction}   **—**   **{len(users)}**\n"

    embed = discord.Embed(title=f"{ctx.message.author.name}'s Vote Results", description=result, color=ctx.author.color)
    await ctx.send(embed=embed)

@client.command()   # Purge command — Be careful
@commands.has_role("Founders")
async def purge(ctx):
  await ctx.channel.delete()
  new_channel = await ctx.channel.clone(reason="Purge")
  await new_channel.edit(position=ctx.channel.position)
  await new_channel.send("Channel was purged succesfully — !")

@client.command()
async def member(ctx):
  member = ctx.author
  role = discord.utils.get(member.guild.roles, name="Member")
  await member.add_roles(role)

@client.command()
async def role(ctx, role):
  if role in guild.roles:
    member = ctx.author
    role = discord.utils.get(member.guild.roles, name="role")
    await member.message("Thanks for appliying — !")
    await member.add_roles(role)

@client.command()
@commands.has_role("Artists")
async def color(ctx):
    channel = client.get_channel(1099149442545889460) # art-channel
    mention = ctx.message.author.mention
    colors = ["Red", "Green", "Blue", "Yellow", "Purple"]
    message = f"Congratulations on becoming an Artist — {mention}\nPlease select a color from the following list:\n═══════════ ⋆★⋆ ═══════════\n"
    for color in colors:
        message += f"*{color}*\n"
    await channel.send(message)

    # If user changes from color role to color role update and delete the old color/s
    def check(message):
      return message.author == ctx.author and message.channel == channel

    try:
      reply = await client.wait_for("message", timeout=60.0, check=check)
    except asyncio.TimeoutError:
            await channel.send(f"{mention} didn't choose a color in time.")
    else:
      color_name = reply.content.capitalize()
      if color_name not in [color.capitalize() for color in colors]:
        await channel.send(f"Sorry {mention}, that's not a valid color choice.")
      else:
        role = discord.utils.get(ctx.guild.roles, name=color_name.capitalize())
        if role is not None:
          await ctx.author.add_roles(role)
          await channel.send(f"{mention}, you have been given the {color_name} color role!")
        else:
          await channel.send(f"Sorry {mention}, something went wrong while assigning your color role.")
    
client.run(TOKEN)
