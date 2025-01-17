from discord.ext import commands, tasks
import discord
import PIL
import random
import datetime
import io
import aiohttp
import scripts.catFacts as catFacts
import scripts.scraper as scraper
from scripts.robloxscrape import get_gamedata
from scripts.YoutubeSearch import youtubeSearch
from scripts.SongOfTheDay import SpotifySong
from scripts.TwitterBot import postMessage, getLastPost


class Scrapers(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        #self.bot.add_listener(self.on_raw_reaction_add, 'on_raw_reaction_add')
        self.reactionsNeeded = 1
        # add dict with guild ids for keys that tracks the reaction threshhold

    @commands.command(aliases=["catfact","cat"], description="displays a random cat fact")
    async def catFact(self, ctx: commands.Context):
        #TODO: delete this after get_fact is done
        await ctx.send("loading cat fact...")
        try:
            catFact = await catFacts.get_fact()
            await ctx.send(catFact)
        except:
            print("error while scraping page")

    @commands.command(description="displays info about dota match")
    async def display_match(self, ctx: commands.Context): # add url back to params
        #await ctx.send("fetching match...")
        #html = await scraper.call_scraper("get_match_info", url)

        thumbnail = discord.File("files/images/dotabuff.png", filename="dotabuff.png")
        embed = discord.Embed(title="bruh")
        embed.add_field(name="test 1", value="tasdfdfjlasdjf")
        embed.add_field(name="test 2", value="aldfjaldskjfd", inline=False)
        embed.add_field(name="test 3", value="\nadjfdfj", inline=False)
        embed.add_field(name="inline test", value="this is inline", inline=True)
        embed.add_field(name="inline test 2", value="this is also inline", inline=True)
        embed.set_thumbnail(url="attachment://dotabuff.png")
        embed.set_author(name=f"requested by {ctx.author.name}")

        await ctx.send(file=thumbnail, embed=embed)

        """await ctx.send(html[0])
        for h in html[1]:
            await ctx.send(h)
            asyncio.sleep(0.2)
        await ctx.send(html[2])
        for h in html[3]:
            await ctx.send(h)
            asyncio.sleep(0.2)"""

        #PIL code here
        
    @commands.command(description="displays info about user dotabuff profile")
    async def display_profile(ctx: commands.Context, url):
        await ctx.send("fetching profile...")
        html = await scraper.call_scraper("parse_profile", url)
        
        #for h in html:
            #await ctx.send(h)

    @commands.command(aliases=['rg'], description="video game 4 the gamily")
    async def robloxgame(self, ctx: commands.Context, id = ''):
        await ctx.send("Checking 4 Game!")
        async with ctx.channel.typing():
            data = await get_gamedata(id)
        if data == 1:
            await ctx.send("Game not found!")
        embed = discord.Embed(title='roblo game')
        embed.add_field(name='Title', value=data[0])
        embed.add_field(name="Player Count", value=data[1])
        embed.add_field(name="Link", value=f'[link]({data[3]})')
        embed.add_field(name="Description", value=data[4])
        embed.set_thumbnail(url=data[2]) 
        await ctx.send(embed=embed)

    @commands.command(aliases=["yt","youtubesearch","ytsearch"], description="searches and displays the top 5 youtube search results for a topic")
    async def youtube(self, ctx: commands.Context, *, searchTerm):
        async with ctx.channel.typing():
            searchTerm = "https://www.youtube.com/results?search_query=" + searchTerm
            searchTerm = searchTerm.replace(" ","+")
            #await ctx.send(searchTerm)
            thumbnails = await youtubeSearch(searchTerm)
            if thumbnails:
                print("success")
                for img in thumbnails:
                    await ctx.send(img)
            else:
                print("epic fail")
                await ctx.send(f"results scraped: {len(thumbnails)}")
            
        embed = discord.Embed(title="youtube")
        embed.set_thumbnail(url="https://i.ytimg.com/vi/b0zE0jrAUXo/hq720.jpg?sqp=-oaymwEnCNAFEJQDSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLCZVNqjADBwRPMkz8T7nzYgeaE59A")
        embed.set_image(url="https://i.ytimg.com/vi/b0zE0jrAUXo/hq720.jpg?sqp=-oaymwEnCNAFEJQDSFryq4qpAxkIARUAAIhCGAHYAQHiAQoIGBACGAY4AUAB&rs=AOn4CLCZVNqjADBwRPMkz8T7nzYgeaE59A")
        
        await ctx.send(embed=embed)
        
    #TODO: search feature
    @commands.command(aliases=["sotd","spotifysong"], description="sends a random song from a spotify album/playlist")
    async def spotify(self, ctx: commands.Context, url):
        song, apiResult = await SpotifySong(url)
        # logic to choose between album and playlist
        if apiResult == "playlist":
            songItems = song['items']
            ranSongChoice = random.choice(songItems)
            choice = ranSongChoice['track']['external_urls']['spotify']
            await ctx.send(choice)
        elif apiResult == "album":
            songItems = song['items']
            ranSongChoice = random.choice(songItems)
            choice = ranSongChoice['external_urls']['spotify']
            await ctx.send(choice)
        else:
            print("input is neither playlist nor album")

    #TODO: cmd to display latest post
    @commands.command(aliases=["bsky","bluesky","latestpost"], description="fetches last bsky post")
    async def latest(self, ctx: commands.Context):
        post = await getLastPost()
        await ctx.send(post)
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        # maybe have list of messages to ignore once react threshold is reached

        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reactions = message.reactions

        #if message.author.id == self.bot.user.id:
        #    return

        if str(payload.emoji) == "🚎":
            for reaction in reactions:
                if str(reaction.emoji) == "🚎":
                    if reaction.count == self.reactionsNeeded:
                        print("posting message")
                        #await channel.send("troll (fake)")

                        if message.attachments:# attachment in msg
                            attachment = message.attachments[0]
                            async with aiohttp.ClientSession() as session:
                                async with session.get(attachment.url) as mediaFile:
                                    if mediaFile.status == 200:
                                        data = io.BytesIO(await mediaFile.read())
                                        with open(f"files/images/{attachment.filename}","wb") as file:
                                            file.write(data.getbuffer())

                            if attachment.filename.lower().endswith(('png','jpg','jpeg','webp')):
                                # file is an image
                                img = f"files/images/{attachment.filename}"
                                if message.content:
                                    content = f"{message.content} - {message.author.name}"
                                    await postMessage(message=content, attachment=img, username=message.author.name)
                                else:
                                    await postMessage(attachment=img, username=message.author.name)

                            elif attachment.filename.lower().endswith(('mp4','webm','mov','gif')):
                                # file is a video
                                video = f"files/images/{attachment.filename}"
                                #await postMessage(attachment=video)
                                if message.content:
                                    content = f"{message.content} - {message.author.name}"
                                    await postMessage(message=message.content, attachment=video, username=message.author.name)
                                else:
                                    await postMessage(attachment=video, username=message.author.name)


                        else:# no url or attachment in msg    
                            await postMessage(f"{message.content} - {message.author.name}")
                        # end loop since correct emoji found
                        break

                        """elif message.content.startswith("http"):# url in msg
                            async with aiohttp.ClientSession() as session:
                                async with session.get(message.content) as mediaFile:
                                    if mediaFile.status == 200:
                                        data = io.BytesIO(await mediaFile.read())
                                        with open(f"files/images/{attachment.filename}","wb") as file:
                                            file.write(data.getbuffer())
                            
                            #if attachment"""


    # i dont think this works
    @tasks.loop(time=datetime.time(hour=5, minute=41))
    async def dailySong(self, ctx: commands.Context):
        channel = self.bot.get_channel(684575538957910055)
        song = await SpotifySong("https://open.spotify.com/playlist/04mZkGQA7QgVt3SPHuob76?si=AYE-9WXlSUOaixoMER3SZw")
        songItems = song['items']

        ranSongChoice = random.choice(songItems)
        choice = ranSongChoice['track']['external_urls']['spotify']

        await channel.send(choice)


def setup(bot):
    bot.add_cog(Scrapers(bot))