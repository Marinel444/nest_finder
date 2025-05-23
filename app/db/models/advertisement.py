from datetime import datetime
from sqlalchemy import String, Integer, BigInteger, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models import Country, City, PropertyType, PropertySubtype


class Advertisement(Base):
    __tablename__ = "advertisements"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    source: Mapped[str | None] = mapped_column(String)
    external_id: Mapped[str] = mapped_column(String, nullable=False)

    title: Mapped[str | None] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(Text)
    url: Mapped[str | None] = mapped_column(String)

    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))

    price: Mapped[float | None] = mapped_column(Numeric(10, 2))
    area: Mapped[float | None] = mapped_column(Numeric(10, 2))
    rooms: Mapped[int | None]
    floor: Mapped[int | None]

    property_type_id: Mapped[int] = mapped_column(ForeignKey("property_types.id"))
    property_subtype_id: Mapped[int] = mapped_column(ForeignKey("property_subtypes.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    country: Mapped["Country"] = relationship("Country")
    city: Mapped["City"] = relationship("City")
    property_type: Mapped["PropertyType"] = relationship("PropertyType")
    property_subtype: Mapped["PropertySubtype"] = relationship("PropertySubtype")
