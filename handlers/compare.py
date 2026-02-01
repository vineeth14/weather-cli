from typing import List
from handlers.temperature import temperature_handler
import asyncio

async def compare_handler(cities:List):

    tasks = []
    for city in cities:
        task = asyncio.create_task(temperature_handler(city))
        tasks.append(task)

    result = await asyncio.gather(*tasks)


