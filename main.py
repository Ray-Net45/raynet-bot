import discord
from discord.ext import commands
from flask import Flask
import threading

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

# Event saat bot berhasil online
@bot.event
async def on_ready():
    print(f"Bot berhasil login sebagai {bot.user}")

# Command untuk memunculkan button
@bot.command()
async def form(ctx):
    class FormButton(discord.ui.View):
        @discord.ui.button(label="Buka Form", style=discord.ButtonStyle.primary)
        async def open_form(self, interaction: discord.Interaction, button: discord.ui.Button):
            class FormModal(discord.ui.Modal, title="Form Input"):
                nama = discord.ui.TextInput(label="Nama", placeholder="Masukkan nama Anda", required=True)
                barang = discord.ui.TextInput(label="Barang", placeholder="Masukkan barang Anda", required=True)
                channel_name = discord.ui.TextInput(label="Channel", placeholder="Masukkan nama channel tujuan", required=True)

                async def on_submit(self, interaction: discord.Interaction):
                    guild = interaction.guild
                    target_channel = discord.utils.get(guild.text_channels, name=self.channel_name.value)

                    if target_channel:
                        await target_channel.send(
                            f"**Data Baru Masuk!**\n**Nama**: {self.nama.value}\n**Barang**: {self.barang.value}\n**Channel Tujuan**: {self.channel_name.value}"
                        )
                        await interaction.response.send_message(
                            f"Data berhasil dikirim ke channel **{self.channel_name.value}**.",
                            ephemeral=True,
                        )
                    else:
                        await interaction.response.send_message(
                            f"Channel dengan nama **{self.channel_name.value}** tidak ditemukan.",
                            ephemeral=True,
                        )

            await interaction.response.send_modal(FormModal())

    await ctx.send("Klik tombol di bawah untuk mengisi form:", view=FormButton())

# Setup Flask untuk membuat web server
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot aktif dan berjalan!"

def run():
    app.run(host='0.0.0.0', port=8080)

# Menjalankan Flask di thread terpisah agar tidak mengganggu bot
thread = threading.Thread(target=run)
thread.start()

# Menjalankan bot
TOKEN = "MTMyMTUzMTcwNDIyOTQ5NDg1NQ.GWM4xD.ELAOH_LcyS7LuKDUdWGixbFq0KxrnuUbZ3uc-o"
bot.run(TOKEN)