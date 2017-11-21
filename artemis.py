# import json
import shlex

from discord.ext import commands
from sqlalchemy import create_engine

from command import Command
from config import CONFIG
from karma import process_karma

from models import Base, User, Karma, KarmaReason

bot = commands.Bot(command_prefix=commands.when_mentioned_or('?'), description="Artemis: Rhiba's bot.")
token = CONFIG['DISCORD_TOKEN']
logging = CONFIG['ENABLE_LOGGING']

# Set up database connection config
if CONFIG['DATABASE_CONNECTION']['USER'] and CONFIG['DATABASE_CONNECTION']['PASSWORD']:
    db_user = '{user}:{password}@'.format(user=CONFIG['DATABASE_CONNECTION']['USER'],
                                          password=CONFIG['DATABASE_CONNECTION']['PASSWORD'])
elif CONFIG['DATABASE_CONNECTION']['USER']:
    db_user = '{user}@'.format(user=CONFIG['DATABASE_CONNECTION']['USER'])
else:
    db_user = ''

if CONFIG['DATABASE_CONNECTION']['PORT']:
    db_port = ':{port}'.format(port=CONFIG['DATABASE_CONNECTION']['PORT'])
else:
    db_port = ''

# Initialise the database
if logging:
    print('Initialising database connection for driver: {driver}'.format(driver=CONFIG['DATABASE_CONNECTION']['DRIVER']))
db_engine = create_engine('{driver}://{user}{host}{port}'.format(
    driver=CONFIG['DATABASE_CONNECTION']['DRIVER'],
    user=db_user,
    host=CONFIG['DATABASE_CONNECTION']['HOST'],
    port=db_port
), echo=logging)

Base.metdata.create_all(db_engine)


commands = dict([(cls.__name__, cls) for cls in Command.__subclasses__()])
descriptions = dict([(cls.__name__, cls.desc()) for cls in Command.__subclasses__()])


def check_auth(user):
    # TODO: Refactor this to use SQLAlchemy
    for i in superusers:
        if i == user:
            return True
    return False


@bot.event
async def on_ready():
    print('Logged in as:')
    print(bot.user.name)
    print('------')
    print('Superusers:')
    for i in superusers:
        print(i)
    print('------')


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # add user to db if not exist
    if not str(message.author) in users and not str(message.author) in superusers:
        insert_statement = 'INSERT INTO users (name, is_superuser, can_alias) values (%s,%s,%s);'
        cursor.execute(insert_statement, (str(message.author), False, False))
        conn.commit()
        users.append(str(message.author))

    if message.content.startswith('<@' + bot.user.id + '>') or message.content.startswith('?'):
        # PIPES MOTHERFUCKER
        to_process = message.content[1:].split('|')
        to_process = [m.lstrip().rstrip() for m in to_process]
        # All commands MUST output a string
        output = []
        for command in to_process:
            pieces = shlex.split(command)
            if pieces[0] == 'help':
                if not output == []:
                    args = pieces[1:] + output
                else:
                    args = pieces[1:]
                output = commands[pieces[0]].call(message, [descriptions, args])
            elif pieces[0] in commands.keys():
                args = []
                # TODO: implement placeholder locations for output of prev command
                if not output == []:
                    args = pieces[1:] + output
                else:
                    args = pieces[1:]
                output = commands[pieces[0]].call(message, args)
            else:
                await bot.send_message(message.channel, "{0} is not a valid command. :cry:".format(pieces[0]))
                return

        if not output == []:
            out = ''
            for o in output:
                out = out + o + " "
            await bot.send_message(message.channel, out.rstrip())

    else:
        reply = process_karma(message, conn, cursor, config["karma_timeout"])
        if not reply == "":
            await bot.send_message(message.channel, reply)


if __name__ == "__main__":
    bot.run(token)
