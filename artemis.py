import json
import shlex

import psycopg2
from discord.ext import commands

from command import Command
from karma import process_karma

bot = commands.Bot(command_prefix=commands.when_mentioned_or('?'), description="Artemis: Rhiba's bot.")
with open('creds.json') as data:
    creds = json.load(data)
with open('artemis_config.json') as data:
    config = json.load(data)
token = creds["token"]
dbinfo = creds["dbinfo"]
users = []
# Connect to db and get superusers
try:
    connect_str = "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(dbinfo["dbname"], dbinfo["user"],
                                                                             dbinfo["host"], dbinfo["password"])
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()
    cursor.execute("""SELECT name FROM users WHERE is_superuser = True;""")
    rows = cursor.fetchall()
    superusers = [i[0] for i in rows]
    cursor.execute("""SELECT name FROM users WHERE is_superuser = False;""")
    rows = cursor.fetchall()
    users = [i[0] for i in rows]
    print("Loaded users and superusers.")

except Exception as e:
    print("Could not connect to db.")
    print(e)

commands = dict([(cls.__name__, cls) for cls in Command.__subclasses__()])
descriptions = dict([(cls.__name__, cls.desc()) for cls in Command.__subclasses__()])


def check_auth(user):
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
