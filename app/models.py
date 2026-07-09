from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean,DateTime
import datetime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone
from sqlalchemy import func

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="role")


class Refresh_Token(Base):
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True) 
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token_hash = Column(String, unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False) 
    revoked = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="refresh_tokens")


class Request_before(Base):
    __tablename__ = "request_before"

    id = Column(Integer, primary_key=True, index=True) 

    customer = Column(String, nullable=False)

    contract_num = Column(String, nullable=False)
    contract_date = Column(Date, nullable=True)

    eol_fio = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    position = Column(String)
    gender = Column(String)
    full_name = Column(String)

    field_id = Column(Integer, ForeignKey("fields.id"), nullable=False)

    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    days = Column(Integer)

    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=True)
    comment = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, approved, rejected
    admin_comment = Column(String, nullable=True)
    created_at = Column(Date, default=datetime.now(timezone.utc))  


    user = relationship("User", foreign_keys=[user_id])
    field = relationship("Field")
    room = relationship("Room", foreign_keys=[room_id])
    

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    contract_num = Column(String, nullable=False)
    contract_date = Column(Date, nullable=True)
    
    eol_fio = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    position = Column(String)

    field_id = Column(Integer, ForeignKey("fields.id"), nullable=False)


    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    days = Column(Integer)

# for manager/admins
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=True)
    comment = Column(String, nullable=True)
    status = Column(String, default="approved")  #approved, rejected
    admin_comment = Column(String, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Прямая ссылка на жильца (Resident), не зависящая от User.resident_id
    resident_id = Column(Integer, ForeignKey("residents.id"), nullable=True)

    user = relationship("User", foreign_keys=[user_id])
    customer = relationship("Customer")
    field = relationship("Field")
    room = relationship("Room", foreign_keys=[room_id])
    resident = relationship("Resident", foreign_keys=[resident_id])
    customer = relationship("Customer", back_populates="requests")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    field_id = Column(Integer, ForeignKey("fields.id"),nullable=True)
    resident_id =  Column(Integer, ForeignKey("residents.id"))

    role = relationship("Role", back_populates="users")
    field = relationship("Field")
    refresh_tokens = relationship("Refresh_Token", back_populates="user")
    resident = relationship("Resident", uselist=False, foreign_keys=[resident_id])

class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True)
    name = Column(String)


    rooms = relationship("Room", back_populates="field")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String)


    requests = relationship("Request", back_populates="customer")

class Resident(Base):
    __tablename__ = "residents"

    id = Column(Integer, primary_key=True)
    
    position = Column(String)
    gender = Column(String, nullable=True)
    birthday = Column(Date, nullable=True)
    
    full_name = Column(String, nullable=False)

    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String)
    

    


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    room_number = Column(String, nullable=False)
    field_id = Column(Integer, ForeignKey("fields.id"))
    capacity = Column(Integer, nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"))
    path_id = Column(Integer, ForeignKey("paths.id"))
    room_unique_id = Column(String)
    status = Column(Integer)



    field = relationship("Field", back_populates="rooms")
    location = relationship("Location", back_populates="rooms")
    path = relationship("Path", back_populates="rooms")
    


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    rooms = relationship("Room", back_populates="location")


class Path(Base):
    __tablename__ = "paths"
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)

    rooms = relationship("Room", back_populates="path")



class ContractCounter(Base):
    __tablename__ = "contract_counters"

    id = Column(Integer, primary_key=True, index=True)
    prefix = Column(String, unique=True, nullable=False)   # например, "УРМ"
    last_number = Column(Integer, default=0, nullable=False)