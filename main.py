import uvicorn

from app.api.routes import app
from app.config import settings

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
