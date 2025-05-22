from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Purpose(Base):
    __tablename__ = "purposes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)  # e.g. 'rent'
    name: Mapped[str] = mapped_column(String, nullable=False)               # e.g. 'Снять'
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PropertyType(Base):
    __tablename__ = "property_types"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    subtypes: Mapped[list["PropertySubtype"]] = relationship(
        back_populates="property_type", cascade="all, delete-orphan"
    )


class PropertySubtype(Base):
    __tablename__ = "property_subtypes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    property_type_id: Mapped[int] = mapped_column(ForeignKey("property_types.id"), nullable=False)
    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    property_type: Mapped["PropertyType"] = relationship(back_populates="subtypes")
