# lab6_car_service/test_tasks_demo.py

print("\n==========================")
print(" TASK 1 — QUEUE DEMO")
print("==========================")


def demo_task1():
    from lab6_car_service.queues import ListQueue, DequeQueue, BoundedQueue

    q = ListQueue()
    print("\n[ListQueue]")
    q.enqueue(1);
    q.enqueue(2)
    print("Dequeued:", q.dequeue())
    print("Dequeued:", q.dequeue())

    q = DequeQueue()
    print("\n[DequeQueue]")
    q.enqueue(5);
    q.enqueue(6)
    print("Dequeued:", q.dequeue())
    print("Dequeued:", q.dequeue())

    q = BoundedQueue(2)
    print("\n[BoundedQueue]")
    q.enqueue(9);
    q.enqueue(10)
    try:
        q.enqueue(11)
    except Exception as e:
        print("Expected error:", e)


demo_task1()

print("\n==========================")
print(" TASK 2 — DINING & REFUELING DEMO")
print("==========================")


def demo_task2():
    from lab6_car_service.dining import PeopleDinner, RobotDinner
    from lab6_car_service.refueling import ElectricStation, GasStation

    ed = ElectricStation()
    gd = GasStation()
    pd = PeopleDinner()
    rd = RobotDinner()

    ed.refuel(1)
    gd.refuel(2)
    pd.serve_dinner(1)
    rd.serve_dinner(2)


demo_task2()

print("\n==========================")
print(" TASK 3 — CARSTATION DEMO")
print("==========================")


def demo_task3():
    from lab6_car_service.models import Car, CarType, PassengerType, ServiceStats
    from lab6_car_service.car_station import CarStation
    from lab6_car_service.dining import PeopleDinner
    from lab6_car_service.refueling import ElectricStation
    from lab6_car_service.queues import ListQueue

    stats = ServiceStats()

    station = CarStation(
        "ElectricPeopleStation",
        CarType.ELECTRIC,
        PassengerType.PEOPLE,
        ListQueue(),
        ElectricStation(),
        PeopleDinner(),
        stats
    )

    car1 = Car(1, CarType.ELECTRIC, PassengerType.PEOPLE, True, 30)
    car2 = Car(2, CarType.ELECTRIC, PassengerType.PEOPLE, False, 40)

    print("[ADD] Car 1 to station")
    station.add_car(car1)
    print("[ADD] Car 2 to station")
    station.add_car(car2)

    station.serve_cars()


demo_task3()

print("\n==========================")
print(" TASK 4 — SEMAPHORE ROUTING DEMO")
print("==========================")


def demo_task4():
    from lab6_car_service.models import Car, CarType, PassengerType, ServiceStats
    from lab6_car_service.queues import ListQueue
    from lab6_car_service.car_station import CarStation
    from lab6_car_service.refueling import ElectricStation, GasStation
    from lab6_car_service.dining import PeopleDinner, RobotDinner
    from lab6_car_service.semaphore import Semaphore

    stats = ServiceStats()

    ep = CarStation("ElectricPeople", CarType.ELECTRIC, PassengerType.PEOPLE,
                    ListQueue(), ElectricStation(), PeopleDinner(), stats)

    gr = CarStation("GasRobots", CarType.GAS, PassengerType.ROBOTS,
                    ListQueue(), GasStation(), RobotDinner(), stats)

    sem = Semaphore([ep, gr])

    c1 = Car(1, CarType.ELECTRIC, PassengerType.PEOPLE, False, 22)
    c2 = Car(2, CarType.GAS, PassengerType.ROBOTS, True, 41)

    print("[DISPATCH] Car 1")
    sem.dispatch(c1)
    print("[DISPATCH] Car 2")
    sem.dispatch(c2)

    ep.serve_cars()
    gr.serve_cars()


demo_task4()

print("\n==========================")
print(" TASK 5 — FULL SYNCHRONOUS RUN")
print("==========================")


def demo_task5():
    from lab6_car_service.sync_runner import run_sync
    run_sync()


demo_task5()

print("\n==========================")
print(" END OF DEMO")
print("==========================")
