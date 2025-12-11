# lab6_car_service/car_station.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .dining import Dineable
from .refueling import Refuelable
from .queues import Queue
from .models import Car, CarType, PassengerType, ServiceStats


@dataclass
class CarStation:
    """
    CarStation composed of:
      - a Queue<Car>
      - a Refuelable
      - an optional Dineable

    It uses dependency injection: the queue, refuel and dining services,
    and stats object are all injected from outside.
    """

    name: str
    car_type: CarType
    passenger_type: PassengerType
    queue: Queue[Car]
    refueling_service: Refuelable
    dining_service: Optional[Dineable]
    stats: ServiceStats

    def add_car(self, car: Car) -> None:
        """
        Add a car to the station queue.
        Validate that this station actually supports this car
        (matches type and passenger type).
        """
        if car.type != self.car_type or car.passengers != self.passenger_type:
            raise ValueError(
                f"{self.name} cannot serve car {car.id} of type "
                f"{car.type}/{car.passengers}"
            )
        self.queue.enqueue(car)

    def serve_cars(self) -> None:
        print(f"\n--- SERVING at {self.name} ---")

        while not self.queue.is_empty():
            car = self.queue.dequeue()

            print(f"[SERVE] Car {car.id} arriving at {self.name}")

            # Refuel
            print(f"[ACTION] Refueling car {car.id}")
            self.refueling_service.refuel(car.id)
            self.stats.register_refuel(car)

            # Dining
            if car.is_dining:
                print(f"[ACTION] Serving dinner for car {car.id}")
                self.dining_service.serve_dinner(car.id)
            else:
                print(f"[SKIP] Car {car.id} does not require dining")

            self.stats.register_dining(car)

        print(f"[DONE] {self.name} queue is now empty\n")

