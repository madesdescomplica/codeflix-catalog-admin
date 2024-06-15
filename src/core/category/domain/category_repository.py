from abc import ABC, abstractmethod
from uuid import UUID

from .category import Category


class CategoryRepository(ABC):

    @abstractmethod
    def save(self, category: Category) -> None:
        raise NotImplementedError('Should implement method: save')

    @abstractmethod
    def get_by_id(self, id: UUID) -> Category | None:
        raise NotImplementedError('Should implement method: get_by_id')

    @abstractmethod
    def update(self, category: Category) -> None:
        raise NotImplementedError('Should implement method: update')

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError('Should implement method: delete')

    @abstractmethod
    def list(self) -> list[Category]:
        raise NotImplementedError('Should implement method: list')