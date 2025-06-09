import asyncio
import asyncpg
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Database:
    def __init__(self):
        # Fetch the database connection string from environment variables
        self.database_url = os.getenv('DATABASE_URL')
        self.connection = None

    async def connect(self):
        """Establish a connection to the database."""
        try:
            self.connection = await asyncpg.connect(self.database_url)
            print("Connected to the database successfully")
        except Exception as e:
            print(f"An error occurred during connection: {e}")

    async def disconnect(self):
        """Close the connection to the database."""
        if self.connection:
            await self.connection.close()
            print("Connection closed")

    async def execute_query(self, query, *args):
        """Execute a raw SQL query and return the results."""
        try:
            if self.connection is None:
                await self.connect()
            
            result = await self.connection.fetch(query, *args)
            return result
        except Exception as e:
            print(f"An error occurred while executing the query: {e}")
            return None

    async def execute_query_single(self, query, *args):
        """Execute a raw SQL query and return a single row."""
        try:
            if self.connection is None:
                await self.connect()
            
            result = await self.connection.fetchrow(query, *args)
            return result
        except Exception as e:
            print(f"An error occurred while executing the query: {e}")
            return None