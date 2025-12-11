import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# --- Morse dictionary ---
MORSE = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.',
    'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
    'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.',
    's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
    'y': '-.--', 'z': '--..',
    '0': '-----','1': '.----','2': '..---','3': '...--','4': '....-',
    '5': '.....','6': '-....','7': '--...','8': '---..','9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.',
    '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-',
    '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-',
    '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.',
    '$': '...-..-', '@': '.--.-.'
}

# Convert text -> Morse
def text_to_morse(text: str) -> str:
    return " ".join(MORSE.get(ch, '?') if ch != ' ' else '/' for ch in text.lower())

# Convert morse -> text
def morse_to_text(morse_code: str) -> str:
    inv = {v: k for k, v in MORSE.items()}
    words = morse_code.split(" / ")
    decoded_words = []
    for word in words:
        letters = word.split()
        decoded_words.append("".join(inv.get(code, '?') for code in letters))
    return " ".join(decoded_words)

# --- Bot setup ---
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} — ready to dot-dash the universe ✨")

# -------- COMMANDS ----------
@bot.command(name="morse")
async def morse(ctx, *, message: str):
    morse_text = text_to_morse(message)
    if len(morse_text) > 1900:
        await ctx.send("Message too long babe 😭 shorten it.")
        return
    # send tagged message
    await ctx.send(f"**{ctx.author.mention} said:**\n`{morse_text}`")
    # delete user's original message
    try:
        await ctx.message.delete()
    except:
        pass

@bot.command(name="demorse")
async def demorse(ctx, *, morse_code: str):
    final_sentence = morse_to_text(morse_code)
    await ctx.send(f"**{ctx.author.mention} decoded:**\n{final_sentence}")
    # delete user's original message
    try:
        await ctx.message.delete()
    except:
        pass

# -------- RUN BOT ----------
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise SystemExit("DISCORD_TOKEN missing from .env file!")
    bot.run(token)
