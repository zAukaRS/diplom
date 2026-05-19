from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


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
    resident_days = relationship("ResidentDay", back_populates="customer")  

class Resident(Base):
    __tablename__ = "residents"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=True)
    room = relationship("Room",foreign_keys=[room_id])
    field_id = Column(Integer, ForeignKey("fields.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))

    check_in = Column(Date)
    check_out = Column(Date)

    full_name = Column(String)
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
    date = Column(Date,nullable=True)
    extra = Column(Date, nullable=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True) 
    workplace_id =  Column(Integer, ForeignKey("workplaces.id"), nullable=True)
    days = Column(Integer,nullable=True)
    customer = relationship("Customer", back_populates="resident_days")
    workplace = relationship("Workplace", back_populates="resident_days")
    resident = relationship("Resident", back_populates="resident_days")
    room = relationship("Room", back_populates="resident_days")


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    room_number = Column(String, nullable=False)
    field_id = Column(Integer, ForeignKey("fields.id"))
    capacity = Column(Integer, nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"))
    path_id = Column(Integer, ForeignKey("paths.id"))
    room_unique_id = Column(String)



    field = relationship("Field", back_populates="rooms")
    location = relationship("Location", back_populates="rooms")
    path = relationship("Path", back_populates="rooms")
    resident_days = relationship("ResidentDay", back_populates="room")
    
    
   


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

class Workplace(Base):
    __tablename__ = "workplaces"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    resident_days = relationship("ResidentDay", back_populates="workplace")