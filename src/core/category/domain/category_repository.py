from abc import ABC, abstractmethod
from uuid import UUID

from .category import Category


class CategoryRepository(ABC):

    @abstractmethod
    def save(self, category: Category):
        raise NotImplementedError('Should implement method: save')

    @abstractmethod
    def get_by_id(self, id: UUID) -> Category | None:
        raise NotImplementedError('Should implement method: get_by_id')