import asyncio
from pprint import pprint

import aiohttp as aiohttp

LINK = "https://swapi.dev/api/people/"


async def make_request(url: str):
    async with aiohttp.client.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def get_persons(count: int = 25):
    tasks = [asyncio.create_task(make_request(f'{LINK}{count}')) for _ in range(1, count + 1)]
    return await asyncio.gather(*tasks)


async def main():
    persons = await get_persons()
    pprint(persons)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    # asyncio.run(main())