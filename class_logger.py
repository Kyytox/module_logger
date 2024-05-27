import os
import logging
import logging.config
import yaml
import warnings
import pprint


class LoggerSetup:
    def __init__(
        self,
        name: str = "root",
        config_path: str = "logging.yaml",
        log_file: str = "main.log",
    ):
        """Initialize the logger setup.

        Args:
            name (str): The logger name. Defaults to "root".
            config_path (str): The path to the config file. Defaults to "logging.yaml".
            log_file (str): The path to the log file. Defaults to "main.log".
        """
        self.name = name
        self.config_path = config_path
        self.log_file = log_file
        self.config = None
        self.logger = None

        self.setup_logger()

    def set_filename_to_logger(self, config: dict):
        """Set the log file to the logger config.

        Args:
            config (dict): The logger config as a dictionary.
        """
        desired_logger_name = self.name
        for self.name, logger_config in config["loggers"].items():
            if self.name == desired_logger_name:
                for handler_name in logger_config["handlers"]:
                    handler_config = config["handlers"][handler_name]
                    if handler_name != "console":
                        handler_config["filename"] = self.log_file

    def get_yaml_config(self) -> dict:
        """Load the config file and return it as a dictionary.

        Returns:
            dict: The config file as a dictionary.
        """

        try:
            with open(self.config_path, "r") as f:
                config = yaml.safe_load(f.read())
        except FileNotFoundError:
            raise FileNotFoundError(f"The config file not found: {self.config_path}.")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error in the config file: {e}")

        if self.name not in config["loggers"]:
            warnings.warn(
                "You specify a non-existing logger name, using the default root logger."
            )

        return config

    def setup_logger(self):
        """Setup the logger with the config file.

        Returns:
            logging.Logger: The logger object.
        """

        # Load the config file
        if self.config_path is None:
            raise ValueError("You forgot to specify the logger config path.")
        else:
            self.config = self.get_yaml_config()

        # add log_file to the config
        self.set_filename_to_logger(self.config)

        # Configure the logging module with the config file
        # pprint.pprint(self.config)
        logging.config.dictConfig(self.config)

        # create logger
        self.logger = logging.getLogger(self.name)

        # use adapter to add formatting fields
        self.logger = logging.LoggerAdapter(self.logger)

        return self.logger

    def delete(self):
        """Delete the logger and the log file."""
        if self.logger:
            del self.logger
        if self.log_file and os.path.exists(self.log_file):
            os.remove(self.log_file)
