import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from app.core.config import settings
from app.database.session import SessionLocal, engine, Base
from app.database.models import Studio, User, Series, PlatformEnum, UserRole
from app.core.auth import get_password_hash

print("Waiting for database...")
max_retries = 5
retry_count = 0

while retry_count < max_retries:
    try:
        engine = create_engine(settings.database_url)
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        break
    except OperationalError:
        retry_count += 1
        print(f"Database not ready, retrying in 3 seconds... ({retry_count}/{max_retries})")
        time.sleep(3)

# Create session
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Create Studios
studios = [
    Studio(name="iqiyi", platform=PlatformEnum.IQIYI),
    Studio(name="viu", platform=PlatformEnum.VIU),
    Studio(name="netflix", platform=PlatformEnum.NETFLIX),
    Studio(name="aisplay", platform=PlatformEnum.AISPLAY),
    Studio(name="oned", platform=PlatformEnum.ONED),
    Studio(name="wetv", platform=PlatformEnum.WETV),
    
]
db.add_all(studios)
db.commit()

# Create Users
users = [
    User(
        username="normal_user",
        email="user@blcentral.com",
        full_name="Normal Fan",
        hashed_password=get_password_hash("user123"),
        role=UserRole.NORMAL,
        is_active=True
    ),
    User(
        username="content_editor",
        email="editor@blcentral.com",
        full_name="Content Editor",
        hashed_password=get_password_hash("editor123"),
        role=UserRole.EDITOR,
        is_active=True
    ),
    User(
        username="admin",
        email="admin@blcentral.com",
        full_name="System Admin",
        hashed_password=get_password_hash("admin123"),
        role=UserRole.ADMIN,
        is_active=True
    ),
]

db.add_all(users)
db.commit()

# Create Series
series_list = [
    Series(
        title_th="มีสติหน่อยคุณธีร์",
        title_en="Me and Thee",
        description="A chance meeting leads photographer Peach to mentor wealthy businessman Thee, whose obsession with TV dramas and disconnect from real-world values needs a serious reality check.",
        release_year=2025,
        status="completed",
        air_day="Saturday",
        air_time="20:30",
        studios=[studios[0]]
    ),
    Series(
        title_th="นิ่งเฮียก็หาว่าซื่อ",
        title_en="Cutie Pie Series",
        description="Thai BL drama focusing on Kuea Keerati and Lian Kilen Wang, childhood friends engaged by family arrangement",
        release_year=2022,
        status="completed",
        air_day="Saturday",
        air_time="22:30",
        studios=[studios[0], studios[2]]
    ),
    Series(
        title_th="รักจริงหลังแต่ง",
        title_en="My Romance Scammer",
        description="The story of two con artists, Tim and Yu, who deceive wealthy heirs, Pai and North, into marriage to seize their fortune, only to fall in love with their targets",
        release_year=2026,
        status="ongoing",
        air_day="Sunday",
        air_time="20:30",
        studios=[studios[5]]
    ),
]

db.add_all(series_list)
db.commit()

print("Database seeded!")
print(f"Series: {len(series_list)}")
print(f"Studios: {len(studios)}")
print(f"Users: {len(users)}")
print("Username: normal_user, Password: user123, Role: NORMAL")
print("Username: content_editor, Password: editor123, Role: EDITOR")
print("Username: admin, Password: admin123, Role: ADMIN")

db.close()