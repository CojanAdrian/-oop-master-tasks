# lab6_car_service/refueling.py
from __future__ import annotations

from abc import ABC, abstractmethod


class Refuelable(ABC):
    """
    Refuelable interface: exactly one abstract method.
    """

    @abstractmethod
    def refuel(self, car_id: int) -> None:
        ...


class ElectricStation(Refuelable):
    def refuel(self, car_id: int) -> None:
        print(f"Refueling electric car {car_id}.")


class GasStation(Refuelable):
    def refuel(self, car_id: int) -> None:
        print(f"Refueling gas car {car_id}.")
