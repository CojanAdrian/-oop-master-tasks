# lab6_car_service/semaphore.py
from __future__ import annotations

from typing import Dict, Iterable, Tuple

from .car_station import CarStation
from .models import Car, CarType, PassengerType


class Semaphore:
    """
    Guides cars to the correct CarStation based on:
        - Car type (ELECTRIC / GAS)
        - Passenger type (PEOPLE / ROBOTS)

    This is the testable 'router' class for Task 4.
    """

    def __init__(self, stations: Iterable[CarStation]) -> None:
        self._station_map: Dict[Tuple[CarType, PassengerType], CarStation] = {}

        for st in stations:
            key = (st.car_type, st.passenger_type)
            if key in self._station_map:
                raise ValueError(f"Duplicate station for {key}: {st.name}")
            self._station_map[key] = st

    def dispatch(self, car: Car) -> None:
        key = (car.type, car.passengers)
        station = self._station_map.get(key)

        if station is None:
            raise ValueError(f"No station configured for {key}")

        print(f"[ROUTING] Car {car.id} | Type={car.type} | Passengers={car.passengers} → {station.name}")
        station.add_car(car)

