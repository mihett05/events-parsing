import asyncio
import contextlib

from faststream import FastStream

from gateway import broker


async def create_rabbit_app() -> FastStream:
    app = FastStream(broker)
    return app


@contextlib.asynccontextmanager
async def lifespan():
    rabbit_app = await create_rabbit_app()
    await rabbit_app.broker.start()
    yield
    await rabbit_app.broker.close()


async def main():
    async with lifespan():
        while True:
            pass


if __name__ == '__main__':
    asyncio.run(main())
