import asyncio
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.core.security import get_password_hash
import uuid

async def create():
    async with AsyncSessionLocal() as db:
        user = User(
            id=uuid.uuid4(),
            email='admin@example.com',
            hashed_password=get_password_hash('Admin123!'),
            is_superuser=True,
            is_active=True,
            is_verified=True,
            username='admin',
            full_name='Admin User'
        )
        db.add(user)
        await db.commit()
        print('✓ Admin user created: admin@example.com / Admin123!')

if __name__ == '__main__':
    asyncio.run(create())
