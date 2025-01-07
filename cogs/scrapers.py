from discord.ext import commands
import discord
import scripts.catFacts as catFacts
import scripts.scraper as scraper
import PIL

class Scrapers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="catfact", description="displays a random cat fact")
    async def catfact(self, ctx: commands.Context):
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

        thumbnail = discord.File("images/dotabuff.png", filename="dotabuff.png")
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


async def setup(bot):
    await bot.add_cog(Scrapers(bot))