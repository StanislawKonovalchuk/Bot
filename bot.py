import os
import discord
from discord import app_commands
from discord.ext import commands

# ===== CONFIG =====
TOKEN = os.getenv("TOKEN")  # token from Railway
APPLICATION_CHANNEL_ID = int(os.getenv("APPLICATION_CHANNEL_ID"))
# ==================

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot is online as {bot.user}")


@bot.tree.command(
    name="aplication",
    description="Submit an application to the Rust team"
)
@app_commands.describe(
    nickname="Your Rust nickname",
    hours="How many hours you have in Rust",
    age="Your age",
    mic="Do you have a microphone? (yes / no)"
)
async def aplication(
    interaction: discord.Interaction,
    nickname: str,
    hours: int,
    age: int,
    mic: str
):
    channel = bot.get_channel(APPLICATION_CHANNEL_ID)

    if channel is None:
        await interaction.response.send_message(
            "❌ Application channel not found.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="🛠 NEW RUST APPLICATION",
        description="A new application has been submitted",
        color=discord.Color.orange()
    )

    embed.add_field(name="👤 Discord User", value=interaction.user.mention, inline=False)
    embed.add_field(name="🎮 Rust Nickname", value=nickname, inline=True)
    embed.add_field(name="⏱ Hours", value=str(hours), inline=True)
    embed.add_field(name="🎂 Age", value=str(age), inline=True)
    embed.add_field(name="🎧 Microphone", value=mic, inline=True)

    embed.set_footer(text="Rust Application Bot")
    embed.timestamp = discord.utils.utcnow()

    await channel.send(embed=embed)

    await interaction.response.send_message(
        "✅ Your application has been submitted!",
        ephemeral=True
    )


bot.run(TOKEN)