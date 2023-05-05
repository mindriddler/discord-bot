# DiscordBotLogger

from __future__ import annotations

import datetime
import sys
from functools import partialmethod

import loguru

from helperfunctions import read_config

logger_config = read_config("logger")


# just a test
class DiscordBotLogger:
    _logger = None  # Add this line

    def __init__(
        self,
        log_level: str = logger_config["log_level_info"],
        _log_path_channel: str = "/logs/channel.log",
        _log_path_command: str = "/logs/command.log",
        _log_path_dm: str = "/logs/dm_logs/dm.log",
        _log_path_info: str = logger_config["log_path_info"],
        log_rotation: int | str | datetime.timedelta | datetime.time = logger_config["log_rotation"],
        log_retention: str = logger_config["log_retention"],
        log_compression_format: str = logger_config["log_compression_format"],
        enqueue: bool = True,
    ) -> None:
        self.custom_levels = []
        self.log_level = log_level
        self.log_path_channel = _log_path_channel
        self.log_path_command = _log_path_command
        self.log_path_dm = _log_path_dm
        self.log_path_info = _log_path_info
        self.rotation = log_rotation
        self.retention = log_retention
        self.compression_format = log_compression_format
        self.enqueue = enqueue

    def _formatter(self, message: dict) -> str:
        return (
            "<green>[{time:YYYY-MM-DD HH:mm:ss}] </green>"
            "<level>[{level:<8}] </level>"
            "<cyan>{name}</cyan>."
            "<cyan>{function}</cyan>:"
            "<cyan>{line}</cyan>: "
            "<level>{message}</level>"
            "\n<red>{exception}</red>"
        )

    def add_custom_level(self, name, level, color, icon):
        if name not in self.custom_levels:
            loguru.logger.level(name, no=level, color=color, icon=icon)
            self.custom_levels.append(name)

    def get_dm_logger_for_user(self, user_id: str) -> loguru.Logger:
        dm_log_path = f"/logs/dm_logs/{user_id}.log"
        logger = loguru.logger
        custom_level_name = f"{user_id}"
        if not hasattr(loguru.logger.__class__, custom_level_name):
            self.add_custom_level(custom_level_name, level=5, color="<magenta>", icon="-")
            loguru.logger.__class__.user_id = partialmethod(loguru.logger.__class__.log, custom_level_name)

        logger.add(
            dm_log_path,
            format=self._formatter,
            level=custom_level_name,
            rotation=self.rotation,
            retention=self.retention,
            compression=self.compression_format,
            enqueue=self.enqueue,
            filter=lambda record: record["level"].name == custom_level_name,
        )

        logger.info(f"Initializing DM logger for user {user_id}")
        return logger

    def get_logger(self) -> loguru.Logger:
        if DiscordBotLogger._logger is None:  # Add this line
            logger = loguru.logger
            logger.remove()
            if not hasattr(loguru.logger.__class__, "COMMAND"):
                loguru.logger.__class__.command = partialmethod(loguru.logger.__class__.log, "COMMAND")
                logger.level("COMMAND", no=10, color="<green>", icon="-")
            if not hasattr(loguru.logger.__class__, "CHANNEL"):
                loguru.logger.__class__.channel = partialmethod(loguru.logger.__class__.log, "CHANNEL")
                logger.level("CHANNEL", no=15, color="<green>", icon="-")

            # Add new handler with custom formatter
            logger.add(self.log_path_info, format=self._formatter, level=self.log_level)
            logger.add(sys.stdout, format=self._formatter, level=self.log_level)
            logger.add(
                self.log_path_command,
                format=self._formatter,
                level="COMMAND",
                rotation=self.rotation,
                retention=self.retention,
                compression=self.compression_format,
                enqueue=self.enqueue,
                filter=lambda record: record["level"].name == "COMMAND",
            )
            logger.add(
                self.log_path_channel,
                format=self._formatter,
                level="CHANNEL",
                rotation=self.rotation,
                retention=self.retention,
                compression=self.compression_format,
                enqueue=self.enqueue,
                filter=lambda record: record["level"].name == "CHANNEL",
            )

            logger.info("Initializing logger")
            DiscordBotLogger._logger = logger

        return DiscordBotLogger._logger
