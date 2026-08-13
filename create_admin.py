from getpass import getpass

from app.database.database import SessionLocal
from app.database.models.user import User, UserRole, UserStatus
from app.core.security import get_password_hash


def create_admin():
    db = SessionLocal()

    try:
        print("=== CRIAÇÃO DE ADMINISTRADOR ===")

        name = input("Nome: ")
        email = input("E-mail: ")
        phone = input("Telefone: ")
        cpf = input("CPF: ")
        address = input("Endereço: ")

        password = getpass("Senha: ")
        password_confirmation = getpass("Confirme a senha: ")

        if password != password_confirmation:
            print("❌ As senhas não coincidem.")
            return

        # Verifica se já existe usuário com esse e-mail
        existing_email = db.query(User).filter(User.email == email).first()

        if existing_email:
            print("❌ Já existe um usuário com esse e-mail.")
            return

        # Verifica se já existe usuário com esse CPF
        existing_cpf = db.query(User).filter(User.cpf == cpf).first()

        if existing_cpf:
            print("❌ Já existe um usuário com esse CPF.")
            return

        admin = User(
            name=name,
            email=email,
            phone=phone,
            cpf=cpf,
            address=address,
            hashed_password=get_password_hash(password),

            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,

            is_active=True,
            is_admin=True
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("\n✅ Administrador criado com sucesso!")
        print(f"ID: {admin.id}")
        print(f"Nome: {admin.name}")
        print(f"E-mail: {admin.email}")
        print(f"Role: {admin.role}")
        print(f"Status: {admin.status}")
        print(f"Admin: {admin.is_admin}")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro ao criar administrador: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()