from fastapi import APIRouter, Depends, BackgroundTasks,status, Header, File, Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.database.database import get_session

from app.services.users import UserService, security
from app.repository.users import UserRepository
from app.repository.password_reset import PasswordResetRepository
from app.responses.users import *
from app.schemas.users import *



user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

guest_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)

auth_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(security.oauth2_scheme), Depends(security.get_current_user)]
)

admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(security.oauth2_scheme), Depends(security.get_current_user)]
)

def get_user_service(session: Session = Depends(get_session)) -> UserService:
    user_repository = UserRepository(session)
    password_reset_repository = PasswordResetRepository(session)
    return UserService(user_repository, password_reset_repository)


@user_router.post("/create", status_code=status.HTTP_201_CREATED,response_model=UserResponse)
async def create_user(background_task: BackgroundTasks, name: str = Form(), license_number: str = Form(), email: str = Form(), phone_number: str = Form(),
                      stresst_address: str = Form(), password: str = Form(), certificate: UploadFile = File() ,
                        user_service: UserService = Depends(get_user_service)):

    data = UserCreateSchema(
        name=name,
        license_number=license_number,
        email=email,
        phone_number=phone_number,
        street_address=stresst_address,
        password=password,
    )

    return await user_service.create_user_account(certificate, data, background_task)

@user_router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_user(data: ActivateUserSchema, background_tasks: BackgroundTasks, user_service: UserService = Depends(get_user_service)):
    await  user_service.activate_user_account(data, background_tasks)
    return JSONResponse({"message": "Account is activated successfully."})

@guest_router.post("/login", status_code=status.HTTP_200_OK, response_model=UserLoginResponse)
async def user_login(data: OAuth2PasswordRequestForm = Depends(), user_service: UserService = Depends(get_user_service), session: Session = Depends(get_session)):
    user = await user_service.get_login_token(data, session)
    return user

@guest_router.post("/refresh", status_code=status.HTTP_200_OK, response_model=UserLoginResponse)
async def refresh_token(refresh_token = Header(), user_service: UserService = Depends(get_user_service), session: Session = Depends(get_session)):
    return await user_service.get_refresh_token(refresh_token, session)

@guest_router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(data: UserForgotPasswordSchema, background_tasks: BackgroundTasks, session: Session = Depends(get_session), user_service: UserService = Depends(get_user_service)):
    await user_service.email_forgot_password_link(data, background_tasks, session)
    return JSONResponse({"message": "A email with password reset link has been sent to you."})

@guest_router.put("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(data: UserRestPasswordSchema, session: Session = Depends(get_session), user_service: UserService = Depends(get_user_service)):
    await user_service.reset_password(data, session)
    return JSONResponse({"message": "Your password has been updated."})

@auth_router.get("/me", status_code=status.HTTP_200_OK, response_model=AllUserResponse)
async def fetch_user(user=Depends(security.get_current_user), token: str = Header(None), user_service: UserService = Depends(get_user_service)):  # Use Header instead
    user_obj = await user_service.fetch_user_detail(user.id)
    return user_obj

@admin_router.get("/users", response_model=list[AllUserResponse])
async def get_all_users(user_service: UserService = Depends(get_user_service), current_user = Depends(security.get_current_user)):
    return await user_service.fetch_all_users(current_user)

@admin_router.get("/user", status_code=status.HTTP_200_OK,response_model=AllUserResponse)
async def get_user_detail(manufacturer_id: int, user_service: UserService = Depends(get_user_service),
                          current_user = Depends(security.get_current_user)):
    return await user_service.get_user_detail(manufacturer_id, current_user)

@admin_router.get("/certificate", status_code=status.HTTP_200_OK)
async def get_manufacturers_certificate(manufacturer_id: int,current_user = Depends(security.get_current_user),
                                         user_service: UserService = Depends(get_user_service)):
    return await user_service.get_manufacture_certificate(manufacturer_id, current_user)

@admin_router.patch("/approve", status_code=status.HTTP_200_OK)
async def approve_manufacturer(manufacturer_id: int, user_service: UserService = Depends(get_user_service),
                               current_user = Depends(security.get_current_user)):
    return await user_service.approve_manufacturer(manufacturer_id, current_user)

@admin_router.patch("/reject", status_code=status.HTTP_200_OK)
async def reject_manufacturer(manufacturer_id: int, user_service: UserService = Depends(get_user_service),
                              current_user = Depends(security.get_current_user)):
    return await user_service.reject_manufacturer(manufacturer_id, current_user)

@admin_router.get("/dashboard", status_code=status.HTTP_200_OK, response_model=AdminDashboard)
async def admin_dashboard(current_user = Depends(security.get_current_user),
                          user_service: UserService = Depends(get_user_service)):
    return await user_service.get_admin_dashboard(current_user)

@admin_router.get("/manufactures", status_code=status.HTTP_200_OK, response_model=ManufacturesInTheSystem)
async def manufactures_in_the_system(current_user = Depends(security.get_current_user),
                                     user_service: UserService = Depends(get_user_service)):
    return await user_service.get_manufacturers_in_the_system(current_user)

@admin_router.get("/approvals", status_code=status.HTTP_200_OK, response_model=ManufacturesForApproval)
async def manufacturers_pending_approval(current_user = Depends(security.get_current_user),
                                         user_service: UserService = Depends(get_user_service)):
    return await user_service.get_manufactures_for_approval(current_user)
