"""
Create admin user for testing
"""

import asyncio
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import async_session_maker
from app.core.security import get_password_hash
from app.models.user import Organization, User


async def create_admin():
    """Create admin user and organization"""
    print("👤 Creating admin user...")

    async with async_session_maker() as session:
        # Check if admin exists
        from sqlalchemy import select

        result = await session.execute(
            select(User).where(User.email == "admin@mtoptimizer.com")
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            print("ℹ️  Admin user already exists")
            return

        # Create organization
        org = Organization(name="Default Organization", slug="default")
        session.add(org)
        await session.flush()

        # Create admin user
        admin = User(
            email="admin@mtoptimizer.com",
            username="admin",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            is_active=True,
            is_superuser=True,
            organization_id=org.id,
        )
        session.add(admin)
        await session.commit()

        print("✅ Admin user created successfully!")
        print("   Email: admin@mtoptimizer.com")
        print("   Password: admin123")
        print(f"   Organization: {org.name}")


def main():
    """Main entry point"""
    try:
        asyncio.run(create_admin())
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
