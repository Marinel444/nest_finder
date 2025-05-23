from datetime import datetime
from sqlalchemy import BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models import User, FilterGroup, Advertisement


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    filter_group_id: Mapped[int] = mapped_column(ForeignKey("filter_groups.id"), nullable=False)
    advertisement_id: Mapped[int] = mapped_column(ForeignKey("advertisements.id"), nullable=False)

    sent_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User")
    filter_group: Mapped["FilterGroup"] = relationship("FilterGroup")
    advertisement: Mapped["Advertisement"] = relationship("Advertisement")
