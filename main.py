from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse
from routers import check

app = FastAPI()

router = APIRouter(
    prefix="/api",
    )
router.include_router(check.router)

app.include_router(router)

@app.get("/")
async def index():
    with open("client/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
