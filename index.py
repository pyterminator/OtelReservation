from uvicorn import run
from fastapi import FastAPI
from auth.routers import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contact.routers import router as contact_router
from vacancy.routers import router as vacancy_router
from therapy.routers import router as therapy_router

app = FastAPI(
    swagger_ui_parameters = { 
        "defaultModelsExpandDepth": -1
    },
    title="Otel Reservation"
)

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(contact_router, prefix="/contact", tags=["Contact Form"])
app.include_router(vacancy_router, prefix="/career", tags=["Career"])
app.include_router(therapy_router, prefix="/therapies", tags=["Therapies"])

if __name__ == "__main__":
    run(app="index:app", port=8000, host="127.0.0.1", reload=True)