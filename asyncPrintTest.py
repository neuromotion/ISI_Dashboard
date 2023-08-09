import asyncio
from itertools import count

async def main():
    for x in count():
        print(x, flush=True)
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())