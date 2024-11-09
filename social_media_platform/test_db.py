import os
import psycopg2
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('/Users/blackstocks/Desktop/Jay/social_media_platform/.env')

# Function to test PostgreSQL connection
def test_postgres_connection():
    print("\n🔍 Testing PostgreSQL Connection...\n")
    
    # Test direct PostgreSQL connection
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST', '127.0.0.1'),  # Default to 127.0.0.1
            port=os.getenv('DB_PORT', '5432')
        )
        print("✅ Direct PostgreSQL connection successful!")
        
        # Get PostgreSQL version
        cursor = conn.cursor()
        cursor.execute('SELECT version();')
        version = cursor.fetchone()
        print(f"📊 PostgreSQL Version: {version[0]}")
        
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print("❌ PostgreSQL connection failed!")
        print(f"🚫 Error: {e}")
        return False

    return True

# Run the test
if __name__ == "__main__":
    if test_postgres_connection():
        print("\n✨ Database connection is working properly!")
        sys.exit(0)
    else:
        print("\n⚠️ Database connection failed. Check the errors above.")
        sys.exit(1)
