from uuid import UUID

from src.core.category.domain import Category
from .exceptions import InvalidCategoryData


def create_category(name: str, description: str = "", is_active: bool = True) -> UUID:
    try:
        category = Category(
            name=name,
            description=description,
            is_active=is_active
        )
    except ValueError as e:
        raise InvalidCategoryData(e)

    return category.id