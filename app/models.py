from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="role")



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    field_id = Column(Integer, ForeignKey("fields.id"),nullable=True)

    role = relationship("Role", back_populates="users")
    field = relationship("Field")


class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    residents = relationship("Resident", back_populates="field")
    rooms = relationship("Room", back_populates="field")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    residents = relationship("Resident", back_populates="customer")


class Resident(Base):
    __tablename__ = "residents"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    room = relationship("Room",foreign_keys=[room_id])  # связь к комнате
    field_id = Column(Integer, ForeignKey("fields.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))

    check_in = Column(Date)
    check_out = Column(Date)

    full_name = Column(String)
    # days = relationship("ResidentDay", back_populates="resident")
    position = Column(String)
    gender = Column(String, nullable=True)
    shift = Column(String, nullable=True) 
    field = relationship("Field", back_populates="residents")
    customer = relationship("Customer", back_populates="residents")
    
    resident_days = relationship(
        "ResidentDay",
        back_populates="resident",
        cascade="all, delete-orphan"
    )


class ResidentDay(Base):
    __tablename__ = "resident_days"

    id = Column(Integer, primary_key=True, index=True)
    resident_id = Column(Integer, ForeignKey("residents.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"),nullable=True)
    date = Column(Date)
    extra = Column(String, nullable=True)
    workplace_id = Column(Integer, ForeignKey("workplaces.id"), nullable=True)
    workplace = relationship("Workplace", back_populates="resident_days")

    resident = relationship("Resident", back_populates="resident_days")
    room = relationship("Room", back_populates="resident_days")


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    room_number = Column(String, nullable=False)

    location_id = Column(Integer, ForeignKey("locations.id"))
    path_id = Column(Integer, ForeignKey("paths.id"))

    location = relationship("Location", back_populates="rooms")
    path = relationship("Path", back_populates="rooms")
    # связь с Resident через ResidentDay
    resident_days = relationship("ResidentDay", back_populates="room")
    field_id = Column(Integer, ForeignKey("fields.id"))  # связь с Field
    
    field = relationship("Field", back_populates="rooms")


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    rooms = relationship("Room", back_populates="location")


class Path(Base):
    __tablename__ = "paths"
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)  # Например: "1 этаж левое крыло"

    rooms = relationship("Room", back_populates="path")




class Workplace(Base):
    __tablename__ = "workplaces"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    resident_days = relationship("ResidentDay", back_populates="workplace")
