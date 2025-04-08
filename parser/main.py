import asyncio
from parser.gateway import app


async def main():
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
