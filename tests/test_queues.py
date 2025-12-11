# tests/test_queues.py
import pytest

from lab6_car_service.queues import BoundedQueue, DequeQueue, ListQueue


def _exercise_int_queue(queue):
    assert queue.is_empty()
    for i in range(3):
        queue.enqueue(i)
    assert not queue.is_empty()
    assert queue.dequeue() == 0
    assert queue.dequeue() == 1
    assert queue.dequeue() == 2
    assert queue.is_empty()
    with pytest.raises(IndexError):
        queue.dequeue()


def test_list_queue_basic():
    q = ListQueue[int]()
    _exercise_int_queue(q)


def test_deque_queue_basic():
    q = DequeQueue[int]()
    _exercise_int_queue(q)


def test_bounded_queue_overflow_and_order():
    q = BoundedQueue[str](capacity=2)
    assert q.is_empty()

    q.enqueue("a")
    q.enqueue("b")
    assert not q.is_empty()

    with pytest.raises(OverflowError):
        q.enqueue("c")

    assert q.dequeue() == "a"
    assert q.dequeue() == "b"
    assert q.is_empty()

    with pytest.raises(IndexError):
        q.dequeue()
