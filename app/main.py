from fastapi import FastAPI
from app.routers import assignments, substitution, title, translator, chapters, roles

app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "Translator app"}


app.include_router(assignments.router)
app.include_router(substitution.router)
app.include_router(title.router)
app.include_router(translator.router)
app.include_router(chapters.router)
app.include_router(roles.router)