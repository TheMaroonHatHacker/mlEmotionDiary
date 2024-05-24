from typing import Annotated
from fastapi import FastAPI, Path, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

ALLOWED_ORIGINS = ["http://localhost:8000"]
ALLOWED_METHODS = ["GET", "POST"]

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=ALLOWED_METHODS,
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="home.j2")


@app.get("/clicked/{count}", response_class=HTMLResponse)
def clicked(
    request: Request, count: Annotated[int, Path(title="Current count of button")]
):
    return templates.TemplateResponse(
        request=request, name="button.j2", context={"count": count + 1}
    )
