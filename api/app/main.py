from fastapi import FastAPI
from app.infra.container.container import Container
from app.presentation.api.router import resize as resize_route


container = Container()
container.wire(modules=[resize_route])

app = FastAPI()
app.container = container


app.include_router(resize_route.router)
