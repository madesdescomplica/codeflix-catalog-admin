from dataclasses import dataclass
from uuid import UUID

from src.core.category.application import CategoryNotFound
from src.core.category.domain import CategoryRepository


@dataclass
class UpdateCategoryRequest:
    id: UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


@dataclass
class UpdateCategory:
    repository: CategoryRepository

    def execute(self, request: UpdateCategoryRequest) -> None:
        """
            - Busca categoria pelo ID
            - Atualiza categoria com os valores passados
            - Ativar/Desativar categoria
            - Salva categoria
        """
        category = self.repository.get_by_id(request.id)

        if category is None:
            raise CategoryNotFound(f"Category with id {request.id} not found")