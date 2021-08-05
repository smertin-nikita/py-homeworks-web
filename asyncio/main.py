import os

import db_config
import asyncio
from pprint import pprint

import aiohttp as aiohttp
import requests
from models import SwPeople, db


async def make_request(session, url: str):
    async with session.get(url) as response:
        return await response.json()


async def get_films(films_uri):
    async with aiohttp.client.ClientSession() as session:
        tasks = [asyncio.create_task(make_request(session, f'{uri}')) for uri in films_uri]
        return await asyncio.gather(*tasks)


async def get_names(items_uri):
    items = await get_films(items_uri)
    return ', '.join(item.get('title', item.get('name')) for item in items)


async def get_persons(count: int = 5):
    async with aiohttp.client.ClientSession() as session:
        link = "https://swapi.dev/api/people/"
        tasks = [asyncio.create_task(make_request(session, f'{link}{_}')) for _ in range(1, count + 1)]
        return await asyncio.gather(*tasks)


async def insert_to_db(data):
    person = await SwPeople.create(
        birth_year=data['birth_year'],
        eye_color=data['eye_color'],
        films=await get_names(data['films']),
        gender=data['gender'],
        hair_color=data['hair_color'],
        height=int(data['height']),
        homeworld=requests.get(data['homeworld']).json()['name'],
        mass=data['mass'],
        name=data['name'],
        skin_color=data['skin_color'],
        species=await get_names(data['species']),
        starships=await get_names(data['starships']),
        vehicles=await get_names(data['vehicles'])
    )

    await person.create()


async def write_to_db(persons):
    tasks = [asyncio.ensure_future(insert_to_db(person)) for person in persons]
    return await asyncio.gather(*tasks)


async def main():
    await db.set_bind(f'postgresql://{db_config.PGUSER}:{db_config.PGPASSWORD}@127.0.0.1/{db_config.PGDATABASE}')
    persons = await get_persons()
    pprint(persons)
    await write_to_db(persons)
    await db.pop_bind().close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    # asyncio.run(main(), debug=True)