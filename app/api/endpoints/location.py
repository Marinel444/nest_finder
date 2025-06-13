from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from app.api.schemas.location import CountryRead, CountryCreate, CityRead
from app.db.models import Country, City
from app.db.session import get_db

router = APIRouter(tags=["location"])


@router.get("/countries", response_model=list[CountryRead])
async def get_countries(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Country).order_by(Country.id))
    return result.scalars().all()


@router.get("/country/{pk}", response_model=CountryRead)
async def get_country(pk: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Country).where(Country.id == pk))
    country = result.scalar_one_or_none()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


@router.post("/country", response_model=CountryRead, status_code=status.HTTP_201_CREATED)
async def create_country(payload: CountryCreate, db: AsyncSession = Depends(get_db)):
    country = Country(name=payload.name)
    db.add(country)
    await db.commit()
    await db.refresh(country)
    return country


@router.get("/cities", response_model=list[CityRead])
async def get_cities(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City).order_by(City.id))
    return result.scalars().all()
