# importing the lavaplayer package
import lavaplayer
# import a discord client like: hikari, discord.py, etc...
import hikari

# create a hikari client to get a events
bot = hikari.GatewayBot("OTQ5NDE2NDA1NjQyNjY2MTA2.YiKC7g.2arnqY7IgboD_1rzSt3OELKLxVg")

# create a lavaplayer client
lavalink = lavaplayer.LavalinkClient(
    host="localhost",  # your lavalink host
    port=2333,  # your lavalink port
    password="youshallnotpass",  # your lavalink password
    user_id=949416405642666106  # your bot id
)

# the started event is called when the client is ready
@bot.listen(hikari.StartedEvent)
async def started_event(event):
    await lavalink.create_new_node(787634332675604511)
    # connect the lavaplayer client to the hikari client
    lavalink.connect()

# the message event is called when a message is sent
@bot.listen(hikari.GuildMessageCreateEvent)
async def message_event(event: hikari.GuildMessageCreateEvent):
    if not event.message:
        return

    # This command to connect to your voice channel
    if event.message.content == "!join":
        # get the voice channel
        states = bot.cache.get_voice_states_view_for_guild(event.guild_id)
        voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == event.author_id)]

        # check if the author is in a voice channel
        if not voice_state:
            await bot.rest.create_message(event.channel_id, "You are not in a voice channel")
            return

        # connect to the voice channel
        channel_id = voice_state[0].channel_id
        await bot.update_voice_state(event.guild_id, channel_id, self_deaf=True)
        await bot.rest.create_message(event.get_channel(), f"Connected to <#{channel_id}>")

    # This command to play a song
    elif event.message.content.startswith("!play"):
        # get a query from the message
        query = event.message.content.replace("!play", "")
        print(query)

        # check if the query is empty
        if not query:
            await bot.rest.create_message(event.channel.id, "Please provide a track to play")
            return

        # Search for the query
        result = await lavalink.auto_search_tracks(query)

        # check if not found results
        if not result:
            await bot.rest.create_message(event.channel.id, "No results found")
            return

        # Play the first result
        await lavalink.play(event.guild_id, result[0], event.author_id)


# the voice_state_update event is called when a user changes voice channel
"""@bot.listen(hikari.VoiceStateUpdateEvent)
async def voice_state_update(v: hikari.VoiceStateUpdateEvent):
    try:
        event: hikari.VoiceServerUpdateEvent = await bot.wait_for(hikari.VoiceServerUpdateEvent, timeout=30)
    except :
        return
    # Update the lavaplayer client with the new voice server
    await lavalink.voice_update(v.guild_id, v.state.session_id, event.token, event.raw_endpoint)"""


# run the bot
bot.run()