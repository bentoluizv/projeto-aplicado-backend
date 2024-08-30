from sqlalchemy.orm import Session

from app.errors.NotFoundError import NotFoundError
from app.infra.database.models import AccommodationDB


def find_accommodation_by_id(session: Session, id: str):
    existing_accommodation = session.get(AccommodationDB, id)

    if not existing_accommodation:
        raise NotFoundError(id)

    return existing_accommodation
