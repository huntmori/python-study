# Database Connection Test Script
import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("=" * 60)
print("FastAPI Database Connection Test")
print("=" * 60)
print(f"\nDatabase URL: {DATABASE_URL.replace('fastapi_password', '***')}")

try:
    print("\n1. Creating engine...")
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

    print("2. Testing connection...")
    with engine.connect() as connection:
        result = connection.execute(text("SELECT VERSION()"))
        version = result.scalar()
        print(f"   ✅ Connected successfully!")
        print(f"   Database version: {version}")

        print("\n3. Checking database...")
        result = connection.execute(text("SELECT DATABASE()"))
        db_name = result.scalar()
        print(f"   ✅ Current database: {db_name}")

        print("\n4. Checking tables...")
        result = connection.execute(text("SHOW TABLES"))
        tables = result.fetchall()
        if tables:
            print(f"   ✅ Found {len(tables)} table(s):")
            for table in tables:
                print(f"      - {table[0]}")
        else:
            print("   ⚠️  No tables found yet (will be created on server startup)")

        print("\n" + "=" * 60)
        print("✅ Database connection test PASSED!")
        print("=" * 60)
        sys.exit(0)

except Exception as e:
    print(f"\n❌ Database connection test FAILED!")
    print(f"Error: {e}")
    print("\n" + "=" * 60)
    print("Please check:")
    print("1. MariaDB container is running: docker ps")
    print("2. Database credentials in .env file")
    print("3. User permissions are set correctly")
    print("=" * 60)
    sys.exit(1)

