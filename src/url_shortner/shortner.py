import datetime
import hashlib

from src.helpers.redis import RedisCache


class URLShortenerHelpers:
    @classmethod
    def generate_unique(cls, user: str, url: str) -> str:
        """Generate unique code using hash of URL + timestamp + random salt."""
        current_time = datetime.datetime.now().strftime("%d%m%Y%H%M%S%f")
        random_salt = "".join(current_time + user)

        # Create hash from URL + timestamp + salt
        hash_input = f"{url}_{current_time}_{random_salt}"
        hash_digest = hashlib.sha256(hash_input.encode()).hexdigest()[:8]

        return hash_digest

    @classmethod
    def initiate_cache(cls) -> RedisCache:
        instance = RedisCache()
        return instance


class URLShortener:
    def __init__(self, url: str, user_id: str) -> None:
        self.url = url
        self.user = user_id

    def short_url(self) -> str | None:
        cache = URLShortenerHelpers.initiate_cache()

        # Generate unique code and ensure it doesn't exist
        unique_code = URLShortenerHelpers.generate_unique(self.user, self.url)

        # Check if this code already exists, regenerate if needed
        while cache.get_cache(unique_code):
            unique_code = URLShortenerHelpers.generate_unique(self.user, self.url)

        # Store the mapping
        cache.set_cache(key=unique_code, value=self.url)
        return unique_code


if __name__ == "__main__":
    inst = URLShortener(
        url="https://google.com",
        user_id="Aman",
    )
    short_code = inst.short_url()
    print(f"Short code: {short_code}")
