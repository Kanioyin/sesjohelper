import discord
from discord.ext import commands
import json
from datetime import datetime, timedelta
from config import TOKEN  # Importuj swój własny token z pliku config.py

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.command(name='add_record')
@commands.has_role('Pan & Władca')
async def add_record(ctx, date_str: str, *members: discord.Member):
    date = datetime.strptime(date_str, '%Y-%m-%d').date()

    try:
        with open('records.json', 'r') as file:
            records = json.load(file)
    except FileNotFoundError:
        records = {}
    records[str(date)] = [member.id for member in members]

    with open('records.json', 'w') as file:
        json.dump(records, file)

@bot.command(name='list_records')
async def list_records(ctx):
    try:
        with open('records.json', 'r') as file:
            records = json.load(file)
    except FileNotFoundError:
        records = {}

    if not records:
        await ctx.send('Brak zapisanych rekordów.')
        return

    for date, members in records.items():
        date_str = datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')
        member_names = [ctx.guild.get_member(member_id).display_name for member_id in members]
        members_str = ', '.join(member_names)
        await ctx.send(f'{date_str}: {members_str}')

@bot.command(name='ile_wolnego')
async def ile_wolnego(ctx):
    try:
        with open('records.json', 'r') as file:
            records = json.load(file)
    except FileNotFoundError:
        await ctx.send('Albo Cię nie było albo coś zjebałem')
        return

    user_id = ctx.author.id

    latest_date = max(records, key=lambda x: datetime.strptime(x, '%Y-%m-%d'))

    if user_id in records[latest_date]:
        await ctx.send('Byłeś na ostatniej sesji dzbanie.')
        return

    for date in reversed(sorted(records.keys())):
        if user_id in records[date]:
            user_date = datetime.strptime(date, '%Y-%m-%d').date()
            latest_date = datetime.strptime(latest_date, '%Y-%m-%d').date()
            difference = latest_date - user_date
            await ctx.send(f'{ctx.author.display_name} ma wolne od ostatniej daty przez {difference.days} dni.')
            return

# Dodaj funkcje do przypisywania roli na podstawie reakcji
@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    role_message_id = 1244395920775319625  # Zamień na ID twojej wiadomości
    role1_id = 1244391784185069639  # świerzak
    role2_id = 1244394043044266024  # CPTG
    role3_id = 338030590257266688  # basic
    emoji1 = 'moai'
    emoji2 = 'Ez'
    emoji3 = 'JP'

    print(f"Emoji added: {payload.emoji.name}")

    if payload.message_id == role_message_id:
        member = guild.get_member(payload.user_id)
        if member is None:
            return

        if payload.emoji.name == emoji1:
            role = guild.get_role(role1_id)
        elif payload.emoji.name == emoji2:
            role = guild.get_role(role2_id)
        elif payload.emoji.name == emoji3:
            role = guild.get_role(role3_id)
        else:
            role = None

        if role is not None:
            await member.add_roles(role)
            print(f"Added {role.name} to {member.display_name}")

@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    role_message_id = 1244395920775319625  # Zamień na ID twojej wiadomości
    role1_id = 1244391784185069639  # świerzak
    role2_id = 1244394043044266024  # CPTG
    role3_id = 338030590257266688  # basic
    emoji1 = 'Czad'
    emoji2 = 'Ez'
    emoji3 = 'JP'

    print(f"Emoji removed: {payload.emoji.name}")

    if payload.message_id == role_message_id:
        member = guild.get_member(payload.user_id)
        if member is None:
            return

        if payload.emoji.name == emoji1:
            role = guild.get_role(role1_id)
        elif payload.emoji.name == emoji2:
            role = guild.get_role(role2_id)
        elif payload.emoji.name == emoji3:
            role = guild.get_role(role3_id)
        else:
            role = None

        if role is not None:
            await member.remove_roles(role)
            print(f"Removed {role.name} from {member.display_name}")

bot.run(TOKEN)
