from utils.hashing import Hash
from auth import operations as ao
from utils.token_manager import TokenManager
from fastapi import APIRouter,  HTTPException, status
from auth.schemes import ValidateUser, ShowUser, TokenFormat, LoginData, ValidateRefreshToken

router = APIRouter()

@router.post('/sign-up', status_code=status.HTTP_201_CREATED, response_model=ShowUser)
async def sign_up(data: ValidateUser):
    new_user = await ao.create_new_user( data.username, data.email, data.password, role=data.role )
    if not new_user: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="İstifadəçi əlavə edilmədi")
    return new_user

@router.post('/sign-in', status_code=status.HTTP_200_OK, response_model=TokenFormat)
async def sign_in(data: LoginData):
    if user := await ao.get_user(data.email):
        if Hash.verify(data.password, user.get_password):
            access_token = TokenManager.create_jwt({"id":user.id})
            refresh_token = TokenManager.create_refresh_token({"id":user.id})
            token_type = "bearer"
            return TokenFormat(access_token=access_token, refresh_token=refresh_token, token_type=token_type)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email və ya şifrə yanlışdır")

@router.post('/refresh', status_code=status.HTTP_201_CREATED, response_model=TokenFormat)
async def refresh_token(data: ValidateRefreshToken):
    if user_id := TokenManager.verify_refresh_token(data.refresh_token):
        access_token = TokenManager.create_jwt({"id":user_id})
        return TokenFormat( access_token = access_token, refresh_token = data.refresh_token, token_type = "bearer" )
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh token xətalıdır")
    