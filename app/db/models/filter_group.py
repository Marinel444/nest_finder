from datetime import datetime
from sqlalchemy import ForeignKey, Integer, Boolean, DateTime, String, Numeric, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.user import User
    from app.db.models import Country, City, Purpose, PropertyType, PropertySubtype


class FilterGroup(Base):
    __tablename__ = "filter_groups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    price_min: Mapped[float | None] = mapped_column(Numeric(10, 2))
    price_max: Mapped[float | None] = mapped_column(Numeric(10, 2))
    area_min: Mapped[int | None]
    area_max: Mapped[int | None]
    rooms_min: Mapped[int | None]
    rooms_max: Mapped[int | None]
    floor_min: Mapped[int | None]
    floor_max: Mapped[int | None]

    countries: Mapped[list["FilterGroupCountry"]] = relationship(
        back_populates="filter_group",
        cascade="all, delete-orphan",
    )
    cities: Mapped[list["FilterGroupCity"]] = relationship(
        back_populates="filter_group",
        cascade="all, delete-orphan",
    )
    purposes: Mapped[list["FilterGroupPurpose"]] = relationship(
        back_populates="filter_group",
        cascade="all, delete-orphan",
    )
    property_types: Mapped[list["FilterGroupPropertyType"]] = relationship(
        back_populates="filter_group",
        cascade="all, delete-orphan",
    )
    property_subtypes: Mapped[list["FilterGroupPropertySubtype"]] = relationship(
        back_populates="filter_group",
        cascade="all, delete-orphan",
    )

    user: Mapped["User"] = relationship(back_populates="filter_groups")


class FilterGroupCountry(Base):
    __tablename__ = "filter_group_countries"

    filter_group_id: Mapped[int] = mapped_column(ForeignKey("filter_groups.id"), primary_key=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"), primary_key=True)

    filter_group: Mapped["FilterGroup"] = relationship(back_populates="countries")
    country: Mapped["Country"] = relationship("Country")


class FilterGroupCity(Base):
    __tablename__ = "filter_group_cities"

    filter_group_id: Mapped[int] = mapped_column(ForeignKey("filter_groups.id"), primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), primary_key=True)

    filter_group: Mapped["FilterGroup"] = relationship(back_populates="cities")
    city: Mapped["City"] = relationship("City")


class FilterGroupPurpose(Base):
    __tablename__ = "filter_group_purposes"

    filter_group_id: Mapped[int] = mapped_column(ForeignKey("filter_groups.id"), primary_key=True)
    purpose_id: Mapped[int] = mapped_column(ForeignKey("purposes.id"), primary_key=True)

    filter_group: Mapped["FilterGroup"] = relationship(back_populates="purposes")
    purpose: Mapped["Purpose"] = relationship("Purpose")


class FilterGroupPropertyType(Base):
    __tablename__ = "filter_group_property_types"

    filter_group_id: Mapped[int] = mapped_column(ForeignKey("filter_groups.id"), primary_key=True)
    property_type_id: Mapped[int] = mapped_column(ForeignKey("property_types.id"), primary_key=True)

    filter_group: Mapped["FilterGroup"] = relationship(back_populates="property_types")
    property_type: Mapped["PropertyType"] = relationship("PropertyType")


class FilterGroupPropertySubtype(Base):
    __tablename__ = "filter_group_property_subtypes"

    filter_group_id: Mapped[int] = mapped_column(ForeignKey("filter_groups.id"), primary_key=True)
    property_subtype_id: Mapped[int] = mapped_column(ForeignKey("property_subtypes.id"), primary_key=True)

    filter_group: Mapped["FilterGroup"] = relationship(back_populates="property_subtypes")
    property_subtype: Mapped["PropertySubtype"] = relationship("PropertySubtype")
