# lab6_car_service/models.py
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict


class CarType(str, Enum):
    ELECTRIC = "ELECTRIC"
    GAS = "GAS"


class PassengerType(str, Enum):
    PEOPLE = "PEOPLE"
    ROBOTS = "ROBOTS"


@dataclass
class Car:
    id: int
    type: CarType
    passengers: PassengerType
    is_dining: bool
    consumption: int

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Car":
        """
        Convert from JSON dict:
        {"id": 1, "type": "ELECTRIC", "passengers": "PEOPLE",
         "isDining": false, "consumption": 42}
        """
        return Car(
            id=int(data["id"]),
            type=CarType(data["type"]),
            passengers=PassengerType(data["passengers"]),
            is_dining=bool(data["isDining"]),
            consumption=int(data["consumption"]),
        )


@dataclass
class ServiceStats:
    """
    Global statistics for all CarStations, as required in the lab.
    Output format must match generator stats example:
    {"ELECTRIC": 2, "GAS": 1, "PEOPLE": 3, "ROBOTS": 0,
     "DINING": 1, "NOT_DINING": 2,
     "CONSUMPTION": {"ELECTRIC": 68, "GAS": 41}}
    """

    electric_count: int = 0
    gas_count: int = 0
    people_count: int = 0
    robots_count: int = 0
    dining_count: int = 0
    not_dining_count: int = 0
    electric_consumption: int = 0
    gas_consumption: int = 0

    def register_refuel(self, car: Car) -> None:
        if car.type == CarType.ELECTRIC:
            self.electric_count += 1
            self.electric_consumption += car.consumption
        elif car.type == CarType.GAS:
            self.gas_count += 1
            self.gas_consumption += car.consumption

    def register_dining(self, car: Car) -> None:
        if car.is_dining:
            self.dining_count += 1
        else:
            self.not_dining_count += 1

        if car.passengers == PassengerType.PEOPLE:
            self.people_count += 1
        elif car.passengers == PassengerType.ROBOTS:
            self.robots_count += 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ELECTRIC": self.electric_count,
            "GAS": self.gas_count,
            "PEOPLE": self.people_count,
            "ROBOTS": self.robots_count,
            "DINING": self.dining_count,
            "NOT_DINING": self.not_dining_count,
            "CONSUMPTION": {
                "ELECTRIC": self.electric_consumption,
                "GAS": self.gas_consumption,
            },
        }
