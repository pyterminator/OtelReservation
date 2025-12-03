from auth import operations as ao
from auth.schemes import ValidateUser, ShowUser, TokenFormat, LoginData
from fastapi import APIRouter,  HTTPException, status


router = APIRouter()

@router.post('/sign-up', status_code=status.HTTP_201_CREATED, response_model=ShowUser)
async def sign_up(data: ValidateUser):
    new_user = await ao.create_new_user(
        data.username,
        data.email,
        data.password,
        role=data.role
    )

    if not new_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="İstifadəçi əlavə edilmədi")
    
    return new_user



@router.post('/sign-in', status_code=status.HTTP_200_OK) # , response_model=TokenFormat
async def sign_in(data: LoginData):
    user = await ao.get_user(data.email)
    print(user)
    return user