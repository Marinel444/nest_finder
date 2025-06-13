import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from app.db.base import Base
from app.db.models.filters import Purpose, PropertyType, PropertySubtype
from app.db.models.location import Country, City

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "expense_db")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def record_exists(session, model, **kwargs) -> bool:
    result = await session.execute(select(model).filter_by(**kwargs))
    return result.scalar_one_or_none() is not None


async def seed_data():
    async with AsyncSessionLocal() as session:
        # --- Purposes ---
        purposes = [
            {"code": "rent", "name": "Rent"},
            {"code": "sale", "name": "Sale"},
        ]
        for data in purposes:
            if not await record_exists(session, Purpose, code=data["code"]):
                session.add(Purpose(**data))

        # --- Property Types ---
        property_types = [
            {"code": "residential", "name": "Residential"},
            {"code": "commercial", "name": "Commercial"},
        ]
        for data in property_types:
            if not await record_exists(session, PropertyType, code=data["code"]):
                session.add(PropertyType(**data))

        await session.commit()

        # Получим созданные типы
        residential = await session.scalar(select(PropertyType).filter_by(code="residential"))
        commercial = await session.scalar(select(PropertyType).filter_by(code="commercial"))

        # --- Subtypes ---
        subtypes = [
            {"code": "apartment", "name": "Apartment", "property_type_id": residential.id},
            {"code": "house", "name": "House", "property_type_id": residential.id},
            {"code": "office", "name": "Office", "property_type_id": commercial.id},
            {"code": "retail", "name": "Retail", "property_type_id": commercial.id},
        ]
        for data in subtypes:
            if not await record_exists(session, PropertySubtype, code=data["code"]):
                session.add(PropertySubtype(**data))

        # --- Countries ---
        countries = [{"name": "Russia"}]
        for data in countries:
            if not await record_exists(session, Country, name=data["name"]):
                session.add(Country(**data))

        await session.commit()

        russia = await session.scalar(select(Country).filter_by(name="Russia"))

        # --- Cities ---
        cities = [{"name": "Moscow", "country_id": russia.id}]
        for data in cities:
            if not await record_exists(session, City, name=data["name"], country_id=data["country_id"]):
                session.add(City(**data))

        await session.commit()

        print("✅ Seed data inserted successfully (without duplicates)")


if __name__ == "__main__":
    asyncio.run(seed_data())
