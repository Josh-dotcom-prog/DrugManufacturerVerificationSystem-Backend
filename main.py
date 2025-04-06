from fastapi import FastAPI
from app.routes.users import user_router, auth_router, guest_router, admin_router
from app.routes.manufacturer import manufacturer_router, manufacturer_admin_router
from app.routes.batches import batch_router

def create_application():
    application = FastAPI()
    # Users
    application.include_router(user_router)
    application.include_router(guest_router)
    application.include_router(auth_router)
    application.include_router(admin_router)

    # Manufacturer
    application.include_router(manufacturer_router)
    application.include_router(manufacturer_admin_router)

    # Batches
    application.include_router(batch_router)

    return application

app = create_application()

@app.get("/")
def index():
    return {"message": "Drug Manufacturer Verification System is up and running."}