import hikari
import lightbulb
import lavaplayer


bot = lightbulb.BotApp(
    token='OTQ5NDE2NDA1NjQyNjY2MTA2.YiKC7g.2arnqY7IgboD_1rzSt3OELKLxVg',
    default_enabled_guilds=(787634332675604511)
)
guilds = 787634332675604511
channels = 787634333245505548

lavalink = lavaplayer.LavalinkClient(
    host="localhost",  # your lavalink host
    port=2333,  # your lavalink port
    password="youshallnotpass",  # your lavalink password
    user_id=949416405642666106
)


@bot.listen(hikari.StartedEvent)
async def started_event(event):
    print('Bot has started!')
    await lavalink.create_new_node(787634332675604511)
    lavalink.connect()


@bot.command
@lightbulb.option("text", "text to repeat")
@lightbulb.command("echo", "repeats given text")
@lightbulb.implements(lightbulb.SlashCommand)
async def echo(ctx):
    await ctx.respond(ctx.options.text)
    print(ctx.options.text)


@bot.command
@lightbulb.command('music', 'connect, disconect...')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def music(ctx):
    pass


@music.child
@lightbulb.command('connect', 'connect to a voice channel')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def connect_to(ctx):
    await bot.update_voice_state(787634332675604511, 787634333245505549)
    await bot.update_voice_state(787634332675604511, 787634333245505549, self_deaf=True)
    await ctx.respond("Connected to voice channel")


@music.child
@lightbulb.command('disconnect', 'disconnect from voice channel')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def disconnect(ctx):
    await bot.update_voice_state(787634332675604511, None)
    await ctx.respond("Disconnected from voice channel")


@music.child
@lightbulb.option("music", "music link to play")
@lightbulb.command('play', 'play music')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def play(ctx):
    query = ctx.options.music
    result = await lavalink.auto_search_tracks(query)

    if result is None:
        await ctx.respond("No results found")
        return
    result = await lavalink.auto_search_tracks(query)

        # check if not found results
    if not result:
        await ctx.respond("No results found")
        return

        # Play the first result
    await lavalink.play(787634332675604511, result[0], 698867593733341194)
    await ctx.respond( f"Playing {result[0].title}")


bot.run()
