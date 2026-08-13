from fastapi import APIRouter, HTTPException, status
# Repare que agora importamos o db_dependency direto do database
from app.database.database import db_dependency
from app.database.models.user import User
from app.schemas.users import UserCreate, UserResponse, UserMeResponse
from app.core.security import get_password_hash
from app.routers.auth import user_dependency

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: db_dependency):
    
    db_user_email = db.query(User).filter(User.email == user.email).first()
    if db_user_email:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    
    db_user_cpf = db.query(User).filter(User.cpf == user.cpf).first()
    if db_user_cpf:
        raise HTTPException(status_code=400, detail="CPF já cadastrado.")

    hashed_password = get_password_hash(user.password)
    
    user_data = user.model_dump(exclude={"password"})
    new_user = User(**user_data, hashed_password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get('/me', response_model=UserMeResponse)
async def read_current_user(db: db_dependency, current_user: user_dependency):
    user = db.query(User).filter(User.id == current_user['id']).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return user