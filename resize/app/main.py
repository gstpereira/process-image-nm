from typing import Annotated
from fastapi import FastAPI, Depends, Request
from app.infra.container.container import Container
from dependency_injector.wiring import Provide, inject
from app.application.use_case.resize_file import ResizeFile
from app.infra.queue.message_queue import MessageConsumeQueue, Worker
from contextlib import asynccontextmanager, AsyncExitStack
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
async def lifespan(message_queue: Annotated[MessageConsumeQueue, Depends(Provide[Container.message_queue])], resize_file_use_case: Annotated[ResizeFile, Depends(Provide[Container.resize_file_use_case])]):
    await message_queue.connect()

    worker = Worker(topic="file_resized", processor=resize_file_use_case, message_queue=message_queue)
    await worker.start()

    yield
    await message_queue.close()

container = Container()
container.wire(modules=[__name__])

app = FastAPI(lifespan=lifespan)
app.container = container
