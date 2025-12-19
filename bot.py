import os
import discord
from discord import app_commands
from discord.ext import commands

# ====== CONFIG ======
# Отримуємо токен та ID каналу із змінних середовища
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("❌ TOKEN environment variable is not set!")

channel_id_str = os.getenv("APPLICATION_CHANNEL_ID")
if not channel_id_str:
    raise ValueError("❌ APPLICATION_CHANNEL_ID environment variable is not set!")
APPLICATION_CHANNEL_ID = int(channel_id_str)
# ====================

# Налаштування Intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ====== EVENTS ======
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot is online as {bot.user}")


# ====== COMMAND ======
@bot.tree.command(
    name="application",
    description="Submit an application to the Rust team"
)
@app_commands.describe(
    nickname="Your Rust nickname",
    hours="How many hours you have in Rust",
    age="Your age",
    mic="Do you have a microphone? (yes / no)"
)
async def application(
    interaction: discord.Interaction,
    nickname: str,
    hours: int,
    age: int,
    mic: str
):
    # Отримуємо канал
    channel = bot.get_channel(APPLICATION_CHANNEL_ID)
    if channel is None:
        await interaction.response.send_message(
            "❌ Application channel not found. Check the channel ID.",
            ephemeral=True
        )
        return

    # Створюємо Embed
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

    # Надсилаємо Embed у канал
    await channel.send(embed=embed)

    # Підтвердження користувачу
    await interaction.response.send_message(
        "✅ Your application has been submitted!",
        ephemeral=True
    )

# ====== RUN BOT ======
bot.run(TOKEN)
