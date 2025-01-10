#!/usr/bin/env python3

"""Alfred. A (Telegram Bot) Personal Assistant."""

import argparse
import importlib
import logging
import sys
import tomli

from telegrambot import TelegramBot


# Configure logging
LOG_FORMATTER = (
    "%(asctime)s -",
    "%(levelname)s -",
    "%(module)s -",
    "%(funcName)s -",
    "%(message)s",
)
logging.basicConfig(format=LOG_FORMATTER)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("PyGithub").setLevel(logging.WARNING)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class AlfredBot:
    """Alfred Bot main class."""

    def __init__(self, configfile: str):
        """Initialize AlfredBot class."""
        try:
            logger.debug("Starting AlfredBot")
            # Read Alfred Bot configuration file
            self.configfile = configfile
            self.config = self.read_config()

            # Init Telegram Bot class
            telegram_config = self.config["TelegramBot"]
            self.telegrambot = TelegramBot(telegram_config)

            # Only execute Telegram Bot polling if testing
            # is not enabled into configfile
            if not self.config["Miscellaneous"]["TESTING"]:  # pragma: no cover
                self.telegram_polling()

        except KeyboardInterrupt:
            self.telegrambot.send_message("See you soon! :)")
            logger.info("Catched KeyboardInterrupt. Bye :)")
            sys.exit()

    def read_config(self):
        """Read Alfred TOML configuration file."""
        with open(self.configfile, "rb") as config_file:
            config = tomli.load(config_file)
        # Disable testing if Miscellaneus section
        # is not defined as key into configuration dictionary
        if "Miscellaneous" not in config.keys():
            config["Miscellaneous"] = {"TESTING": True}
        return config

    def telegram_polling(self):
        """Read new Telegram messages through polling mechanism."""
        last_message_id = -1
        while True:
            message_id = self.telegrambot.extract_message_id()
            # Discard first iteration until now incoming message
            if last_message_id == -1:
                last_message_id = message_id

            # Check if new message is available
            if message_id:
                # Check if new message is different from last one
                if message_id != last_message_id:
                    message = self.telegrambot.read_message()
                    self.processing_incoming_message(message)
                    last_message_id = message_id
            else:
                break

    def get_api_keyphrase(self):
        """Get list of API keyphrases."""
        phrases = []
        # Extract API packages defined into configuration file
        packages = self.config["API"].keys()
        logger.debug("API packages %s", packages)
        for package in packages:
            # Extract API modules from each API package
            modules = self.config["API"][package].keys()
            logger.debug("API modules %s", modules)
            for module in modules:
                # Extract API actions from each API modules
                actions = self.config["API"][package][module].keys()
                logger.debug("Actions %s", actions)
                for action in actions:
                    # Try to extract phrase from API action configuration
                    try:
                        phrases.append(
                            self.config["API"][package][module][action][
                                "phrase"
                            ]
                        )
                    # Except KeyError if no phrase is defined and TypeError
                    # if no action is defined
                    except (KeyError, TypeError):
                        continue
        return phrases

    def get_api_function(self, phrase: str):
        """Get API and function through phrase."""
        packages = self.config["API"].keys()
        # For each package, search incoming message into `phrase`
        # subsection of API configuration defined into configfile
        for package in packages:
            package_config = self.config["API"][package]
            class_actions = package_config.keys()
            for class_action in class_actions:
                action_config = package_config[class_action]
                actions = action_config.keys()
                for action in actions:
                    try:
                        if phrase == action_config[action]["phrase"]:
                            module = action_config[action]["module"]
                            return f"API.{package}.{module}.{class_action}"
                    # Avoid KeyError and TypeError errors in case of non-API
                    # configuration section
                    except (KeyError, TypeError):
                        continue
        return None

    def processing_incoming_message(self, message: str):
        """Check incoming message.

        Compare it against phrases defined by configuration.
        """
        logger.info("Received message: %s", message)
        api_phrases = self.get_api_keyphrase()
        if message in api_phrases:
            # Get API and function through message
            # with format API.package.module.class_action
            module_aux = self.get_api_function(message)

            # Extract all but last element of module_aux
            # spliited by dot character to extract the
            # module name
            module_name = ".".join(module_aux.split(".")[:-1])

            # Extract class by last element of module_aux
            # splitted by dot character to etract the
            # class name
            class_name = module_aux.split(".")[-1]

            # Load module dynamically and class
            module = importlib.import_module(module_name)
            dynamic_class = getattr(module, class_name)

            # Run API process action function and retrieve string result
            result = dynamic_class(self.configfile).process_action(message)

            # Send result to Telegram Bot
            self.telegrambot.send_message(result)
        else:
            logger.info("No API phrase found for %s", message)
            error_msg = (
                f"I don't have any action for {message}",
                "Please, try again",
            )
            self.telegrambot.send_message(error_msg)


def argument_parser():
    """Argument parser."""
    args = argparse.ArgumentParser()
    args.add_argument(
        "--config",
        help="""AlfredBot's main configfile""",
        default="config/alfred.toml",
    )

    return args.parse_args()


if __name__ == "__main__":
    # Argument parser
    args = argument_parser()

    # Launch AlfredBot
    AlfredBot(args.config)
