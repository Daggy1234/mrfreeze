"""
Class for coordinating all the different settings modules.

This class loads all of the different settings sub-modules
and provides a single interface for working with them all.
"""

import logging
from typing import List

from mrfreeze.database.tables.abc_table_base import ABCTableBase
from mrfreeze.database.tables.freeze_mutes import FreezeMutes
from mrfreeze.database.tables.inkcyclopedia_mutes import InkcyclopediaMutes
from mrfreeze.database.tables.mute_channels import MuteChannels
from mrfreeze.database.tables.mute_interval import MuteInterval
from mrfreeze.database.tables.mute_roles import MuteRoles
from mrfreeze.database.tables.self_mute_times import SelfMuteTimes
from mrfreeze.database.tables.tempconverter_mutes import TempConverterMutes
from mrfreeze.database.tables.trash_channels import TrashChannels


class Settings:
    """Settings is a class for coordinating all the various settings modules."""

    def __init__(self) -> None:
        self.dbpath = "settings.db"
        self.tables: List[ABCTableBase] = list()
        self.logger = logging.getLogger(self.__class__.__name__)

        # Initialize the tables
        self.logger.info("Instantiating tables")
        self.mute_interval = MuteInterval(self.dbpath, self.logger)
        self.freeze_mutes = FreezeMutes(self.dbpath, self.logger)
        self.inkcyclopedia = InkcyclopediaMutes(self.dbpath, self.logger)
        self.mute_channels = MuteChannels(self.dbpath, self.logger)
        self.mute_roles = MuteRoles(self.dbpath, self.logger)
        self.self_mute_times = SelfMuteTimes(self.dbpath, self.logger)
        self.tempconverter_mutes = TempConverterMutes(self.dbpath, self.logger)
        self.trash_channels = TrashChannels(self.dbpath, self.logger)
        self.logger.info("All tables instantiated")

        # Add tables to self.tables
        self.tables.append(self.mute_interval)
        self.tables.append(self.freeze_mutes)
        self.tables.append(self.inkcyclopedia)
        self.tables.append(self.mute_channels)
        self.tables.append(self.mute_roles)
        self.tables.append(self.self_mute_times)
        self.tables.append(self.tempconverter_mutes)
        self.tables.append(self.trash_channels)

        # Initialize all the tables
        self.logger.info("Initializing tables")
        self.initialize()
        self.logger.info("All tables initialized")

        # Link all the methods
        # Mute Interval
        self.get_mute_interval          = self.mute_interval.get
        self.set_mute_interval          = self.mute_interval.set_by_id

        # Freeze Mutes
        self.is_freeze_muted            = self.freeze_mutes.get
        self.toggle_freeze_mute         = self.freeze_mutes.toggle

        # Inkcyclopedia Mutes
        self.is_inkcyclopedia_muted     = self.inkcyclopedia.get
        self.toggle_inkcyclopedia_mute  = self.inkcyclopedia.toggle

        # Mute Channels
        self.get_mute_channel           = self.mute_channels.get
        self.set_mute_channel           = self.mute_channels.set
        self.set_mute_channel_by_id     = self.mute_channels.set_by_id

        # Mute Roles
        self.get_mute_role              = self.mute_roles.get
        self.set_mute_role              = self.mute_roles.set
        self.set_mute_role_by_id        = self.mute_roles.set_by_id

        # Self mute times
        self.get_self_mute_time         = self.self_mute_times.get
        self.set_self_mute_time         = self.self_mute_times.set_by_id

        # TempConverterMutes Mutes
        self.is_tempconverter_muted     = self.tempconverter_mutes.get
        self.toggle_tempconverter_mute  = self.tempconverter_mutes.toggle

        # Trash Channels
        self.get_trash_channel          = self.trash_channels.get
        self.set_trash_channel          = self.trash_channels.set
        self.set_trash_channel_by_id    = self.trash_channels.set_by_id

    def initialize(self) -> None:
        """Set up the database and tables necessary for the server settings module."""
        for module in self.tables:
            module.create_table()

        for module in self.tables:
            module.load_from_db()
