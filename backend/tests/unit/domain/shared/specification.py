from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

# Будет определённый тип данных
T = TypeVar("T")

class Specification(ABC,Generic[T]):
    """
    Абстарктный метод Спецификации
    """
    @abstractmethod
    def is_satisfied_by(self,candidate: T)-> bool:
        """
        Метод который будет проверять подходит ли он правилам
        :param candidate:
        :return:
        """
    def __and__(self, other: "Specification[T]") -> "ANDSpecification[T]":
        return AndSpecification(self, other)

    def __or__(self, other:"Specification[T]") -> "ORSpecification[T]":
        return OrSpecification(self, other)
    def __invert__(self)-> "NOTSpecification[T]":
        return NotSpecification(self)
#upper & lower
@dataclass
class AndSpecification(Specification[T]):
    left: Specification[T]
    right: Specification[T]

    def is_satisfied_by(self,candidate: T) -> bool:
        return self.left.is_satisfied_by(candidate) and self.right.is_satisfied_by(candidate)

@dataclass
class OrSpecification(Specification[T]):
    left: Specification[T]
    right: Specification[T]
    def is_satisfied_by(self,candidate: T) -> bool:
        return self.left.is_satisfied_by(candidate) or self.right.is_satisfied_by(candidate)

@dataclass
class NotSpecification(Specification[T]):
    spec: Specification[T]
    def is_satisfied_by(self,candidate: T) -> bool:
        return not self.spec.is_satisfied_by(candidate)