"""
Configuration management for the BEAMSim discrete-event simulation engine.

This module defines the ConfigManager class, which handles loading and
validating configuration files for the simulation.
"""

import yaml


class ConfigManager:
    """
    A class for managing simulation configurations.
    """

    def __init__(self, default_config_path):
        """
        Initialize the ConfigManager.

        Args:
            default_config_path (str): Path to the default configuration file.
        """
        self.config = self._load_config(default_config_path)

    def _load_config(self, path):
        """
        Load a configuration file.

        Args:
            path (str): Path to the configuration file.

        Returns:
            dict: The loaded configuration.
        """
        with open(path, 'r') as file:
            return yaml.safe_load(file)

    def update_config(self, custom_config_path):
        """
        Update the configuration with values from a custom configuration file.

        Args:
            custom_config_path (str): Path to the custom configuration file.
        """
        custom_config = self._load_config(custom_config_path)
        self._merge_configs(self.config, custom_config)

    def _merge_configs(self, base_config, custom_config):
        """
        Recursively merge two configurations.

        Args:
            base_config (dict): The base configuration.
            custom_config (dict): The custom configuration to merge.
        """
        for key, value in custom_config.items():
            if isinstance(value, dict) and key in base_config:
                self._merge_configs(base_config[key], value)
            else:
                base_config[key] = value

    def get(self, key, default=None):
        """
        Retrieve a configuration value.

        Args:
            key (str): The configuration key (dot-separated for nested keys).
            default: The default value if the key is not found.

        Returns:
            The configuration value or the default.
        """
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value