from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.appointments import router as appointments_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(appointments_router, prefix="/appointments", tags=["appointments"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the OCR-based NLP Appointment Scheduling Service!"}