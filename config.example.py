CONFIG = {
    # This is the discord bot token you receive when registering a new bot
    'DISCORD_TOKEN': 'token_here',
    'ENABLE_LOGGING': True,
    # This Python dict contains information on the database connection for the bot.
    # The connection string for the ORM will be made from this, i.e: sqlite:///:memory:
    'DATABASE_CONNECTION': {
        'USER': '',
        'PASSWORD': '',
        'DRIVER': 'sqlite',
        'HOST': ':memory:',
        'PORT': '',
        'LOG_ACTIVITY': True
    }
}