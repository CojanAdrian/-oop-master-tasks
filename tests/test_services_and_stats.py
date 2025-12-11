# tests/test_services_and_stats.py
from lab6_car_service.car_station import CarStation
from lab6_car_service.dining import PeopleDinner
from lab6_car_service.models import (
    Car,
    CarType,
    PassengerType,
    ServiceStats,
)
from lab6_car_service.queues import ListQueue
from lab6_car_service.refueling import ElectricStation


def test_two_electric_stations_share_global_stats():
    """
    Imagine there are two car service stations with electric refuelers.
    The counts must be aggregated globally, not per station.
    """
    stats = ServiceStats()
    refueler = ElectricStation()
    diner = PeopleDinner()

    station1 = CarStation(
        name="E1",
        car_type=CarType.ELECTRIC,
        passenger_type=PassengerType.PEOPLE,
        queue=ListQueue(),
        refueling_service=refueler,
        dining_service=diner,
        stats=stats,
    )

    station2 = CarStation(
        name="E2",
        car_type=CarType.ELECTRIC,
        passenger_type=PassengerType.PEOPLE,
        queue=ListQueue(),
        refueling_service=refueler,
        dining_service=diner,
        stats=stats,
    )

    car1 = Car(
        id=1,
        type=CarType.ELECTRIC,
        passengers=PassengerType.PEOPLE,
        is_dining=True,
        consumption=10,
    )
    car2 = Car(
        id=2,
        type=CarType.ELECTRIC,
        passengers=PassengerType.PEOPLE,
        is_dining=False,
        consumption=20,
    )

    station1.add_car(car1)
    station2.add_car(car2)

    station1.serve_cars()
    station2.serve_cars()

    assert stats.electric_count == 2
    assert stats.electric_consumption == 30
    assert stats.dining_count == 1
    assert stats.not_dining_count == 1
    assert stats.people_count == 2
    assert stats.robots_count == 0


def test_station_cannot_accept_incompatible_car():
    stats = ServiceStats()
    refueler = ElectricStation()
    diner = PeopleDinner()
    station = CarStation(
        name="E-PEOPLE",
        car_type=CarType.ELECTRIC,
        passenger_type=PassengerType.PEOPLE,
        queue=ListQueue(),
        refueling_service=refueler,
        dining_service=diner,
        stats=stats,
    )

    bad_car = Car(
        id=99,
        type=CarType.GAS,
        passengers=PassengerType.PEOPLE,
        is_dining=False,
        consumption=15,
    )

    import pytest
    with pytest.raises(ValueError):
        station.add_car(bad_car)
