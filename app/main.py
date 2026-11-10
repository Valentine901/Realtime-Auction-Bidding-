from fastapi import FastAPI
from app.api.routes import auth
from app.api.routes import user
from app.api.routes import room
from app.api.error_handlers import register_error_handlers
from app.api.routes import product
from app.api.routes import ws
app = FastAPI()

app.include_router(auth.router)
app.include_router(ws.router)
app.include_router(user.router)
app.include_router(room.router)
app.include_router(product.router)
register_error_handlers(app)
