from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

from app.database.database import db_dependency
from app.database.models.user import User, UserStatus, UserRole
from app.schemas.users import UserResponse
from app.schemas.admin import UserAdminResponse
from app.routers.auth import user_dependency
from app.schemas.admin import UpdateStatusRequest
from typing import Optional

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users", response_model=List[UserAdminResponse])
def get_all_users(db: db_dependency, user: user_dependency,status: Optional[UserStatus] = None):
    if user["role"] != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Acesso negado.")
    
    query = db.query(User).filter(User.role == UserRole.STUDENT)
    
    if status:
        query = query.filter(User.status == status)
        
    return query.all()

@router.get('/user/{user_id}', response_model=UserAdminResponse)
async def get_user_by_id(user: user_dependency, db:db_dependency, user_id: int):
    if user['role'] != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")

    target_user = db.query(User).filter(User.id == user_id, User.role == UserRole.STUDENT).first()

    if not target_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return target_user

@router.patch("/users/{user_id}/status", response_model=UserAdminResponse)
async def update_user_status(user_id: int, db:db_dependency, user: user_dependency, body:UpdateStatusRequest):
    if user['role'] != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    
    target_user = db.query(User).filter(User.id == user_id).first()

    if not target_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    target_user.status = body.status
    db.commit()
    db.refresh(target_user)

    return target_user

@router.delete("/users/{user_id}/deleted")
async def delete_user(user_id: int, user: user_dependency, db:db_dependency):
    if user['role'] != UserRole.ADMIN.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")

    target_user = db.query(User).filter(User.id == user_id, User.role == UserRole.STUDENT).first()

    if not target_user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    db.delete(target_user)
    db.commit()
    return {"detail": "Usuário deletado com sucesso."}