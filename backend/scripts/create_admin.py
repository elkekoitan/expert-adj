"""
Gerçek admin kullanıcı seed scripti.

Kullanım:
  1) Ortam değişkenlerini ayarla:
     - FIRST_SUPERUSER
     - FIRST_SUPERUSER_PASSWORD
  2) Proje kökünden çalıştır:
     - python -m backend.scripts.create_admin

Notlar:
  - Var olan admin varsa yeniden oluşturmaz.
  - MOCK YOK: Gerçek User kaydı oluşturur, başarısızlıkta exception fırlatır.
"""

import asyncio
import os
import sys

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Parent path ekle (module import için)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.core.security import get_password_hash
from app.core.database import AsyncSessionLocal
from app.models.user import Organization, User


async def create_admin() -> None:
    if not settings.FIRST_SUPERUSER or not settings.FIRST_SUPERUSER_PASSWORD:
        raise RuntimeError(
            "FIRST_SUPERUSER ve FIRST_SUPERUSER_PASSWORD ortam değişkenleri tanımlı olmalı."
        )

    async with AsyncSessionLocal() as session:  # type: AsyncSession
        # Admin var mı kontrol et
        result = await session.execute(
            select(User).where(User.email == settings.FIRST_SUPERUSER)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            print("ℹ️ Admin user already exists")
            return

        # Organization yoksa basit bir default org oluştur (id lazım olabilir)
        org = Organization(name="Default Organization", slug="default")
        session.add(org)
        await session.flush()

        # Admin kullanıcı oluştur
        admin = User(
            email=settings.FIRST_SUPERUSER,
            username=settings.FIRST_SUPERUSER,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            full_name="Admin User",
            is_active=True,
            is_superuser=True,
            organization_id=org.id,
        )
        session.add(admin)
        await session.commit()

        print("✅ Admin user created successfully!")
        print(f"   Email: {settings.FIRST_SUPERUSER}")
        print(f"   Password: {settings.FIRST_SUPERUSER_PASSWORD}")
        print(f"   Organization: {org.name}")


def main() -> int:
    try:
        asyncio.run(create_admin())
        return 0
    except Exception as e:
        print(f"❌ Error while creating admin user: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
