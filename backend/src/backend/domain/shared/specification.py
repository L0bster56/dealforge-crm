from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

# Будет какой то определенный тип данных
T = TypeVar("T")


class Specification(ABC, Generic[T]):
    """
    Абстрактный класс спецификации
    """
    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        """
        Метод который будет проверять подходит ли он по правилам
        """

    def __and__(self, other: "Specification[T]") -> "AndSpecification[T]":
        return AndSpecification(self, other)

    def __or__(self, other: "Specification[T]") -> "OrSpecification[T]":
        return OrSpecification(self, other)

    def __invert__(self) -> "NotSpecification[T]":
        return NotSpecification(self)

@dataclass
class AndSpecification(Specification[T]):
    left: Specification[T]
    right: Specification[T]

    def is_satisfied_by(self, candidate: T) -> bool:
        return self.left.is_satisfied_by(candidate) and self.right.is_satisfied_by(candidate)


@dataclass
class OrSpecification(Specification[T]):
    left: Specification[T]
    right: Specification[T]

    def is_satisfied_by(self, candidate: T) -> bool:
        return self.left.is_satisfied_by(candidate) or self.right.is_satisfied_by(candidate)


@dataclass
class NotSpecification(Specification[T]):
    spec: Specification[T]

    def is_satisfied_by(self, candidate: T) -> bool:
        return not self.spec.is_satisfied_by(candidate)