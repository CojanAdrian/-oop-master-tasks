# lab6_car_service/sync_runner.py
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Tuple

from .car_station import CarStation
from .dining import PeopleDinner, RobotDinner
from .models import Car, CarType, PassengerType, ServiceStats
from .queues import ListQueue
from .refueling import ElectricStation, GasStation
from .semaphore import Semaphore


def load_cars(path: Path) -> List[Car]:
    """
    Load all cars from a synchronous generator output file.
    The file should contain a JSON array of car objects, e.g.:

    [
      {"id": 1, "type": "ELECTRIC", "passengers": "PEOPLE",
       "isDining": false, "consumption": 42},
      ...
    ]
    """
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    return [Car.from_dict(item) for item in raw]


def build_default_setup() -> Tuple[List[CarStation], Semaphore, ServiceStats]:
    """
    Build four CarStations:

        - ELECTRIC + PEOPLE
        - ELECTRIC + ROBOTS
        - GAS      + PEOPLE
        - GAS      + ROBOTS

    All of them share one ServiceStats instance.
    """
    stats = ServiceStats()

    electric_station = ElectricStation()
    gas_station = GasStation()
    people_dinner = PeopleDinner()
    robot_dinner = RobotDinner()

    stations: List[CarStation] = [
        CarStation(
            name="ElectricPeopleStation",
            car_type=CarType.ELECTRIC,
            passenger_type=PassengerType.PEOPLE,
            queue=ListQueue(),
            refueling_service=electric_station,
            dining_service=people_dinner,
            stats=stats,
        ),
        CarStation(
            name="ElectricRobotStation",
            car_type=CarType.ELECTRIC,
            passenger_type=PassengerType.ROBOTS,
            queue=ListQueue(),
            refueling_service=electric_station,
            dining_service=robot_dinner,
            stats=stats,
        ),
        CarStation(
            name="GasPeopleStation",
            car_type=CarType.GAS,
            passenger_type=PassengerType.PEOPLE,
            queue=ListQueue(),
            refueling_service=gas_station,
            dining_service=people_dinner,
            stats=stats,
        ),
        CarStation(
            name="GasRobotStation",
            car_type=CarType.GAS,
            passenger_type=PassengerType.ROBOTS,
            queue=ListQueue(),
            refueling_service=gas_station,
            dining_service=robot_dinner,
            stats=stats,
        ),
    ]

    semaphore = Semaphore(stations)
    return stations, semaphore, stats


def run_sync(path_to_cars_json: str = "cars.json") -> None:
    """
    Synchronous version (Option B):
        - Read all cars from cars.json
        - Route them using Semaphore
        - Call serve_cars on each CarStation
        - Print statistics (as JSON) at the end
    """
    cars_file = Path(path_to_cars_json)
    cars = load_cars(cars_file)

    stations, semaphore, stats = build_default_setup()

    # Route each car to its station
    for car in cars:
        semaphore.dispatch(car)

    # Serve queued cars in each station
    for st in stations:
        st.serve_cars()

    # Output final statistics
    print(json.dumps(stats.to_dict()))


if __name__ == "__main__":
    run_sync()
