"""
Redis Module
"""

from typing import Self
import coredis

from management_server.schemas import UserInCache
from management_server.settings import RedisSettings
from management_server.exceptions import InvalidRequestError

settings = RedisSettings()


def get_redis_client() -> coredis.Redis:
    """
    Returns a Redis client object.

    :return: A coredis.Redis object representing the Redis client.
    :rtype: coredis.Redis
    """
    return coredis.Redis(host=settings.redis_host, port=settings.redis_port)


redis_client = get_redis_client()


class Redis:
    """
    Redis class for interacting with Redis.
    """

    def __init__(self, user_id: str) -> None:
        self.user_id = user_id

    def __await__(self) -> Self:
        return self.async_init().__await__()

    async def async_init(self) -> bool | None:
        """
        Asynchronously initializes the object with the given secret.

        Args:
            secret (str): The secret used for initialization.

        Returns:
            bool: True if the initialization was successful.

        Raises:
            InvalidCredentialsError: If the secret is invalid.
        """
        exists = await redis_client.exists([self.user_id])
        if exists != 1:
            raise InvalidRequestError(detail="User not found in cache", status_code=404)
        return self

    @staticmethod
    async def create_key(key: str, data: UserInCache) -> bool:
        """
        Creates a key in Redis

        Parameters:
            secret (str): The secret used as the key in Redis.
            data: The data to store in Redis.

        Returns:
            bool: Returns True if the key was successfully created and set to expire after the specified TTL, otherwise returns False.
        """
        created_hash = await redis_client.set(key, data.model_dump_json())

        if created_hash == 0:
            return False
        return True

    # async def check_if_token_valid(self, token: str) -> bool:
    #     """
    #     Check if the given token is valid.

    #     Parameters:
    #         token (str): The token to be checked.

    #     Returns:
    #         bool: True if the token is valid, False otherwise.
    #     """
    #     tokens = await self.get_items(return_items=True)
    #     if not token.encode() in tokens.values():
    #         return False
    #     return True

    # async def check_if_key_black_listed(self) -> bool:
    #     """
    #     Check if the key is blacklisted.

    #     Returns:
    #         bool: True if the key is not blacklisted, False otherwise.
    #     """
    #     user = await self.get_items(return_items=True)
    #     if user.get("black_listed".encode()) == "1".encode():
    #         return False
    #     return True

    # async def get_items(self, return_items: bool = False) -> Union[bool, dict]:
    #     """
    #     Retrieves the items associated with the user.

    #     Args:
    #         return_items (bool, optional): Whether to return the items or not. Defaults to False.

    #     Returns:
    #         Union[bool, dict]: If return_items is False, returns True if the user exists, otherwise returns False.
    #                            If return_items is True, returns a dictionary containing the user's items.
    #     """
    #     user = await redis_client.hgetall(self.secret)
    #     if user is None:
    #         return False
    #     if return_items:
    #         return user
    #     return True

    # async def update_field_keys(self, values: UpdateRedisKey, token: str) -> bool:
    #     """
    #     Updates the field keys in Redis with the provided values.

    #     Args:
    #         values (UpdateRedisKey): The values to update the Redis field keys with.
    #         token (str): The authentication token.

    #     Returns:
    #         bool: True if the field keys were successfully updated, False otherwise.
    #     """
    #     if not await self.check_if_token_valid(token):
    #         raise InvalidCredentialsError()
    #     update = await redis_client.hset(
    #         self.secret,
    #         {
    #             "access_token": values.access_token,
    #             "refresh_token": values.refresh_token,
    #         },
    #     )
    #     await redis_client.expire(self.secret, values.ttl)
    #     if update != 1:
    #         return JSONResponse(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             content={"message": "tokens not updated"},
    #         )
    #     return True

    # async def black_list(self, token: str | None = None, is_token: bool = True) -> bool:
    #     """
    #     Check if the given token is blacklisted.

    #     Args:
    #         token (str): The token to be checked.

    #     Returns:
    #         bool: True if the token is blacklisted, False otherwise.
    #     """
    #     if is_token:
    #         if not await self.check_if_token_valid(token):
    #             raise InvalidCredentialsError()

    #     update = await redis_client.hset(self.secret, {"black_listed": True})
    #     if update != 0:
    #         return JSONResponse(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             content={"message": "black list not changed"},
    #         )

    #     return True


def get_redis_cache() -> Redis:
    return Redis()
