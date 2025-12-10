# lab6_car_service/dining.py
from __future__ import annotations

from abc import ABC, abstractmethod


class Dineable(ABC):
    """
    Dineable interface: exactly one abstract method.
    """

    @abstractmethod
    def serve_dinner(self, car_id: int) -> None:
        ...


class PeopleDinner(Dineable):
    def serve_dinner(self, car_id: int) -> None:
        print(f"Serving dinner to people in car {car_id}.")


class RobotDinner(Dineable):
    def serve_dinner(self, car_id: int) -> None:
        print(f"Serving dinner to robots in car {car_id}.")
