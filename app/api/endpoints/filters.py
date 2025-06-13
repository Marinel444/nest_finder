from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.db.session import get_db
from app.db.models import Purpose, PropertyType
from app.api.schemas.filters import PurposeRead, PropertyTypeRead

router = APIRouter(tags=["Filters"])


@router.get("/purposes", response_model=list[PurposeRead])
async def get_purposes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Purpose).order_by(Purpose.id))
    return result.scalars().all()


@router.get("/property-types", response_model=list[PropertyTypeRead])
async def get_property_types(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(PropertyType).options(joinedload(PropertyType.subtypes)).order_by(PropertyType.id)
    )
    return result.scalars().unique().all()
