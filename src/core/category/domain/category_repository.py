from abc import ABC, abstractmethod

from .category import Category


class CategoryRepository(ABC):

    @abstractmethod
    def save(self, category: Category):
        raise NotImplementedError('Should implement method: save')
