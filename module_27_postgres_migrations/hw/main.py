import asyncio
from sqlalchemy.future import select
from database import SessionLocal
from models import TestTable

async def main():
    async with SessionLocal() as session:
        result = await session.execute(select(TestTable))
        rows = result.scalars().all()
        print(rows)

if __name__ == "__main__":
    asyncio.run(main())
