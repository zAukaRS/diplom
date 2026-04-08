from .models import Role
from .database import SessionLocal

def get_admin_role_id():
    db = SessionLocal()
    try:
        role = db.query(Role).filter(Role.name == "admin").first()
        if role:
            return role.id
        # Если роли нет, создаем
        new_role = Role(name="admin")
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        return new_role.id
    finally:
        db.close()