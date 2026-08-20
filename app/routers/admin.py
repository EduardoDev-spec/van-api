<<<<<<< HEAD
from typing import List, Literal
=======
from typing import List
>>>>>>> a248c5bcbe75973cf774005ddd712eb06ebcc5d8
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

from app.database.database import db_dependency
from app.database.models.user import User, UserStatus, UserRole
<<<<<<< HEAD
from app.database.models.attendance import Attendance
=======
>>>>>>> a248c5bcbe75973cf774005ddd712eb06ebcc5d8
from app.schemas.users import UserResponse
from app.schemas.admin import UserAdminResponse
from app.routers.auth import user_dependency
from app.schemas.admin import UpdateStatusRequest
from typing import Optional
<<<<<<< HEAD
from datetime import date
=======
>>>>>>> a248c5bcbe75973cf774005ddd712eb06ebcc5d8

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
<<<<<<< HEAD
async def delete_user(user_id: int, user: user_dependency, db: db_dependency):
    if user['role'] != UserRole.ADMIN.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
=======
async def delete_user(user_id: int, user: user_dependency, db:db_dependency):
    if user['role'] != UserRole.ADMIN.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
>>>>>>> a248c5bcbe75973cf774005ddd712eb06ebcc5d8

    target_user = db.query(User).filter(User.id == user_id, User.role == UserRole.STUDENT).first()

    if not target_user:
<<<<<<< HEAD
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    # 1. Apaga primeiro os registros de presença vinculados a este usuário para evitar o erro de chave estrangeira
    db.query(Attendance).filter(Attendance.user_id == user_id).delete()

    # 2. Agora deleta o usuário com segurança
    db.delete(target_user)
    db.commit()
    
    return {"detail": "Usuário deletado com sucesso."}

@router.get('/admin/attendances')
async def get_attendances(
    data: date, 
    shift: Literal["morning", "night"], 
    user: user_dependency, 
    db: db_dependency
):
    if user.get('role') != UserRole.ADMIN.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")

    
    attendances = db.query(Attendance).filter(
        Attendance.date == data,
        Attendance.shift == shift,
        Attendance.is_confirmed == True,
        Attendance.transport_mode.in_(["ida_e_volta", "so_ida", "so_volta"]) # <-- O segredo está aqui!
    ).all()

    ida_e_volta = []
    so_ida = []
    so_volta = []

    # Organizando cada aluno
    for att in attendances:
        info_aluno = {
            "id_presenca": att.id,
            "aluno_nome": att.student.name,
            "aluno_telefone": att.student.phone
        }

        if att.transport_mode == "ida_e_volta":
            ida_e_volta.append(info_aluno)
        elif att.transport_mode == "so_ida":
            so_ida.append(info_aluno)
        elif att.transport_mode == "so_volta":
            so_volta.append(info_aluno)

    return {
        "total_van": len(attendances),
        "grupos": {
            "ida_e_volta": ida_e_volta,
            "so_ida": so_ida,
            "so_volta": so_volta
        }
    }
=======
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    db.delete(target_user)
    db.commit()
    return {"detail": "Usuário deletado com sucesso."}
>>>>>>> a248c5bcbe75973cf774005ddd712eb06ebcc5d8
