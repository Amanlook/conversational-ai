"""Redis cache utility for the dual-mode AI assistant."""

import os

import redis
from dotenv import load_dotenv
from redis import Redis


class RedisCache:
    """Redis cache manager with environment-based configuration."""

    def __init__(self) -> None:
        """Initialize Redis cache with environment variables."""
        load_dotenv()

        # Load Redis configuration from environment
        self.host = os.environ.get("REDIS_HOST", "localhost")
        self.username = os.environ.get("REDIS_USERNAME")
        self.password = os.environ.get("REDIS_PASSWORD")
        self.port = int(os.environ.get("REDIS_PORT", "6379"))
        self.db = int(os.environ.get("REDIS_DB", "0"))

        # Initialize connection
        self._client: Redis | None = self.connect()

    def connect(self) -> Redis:
        """
        Create and return a Redis connection.

        Returns:
            Redis client instance

        Raises:
            redis.ConnectionError: If connection fails
        """
        try:
            client = redis.Redis(
                host=self.host,
                username=self.username,
                password=self.password,
                port=self.port,
                db=self.db,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
            )

            # Test the connection
            client.ping()
            return client
        except redis.ConnectionError as e:
            raise redis.ConnectionError(f"Failed to connect to Redis: {e}") from e

    @property
    def client(self) -> Redis:
        """
        Get the Redis client, creating connection if needed.

        Returns:
            Redis client instance
        """
        if self._client is None:
            self._client = self.connect()
        return self._client

    def set_cache(self, key: str, value: str, expire: int = 3600) -> bool:
        """
        Set a cache value with expiration.

        Args:
            key: Cache key
            value: Cache value
            expire: Expiration time in seconds (default: 1 hour)

        Returns:
            True if successful, False otherwise
        """
        try:
            result = self.client.setex(key, expire, value)
            return bool(result)
        except Exception as e:
            print(f"Error setting cache: {e}")
            return False

    def get_cache(self, key: str) -> str | None:
        """
        Get a cache value by key.

        Args:
            key: Cache key

        Returns:
            Cache value if exists, None otherwise
        """
        try:
            result = self.client.get(key)
            return result if isinstance(result, str) else None
        except Exception as e:
            print(f"Error getting cache: {e}")
            return None

    def delete_cache(self, key: str) -> bool:
        """
        Delete a cache key.

        Args:
            key: Cache key to delete

        Returns:
            True if key was deleted, False otherwise
        """
        try:
            return bool(self.client.delete(key))
        except Exception as e:
            print(f"Error deleting cache: {e}")
            return False

    def clear_all(self) -> bool:
        """
        Clear all cache data.

        Returns:
            True if successful, False otherwise
        """
        try:
            result = self.client.flushdb()
            return bool(result)
        except Exception as e:
            print(f"Error clearing cache: {e}")
            return False

    def is_connected(self) -> bool:
        """
        Check if Redis connection is active.

        Returns:
            True if connected, False otherwise
        """
        try:
            if self._client is None:
                return False
            self._client.ping()
            return True
        except Exception:
            return False

    def close(self) -> None:
        """Close the Redis connection."""
        if self._client is not None:
            self._client.close()
            self._client = None
