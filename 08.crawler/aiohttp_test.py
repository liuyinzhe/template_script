import asyncio
import aiohttp

#http://www.kingname.info/2020/03/23/why-default-aiohttp-slow/

template = 'http://exercise.kingname.info/exercise_middleware_ip/{page}'


async def get(session, page):
    url = template.format(page=page)
    resp = await session.get(url)
    print(await resp.text(encoding='utf-8'))


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for page in range(1000):
            task = asyncio.create_task(get(session, page))
            tasks.append(task)
        for task in tasks:
            await task

asyncio.run(main())
