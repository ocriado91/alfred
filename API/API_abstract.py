#!/usr/bin/env python3

from abc import ABC, abstractmethod
class API(ABC):

    @abstractmethod
    def process_action(self,
                       message: str):
        None