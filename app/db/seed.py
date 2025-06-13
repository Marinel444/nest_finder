from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.models.filters import Purpose, PropertyType, PropertySubtype
from app.db.models.location import Country, City

DATABASE_URL = "sqlite:///./db.sqlite3"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def record_exists(session, model, **kwargs) -> bool:
    return session.query(model).filter_by(**kwargs).first() is not None


def seed_data():
    session = SessionLocal()

    purposes = [
        {"code": "rent", "name": "Rent"},
        {"code": "sale", "name": "Sale"},
    ]
    for data in purposes:
        if not record_exists(session, Purpose, code=data["code"]):
            session.add(Purpose(**data))

    property_types = [
        {"code": "residential", "name": "Residential"},
        {"code": "commercial", "name": "Commercial"},
    ]
    for data in property_types:
        if not record_exists(session, PropertyType, code=data["code"]):
            session.add(PropertyType(**data))
    session.commit()

    residential = session.query(PropertyType).filter_by(code="residential").first()
    commercial = session.query(PropertyType).filter_by(code="commercial").first()

    # --- Property Subtypes ---
    subtypes = [
        {"code": "apartment", "name": "Apartment", "property_type_id": residential.id},
        {"code": "house", "name": "House", "property_type_id": residential.id},
        {"code": "office", "name": "Office", "property_type_id": commercial.id},
        {"code": "retail", "name": "Retail", "property_type_id": commercial.id},
    ]
    for data in subtypes:
        if not record_exists(session, PropertySubtype, code=data["code"]):
            session.add(PropertySubtype(**data))

    # --- Countries ---
    countries = [
        {"name": "Russia"},
    ]
    for data in countries:
        if not record_exists(session, Country, name=data["name"]):
            session.add(Country(**data))
    session.commit()

    russia = session.query(Country).filter_by(name="Russia").first()

    # --- Cities ---
    cities = [
        {"name": "Moscow", "country_id": russia.id},

    ]
    for data in cities:
        if not record_exists(session, City, name=data["name"], country_id=data["country_id"]):
            session.add(City(**data))

    session.commit()
    session.close()
    print("✅ Seed data inserted successfully (without duplicates)")


if __name__ == "__main__":
    seed_data()
