from typing import Annotated
from fastapi import FastAPI, Depends, Request
from app.infra.container.container import Container
from dependency_injector.wiring import Provide, inject
from app.infra.queue.message_queue import MessageQueue
from contextlib import asynccontextmanager, AsyncExitStack
from app.presentation.api.router import resize as resize_route
from fastapi.dependencies.utils import get_dependant, solve_dependencies


def inject_lifespan(lifespan):
    @asynccontextmanager
    async def _inject_lifespan(app: FastAPI):
        # A fake request for solve_dependencies
        request = Request(scope={
            "type": "http",
            "http_version": "1.1",
            "method": "GET",
            "scheme": "http",
            "path": "/",
            "raw_path": b"/",
            "query_string": b"",
            "root_path": "",
            "headers": (
                (b"X-Request-Scope", b"lifespan"),
            ),
            "client": ("localhost", 80),
            "server": ("localhost", 80),
            "state": app.state,
        })
        dependant = get_dependant(path="/", call=lifespan)

        async with AsyncExitStack() as async_exit_stack:
            solved_deps = await solve_dependencies(
                request=request,
                dependant=dependant,
                async_exit_stack=async_exit_stack,
                embed_body_fields=False
            )

            ctxmgr = asynccontextmanager(lifespan)
            async with ctxmgr(**solved_deps.values) as value:
                yield value

    return _inject_lifespan

@inject_lifespan
@inject
async def lifespan(message_queue: Annotated[MessageQueue, Depends(Provide[Container.message_queue])]):
    await message_queue.connect()
    yield
    await message_queue.close()

container = Container()
container.wire(modules=[resize_route, __name__])

app = FastAPI(lifespan=lifespan)
app.container = container

app.include_router(resize_route.router)
