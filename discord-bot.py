import discord
from discord import app_commands

from modules.logger.logger import Logger
from modules.config.config import Config

NAME = "discord-bot"
CLIENT_ID = ""
INVITE = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&permissions=8&scope=bot%20applications.commands"
LOGGER = None
CONFIG = None


class Kara(discord.Client):
	def __init__(self, logger, config):
		super().__init__(intents = discord.Intents.default())
		self.synced = False
		self.log = logger
		self.cfg = config

	async def on_ready(self):
		await self.wait_until_ready()
		if not self.synced:
			await TREE.sync()
			self.synced = True
			self.log = LOGGER
			self.cfg = CONFIG
		self.log.info(f"Initialization '{self.user}' complete")


CLIENT = Kara(LOGGER, CONFIG)
TREE = app_commands.CommandTree(CLIENT)


@TREE.command(name = "test", description = "I am command!")
async def self(interaction: discord.Interaction, name: str):
	await interaction.response.send_message(f"Hello {name}! I am Valky's new bot, created as a ValKore module!")

@TREE.command(name = "hidden", description = "I am command, but hidden!")
async def self(interaction: discord.Interaction, name: str):
	await interaction.response.send_message(f"Hello {name}! I am Valky's new bot, created as a ValKore module!", ephemeral = True)


def run(logger):

	global LOGGER, CONFIG
	if logger is None:
		BASE = "."
		LOGGER = Logger(name=NAME)
	else:
		BASE = f"./modules/{NAME}"
		LOGGER = logger

	CONFIG = Config(path=f"{BASE}/config.ini").readConfig()
	LOGGER.info(f"Starting {CONFIG['VKore']['name']}")

	CLIENT.run(CONFIG['Settings']['token'])

# start up wot
if __name__ == '__main__':
	run(None)
