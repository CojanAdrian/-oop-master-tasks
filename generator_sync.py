import json
import random
from pathlib import Path


def generate_car(car_id: int):
    return {
        "id": car_id,
        "type": random.choice(["ELECTRIC", "GAS"]),
        "passengers": random.choice(["PEOPLE", "ROBOTS"]),
        "isDining": random.choice([True, False]),
        "consumption": random.randint(10, 50)
    }


def generate_cars_file(count=20):
    queue_dir = Path("queue")
    queue_dir.mkdir(exist_ok=True)

    cars = [generate_car(i) for i in range(1, count + 1)]

    out_file = queue_dir / "cars.json"
    with out_file.open("w", encoding="utf-8") as f:
        json.dump(cars, f, indent=4)

    print(f"[SYNC] Generated {count} cars into {out_file}")


if __name__ == "__main__":
    generate_cars_file(20)
