import asyncio

import aiohttp as aiohttp


async def get_person(url: str):
    async with aiohttp.client.ClientSession() as session:
        async with session.get(url) as response:
            json = await response.json()
            return json


async def main():
    persons = get_person()

if __name__ == '__main__':
    # asyncio.get_event_loop().run_until_complete(main())
    asyncio.run(main())