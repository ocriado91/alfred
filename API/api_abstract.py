#!/usr/bin/env python3
"""Abstract class to implement Facade Design Pattern into API interfaces."""

from abc import ABC, abstractmethod


class API(ABC):
    """Abstract class."""

    @abstractmethod
    def process_action(self, message: str):
        """Process incoming message action."""
        pass
