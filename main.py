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


bot.run(TOKEN)