from __future__ import annotations

import datetime
import sys
from functools import partialmethod

import loguru


class DiscordBotLogger:
    def __init__(
        self,
        log_level: str = "DEBUG",
        _log_path_channel: str = "logs/channel.log",
        _log_path_command: str = "logs/command.log",
        _log_path_dm: str = "logs/dm_logs/dm.log",
        _log_path: str = "logs/info.log",
        log_rotation: int | str | datetime.timedelta | datetime.time = 100_000_000,
        log_retention: str = "730 days",
        log_compression_format: str = "zip",
        enqueue: bool = True,
    ) -> None:
        self.custom_levels = []
        self.log_level = log_level
        self.log_path_channel = _log_path_channel
        self.log_path_command = _log_path_command
        self.log_path_dm = _log_path_dm
        self.log_path = _log_path
        self.rotation = log_rotation
        self.retention = log_retention
        self.compression_format = log_compression_format
        self.enqueue = enqueue

    def _formatter(self, message: dict) -> str:
        return (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>"
            "| <level>{level}</level> | "
            "<cyan>{name}</cyan>:"
            "<cyan>{function}</cyan>:"
            "<cyan>{line}</cyan> - "
            "<level>{message}</level>"
            "\n<red>{exception}</red>"
        )

    def add_custom_level(self, name, level, color, icon):
        if name not in self.custom_levels:
            loguru.logger.level(name, no=level, color=color, icon=icon)
            self.custom_levels.append(name)

    def get_dm_logger_for_user(self, user_id: str) -> loguru.Logger:
        dm_log_path = f"logs/dm_logs/{user_id}.log"
        logger = loguru.logger
        if not hasattr(loguru.logger.__class__, f"{user_id}"):
            loguru.logger.__class__.user_id = partialmethod(loguru.logger.__class__.log, f"{user_id}")
            self.add_custom_level(f"{user_id}", level=5, color="<magenta>", icon="-")

        logger.add(
            dm_log_path,
            format=self._formatter,
            level=user_id,
            rotation=self.rotation,
            retention=self.retention,
            compression=self.compression_format,
            enqueue=self.enqueue,
            filter=lambda record: record["level"].name == user_id,
        )

        logger.info(f"Initializing DM logger for user {user_id}")
        return logger

    def get_logger(self) -> loguru.Logger:
        logger = loguru.logger
        logger.remove()
        if not hasattr(loguru.logger.__class__, "command"):
            loguru.logger.__class__.command = partialmethod(loguru.logger.__class__.log, "command")
            logger.level("command", no=10, color="<green>", icon="-")
        if not hasattr(loguru.logger.__class__, "channel"):
            loguru.logger.__class__.channel = partialmethod(loguru.logger.__class__.log, "channel")
            logger.level("channel", no=15, color="<green>", icon="-")
        # Add new handler with custom formatter
        logger.add(self.log_path, format=self._formatter, level=self.log_level)
        logger.add(sys.stdout, format=self._formatter, level=self.log_level)
        logger.add(
            self.log_path_command,
            format=self._formatter,
            level="command",
            rotation=self.rotation,
            retention=self.retention,
            compression=self.compression_format,
            enqueue=self.enqueue,
            filter=lambda record: record["level"].name == "command",
        )
        logger.add(
            self.log_path_channel,
            format=self._formatter,
            level="channel",
            rotation=self.rotation,
            retention=self.retention,
            compression=self.compression_format,
            enqueue=self.enqueue,
            filter=lambda record: record["level"].name == "channel",
        )

        logger.info("Initializing logger")
        return logger
