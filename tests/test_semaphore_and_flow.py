# tests/test_semaphore_and_flow.py
import json
from pathlib import Path

from lab6_car_service.models import (
    Car,
    CarType,
    PassengerType,
)
from lab6_car_service.semaphore import Semaphore
from lab6_car_service.sync_runner import build_default_setup


def test_semaphore_routes_car_to_correct_station():
    stations, semaphore, stats = build_default_setup()

    gas_robot_car = Car(
        id=3,
        type=CarType.GAS,
        passengers=PassengerType.ROBOTS,
        is_dining=True,
        consumption=41,
    )

    semaphore.dispatch(gas_robot_car)

    # Exactly one station should have one car in its queue
    queue_sizes = [not st.queue.is_empty() for st in stations]
    assert sum(1 for val in queue_sizes if val) == 1

    # Serve cars to verify stats get updated correctly
    for st in stations:
        st.serve_cars()

    assert stats.gas_count == 1
    assert stats.robots_count == 1
    assert stats.dining_count == 1
    assert stats.gas_consumption == 41


def test_end_to_end_stats_match_example(tmp_path: Path):
    """
    Use the small example from the lab PDF:
        {"ELECTRIC": 2, "GAS": 1, "PEOPLE": 3, "ROBOTS": 0,
         "DINING": 1, "NOT_DINING": 2,
         "CONSUMPTION": {"ELECTRIC": 68, "GAS": 41}}
    """
    sample_cars = [
        {
            "id": 1,
            "type": "ELECTRIC",
            "passengers": "PEOPLE",
            "isDining": False,
            "consumption": 42,
        },
        {
            "id": 2,
            "type": "ELECTRIC",
            "passengers": "PEOPLE",
            "isDining": False,
            "consumption": 26,
        },
        {
            "id": 3,
            "type": "GAS",
            "passengers": "PEOPLE",
            "isDining": True,
            "consumption": 41,
        },
    ]

    # Save to temporary cars.json
    cars_file = tmp_path / "cars.json"
    cars_file.write_text(json.dumps(sample_cars), encoding="utf-8")

    from lab6_car_service.sync_runner import load_cars

    cars = load_cars(cars_file)
    stations, semaphore, stats = build_default_setup()

    for car in cars:
        semaphore.dispatch(car)

    for st in stations:
        st.serve_cars()

    result = stats.to_dict()
    expected = {
        "ELECTRIC": 2,
        "GAS": 1,
        "PEOPLE": 3,
        "ROBOTS": 0,
        "DINING": 1,
        "NOT_DINING": 2,
        "CONSUMPTION": {"ELECTRIC": 68, "GAS": 41},
    }

    assert result == expected
