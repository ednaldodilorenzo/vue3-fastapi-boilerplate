import logging
import json
from fastapi.exceptions import HTTPException
from functools import wraps
from abc import abstractmethod
from pathlib import Path
from flagsmith import Flagsmith
from flagsmith.models import Flags
from flagsmith.exceptions import FlagsmithAPIError
from app.config import feature_flags_settings

logger = logging.getLogger(name=__file__)


class FeatureFlags:

    @abstractmethod
    def flag_is_enabled(self, flag: str) -> bool:
        pass

    @abstractmethod
    def load_feature_flags(self):
        pass


class FlagsmithFlags(FeatureFlags):

    _flags: Flags = None
    _flagsmith: Flagsmith = None

    def __init__(self):
        self._flagsmith = Flagsmith(
            environment_key=feature_flags_settings.server_key,  # Replace with your environment key
            api_url=feature_flags_settings.source,  # Set the custom server address
        )

    def _has_flag(self, flag: str) -> bool:
        return self._flags and (flag in self._flags.all_flags())

    def load_feature_flags(self):
        try:
            self._flags = self._flagsmith.get_environment_flags()
        except FlagsmithAPIError as fae:
            logger.error(fae)

    def flag_is_enabled(self, flag: str) -> bool:
        return bool(self._has_flag(flag) and self._flags.is_feature_enabled(flag))


class FileFlags(FeatureFlags):
    _flags: dict = {}

    def _has_flag(self, flag: str) -> bool:
        return flag in self._flags

    def load_feature_flags(self):
        file = Path(feature_flags_settings.source)
        if file.exists():
            with file.open(encoding="UTF-8") as file:
                self._flags = json.load(file)
        else:
            logger.error("Failed to load feature flags file!")

    def flag_is_enabled(self, flag: str) -> bool:
        return self._flags.get(flag, False)


feature_flags: FeatureFlags = FlagsmithFlags() if feature_flags_settings.server_mode else FileFlags()


def feature_enabled(flag: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not feature_flags.flag_is_enabled(flag):
                raise HTTPException(status_code=404, detail="Route not found.")
            return await func(*args, **kwargs)

        return wrapper

    return decorator
