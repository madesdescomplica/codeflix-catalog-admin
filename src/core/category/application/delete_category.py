from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain import CategoryRepository

@dataclass
class DeleteCategoryRequest:
    id: UUID

@dataclass
class DeleteCategory:
    repository: CategoryRepository

    def execute(self, request: DeleteCategoryRequest) -> None:
        self.repository.get_by_id(request.id)