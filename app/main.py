from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.routes import message_router, report_routes
from fastapi.middleware.cors import CORSMiddleware  # <-- ADD

load_dotenv()
app = FastAPI()

# CORS - Cross Origin Resource Sharing
# This middleware allows the browser frontend to call the FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:63342",  # JetBrains/PyCharm preview
        "http://127.0.0.1:63342",  # VSCode Live Server
        "http://127.0.0.1:5500",
        "http://localhost:5500",  # Simple local host
        "http://127.0.0.1",
        "http://localhost"
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],
)

from app.data_loader import data_manager


@app.on_event("startup")
def startup_event():
    """
    On application startup: load all data from JSON files into memory
    """
    data_manager.load_data()


"""
register backend API routes:
 /message  -> chatbot conversation logic
 /generate-reports -> scheduled reporting simulator
 /debug/state  ->internal application state viewer
"""
app.include_router(message_router.router)
app.include_router(report_routes.router)
