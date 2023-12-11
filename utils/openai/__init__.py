import openai
from aiohttp import ClientSession
from config import env_variables
from os import environ

openai.api_key = env_variables.OPENAI_API_KEY

environ["OPENAI_API_KEY"] = env_variables.OPENAI_API_KEY

def start_openai():
    openai.aiosession.set(ClientSession("https://api.openai.com"))
    openai.temperature = 0


async def shutdown_openai():
    await openai.aiosession.get().close()