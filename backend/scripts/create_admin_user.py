"""
Script to create admin user
Usage: python scripts/create_admin_user.py
"""
import sys
import os
import asyncio
import uuid
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

from app.core.config import settings
from app.models import User, UserProfile


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_admin_user():
    """
    Create super admin user: turhanhamza@gmail.com
    """
    # Create async engine
    engine = create_async_engine(str(settings.DATABASE_URL), echo=True)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        try:
            # Check if admin user already exists
            from sqlalchemy import select
            result = await session.execute(
                select(User).where(User.email == "turhanhamza@gmail.com")
            )
            existing_user = result.scalar_one_or_none()

            if existing_user:
                print("❌ Admin user already exists!")
                print(f"   Email: {existing_user.email}")
                print(f"   Username: {existing_user.username}")
                print(f"   ID: {existing_user.id}")
                return

            # Create admin user
            admin_user = User(
                id=uuid.uuid4(),
                email="turhanhamza@gmail.com",
                username="turhanhamza",
                full_name="Turhan Hamza",
                hashed_password=pwd_context.hash("Admin@123456"),  # Default password
                is_active=True,
                is_verified=True,
                is_superuser=True,
                is_2fa_enabled=False,
                max_eas=999999,  # Unlimited
                max_backtests_per_month=999999,  # Unlimited
                max_optimizations_per_month=999999,  # Unlimited
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat(),
            )

            session.add(admin_user)
            await session.flush()

            # Create admin profile
            admin_profile = UserProfile(
                id=uuid.uuid4(),
                user_id=admin_user.id,
                bio="Platform Administrator",
                experience_level="expert",
                preferred_markets=["forex", "crypto", "stocks"],
                risk_tolerance="high",
                trading_style="swing_trader",
                profile_visibility="public",
                show_activity=True,
                show_in_search=True,
                reputation_score=1000,  # Max reputation
                is_verified=True,
                verification_date=datetime.utcnow().isoformat(),
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat(),
            )

            session.add(admin_profile)
            await session.commit()

            print("✅ Admin user created successfully!")
            print("")
            print("━" * 60)
            print("📧 Email:    turhanhamza@gmail.com")
            print("👤 Username: turhanhamza")
            print("🔑 Password: Admin@123456")
            print("🆔 User ID:  " + str(admin_user.id))
            print("━" * 60)
            print("")
            print("⚠️  IMPORTANT: Change the password after first login!")
            print("")
            print("Admin Permissions:")
            print("  ✅ Super Admin (full platform access)")
            print("  ✅ Unlimited EAs")
            print("  ✅ Unlimited backtests")
            print("  ✅ Unlimited optimizations")
            print("  ✅ User management")
            print("  ✅ Content moderation")
            print("  ✅ System configuration")
            print("  ✅ Audit log access")
            print("")

        except Exception as e:
            print(f"❌ Error creating admin user: {e}")
            await session.rollback()
            raise
        finally:
            await engine.dispose()


async def main():
    """Main entry point"""
    print("")
    print("═" * 60)
    print("  🚀 Creating Admin User")
    print("═" * 60)
    print("")

    try:
        await create_admin_user()
        print("✨ Done!")
        print("")
    except Exception as e:
        print(f"❌ Failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
