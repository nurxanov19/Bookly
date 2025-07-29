from fastapi import APIRouter, Depends, status
from .schemas import UserCreateModel, UserModel, UserLoginModel
from .services import UserCreationService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from fastapi.exceptions import HTTPException
from .utils import verify_password, create_access_token
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.db.redis import add_jti_to_blocklist


user_router = APIRouter()
user_creation_service = UserCreationService()
role_checker = RoleChecker(['admin', 'user'])


REFRESH_TOKEN_EXPIRY = 2

@user_router.post(
        '/signup', response_model=UserModel, status_code=status.HTTP_201_CREATED
        )
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
                ):
    email = user_data.email
    user_exists = await user_creation_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")

    new_user = await user_creation_service.create_user(user_data, session)
    return new_user

@user_router.post('/login')
async def login_user(user_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    password = user_data.password

    user = await user_creation_service.get_user_by_email(email, session)

    if user is not None:
        pswrd_valid = verify_password(password, user.password_hash)

        if pswrd_valid:
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid),
                    "role": user.role
                }
            )
            refresh_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid)
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse(
                content={
                    'message': 'User logged successfully',
                    'access': access_token,
                    'refresh': refresh_token,
                    'user': {'email': user.email, 'user_uid': str(user.uid)}
                }
            )
        
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials!')


@user_router.get('/refresh_token')
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details['user'])
        return JSONResponse(content={"access_token": new_access_token}, status_code=status.HTTP_201_CREATED )

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials or unsuccessful login")

@user_router.get('/me')
async def get_current_user(user = Depends(get_current_user), _ : bool = Depends(role_checker)):
    return user


@user_router.get('/logout')
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details['jti']

    await add_jti_to_blocklist(jti=jti)
    return JSONResponse(content={"message": 'You logged out successfully'},
                        status_code=status.HTTP_200_OK)

