from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from routers import check
import os

app = FastAPI()

router = APIRouter(
    prefix="/api",
    )
router.include_router(check.router)

app.include_router(router)

app.mount("/", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "client")))

@app.get("/")
async def index():
    return {
        "msg": "Welcome to Pdf Rules Checker"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

