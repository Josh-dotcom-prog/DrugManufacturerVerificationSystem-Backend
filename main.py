from fastapi import FastAPI
from app.routes.users import user_router, auth_router, guest_router, admin_router

def create_application():
    application = FastAPI()
    # Users
    application.include_router(user_router)
    application.include_router(guest_router)
    application.include_router(auth_router)
    application.include_router(admin_router)

    return application

app = create_application()

@app.get("/")
def index():
    return {"message": "Drug Manufacturer Verification System is up and running."}