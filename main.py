from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from app.routes.users import user_router, auth_router, guest_router, admin_router
from app.routes.drugs import drug_router, verify_drug_router

def create_application():
    application = FastAPI()
    # Users
    application.include_router(user_router)
    application.include_router(guest_router)
    application.include_router(auth_router)
    application.include_router(admin_router)
    application.include_router(verify_drug_router)

    # Drugs
    application.include_router(drug_router)

    return application

app = create_application()

origins = [
    "http://localhost:5173",  # or your frontend's actual origin
    # "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],                # <-- VERY IMPORTANT
    allow_headers=["*"],                # <-- VERY IMPORTANT
)

@app.get("/")
def index():
    return {"message": "Drug Manufacturer Verification System is up and running."}