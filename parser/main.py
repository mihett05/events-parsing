import asyncio

from faststream import FastStream

from gateway import broker


async def runner():
    rabbit_app = FastStream(broker)
    await rabbit_app.run()


async def main():
    rabbit_app = FastStream(broker)
    await rabbit_app.run()


if __name__ == "__main__":
    asyncio.run(main())
