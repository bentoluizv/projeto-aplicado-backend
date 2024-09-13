from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.infra.database.models import Base
from app.settings.Settings import Settings

engine = create_engine(
    f'postgresql://postgres.ourkxxhmvdlnpkghomcn:{Settings().DATABASE_PASSWORD}@aws-0-sa-east-1.pooler.supabase.com:6543/postgres'  # type: ignore
)

Base.metadata.create_all(engine)


def get_database_session():
    with Session(engine) as session:
        yield session
