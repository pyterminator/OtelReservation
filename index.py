from uvicorn import run
from fastapi import FastAPI
from contact.routers import router as contact_router

app = FastAPI(
    swagger_ui_parameters = { 
        "defaultModelsExpandDepth": -1
    },
    title="Otel Reservation"
)

app.include_router(contact_router, prefix="/contact", tags=["Contact Form"])

if __name__ == "__main__":
    run(app="index:app", port=8000, host="127.0.0.1", reload=True)