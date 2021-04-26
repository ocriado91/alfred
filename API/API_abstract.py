#!/usr/bin/env python3

from abc import ABC, abstractmethod
from TelegramBot import telegrambot
class API(ABC):

    @abstractmethod
    def process_action(self,
                      message: str,
                      retry: int):
        None

    @abstractmethod
    def show_options(self):
        None