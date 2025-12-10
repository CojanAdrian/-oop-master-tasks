# lab6_car_service/queues.py
from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from typing import Deque, Generic, List, TypeVar

T = TypeVar("T")


class Queue(ABC, Generic[T]):
    """
    Generic Queue<T> interface with enqueue/dequeue,
    as in lab requirements.
    """

    @abstractmethod
    def enqueue(self, item: T) -> None:
        ...

    @abstractmethod
    def dequeue(self) -> T:
        ...

    @abstractmethod
    def is_empty(self) -> bool:
        ...


class ListQueue(Queue[T]):
    """
    Simple list-based FIFO queue.
    """

    def __init__(self) -> None:
        self._data: List[T] = []

    def enqueue(self, item: T) -> None:
        self._data.append(item)
        print(f"[QUEUE] Enqueued {item}")

    def dequeue(self) -> T:
        if not self._data:
            raise IndexError("dequeue from empty queue")
        return self._data.pop(0)

    def is_empty(self) -> bool:
        return not self._data


class DequeQueue(Queue[T]):
    """
    Queue backed by collections.deque.
    """

    def __init__(self) -> None:
        self._data: Deque[T] = deque()

    def enqueue(self, item: T) -> None:
        self._data.append(item)
        print(f"[QUEUE] Enqueued {item}")

    def dequeue(self) -> T:
        if not self._data:
            raise IndexError("dequeue from empty queue")
        return self._data.popleft()

    def is_empty(self) -> bool:
        return not self._data


class BoundedQueue(Queue[T]):
    """
    Queue with max capacity, demonstrates a different
    implementation behavior (throws on overflow).
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._data: List[T] = []

    def enqueue(self, item: T) -> None:
        if len(self._data) >= self._capacity:
            raise OverflowError("queue is full")
        self._data.append(item)
        print(f"[QUEUE] Enqueued {item}")

    def dequeue(self) -> T:
        if not self._data:
            raise IndexError("dequeue from empty queue")
        return self._data.pop(0)

    def is_empty(self) -> bool:
        return not self._data
