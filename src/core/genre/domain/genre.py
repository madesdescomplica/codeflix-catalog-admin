from uuid import UUID, uuid4
from dataclasses import dataclass, field


@dataclass
class Genre:
    name: str
    is_active: bool = True
    id: UUID = field(default_factory=uuid4)
    categories: set[UUID] = field(default_factory=set)

    def __post_init__(self):
        self.validate()

    def validate(self):
        if not self.name:
            raise ValueError("name can not be empty or null")

        if len(self.name) > 255:
            raise ValueError("name can not be longer than 255 caracteres")

    def __str__(self) -> str:
        return f"id: {self.id}, \
            name: {self.name}, \
            is_active: {self.is_active}"

    def __repr__(self) -> str:
        return f"id: {self.id}, \
            name: {self.name}, \
            is_active: {self.is_active}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Genre):
            return False

        return self.id == other.id

    def update_name(self, name):
        self.name = name
        self.validate()

    def activate(self):
        self.is_active = True
        self.validate()

    def deactivate(self):
        self.is_active = False
        self.validate()

    def add_category(self, category_id: UUID):
        self.categories.add(category_id)
        self.validate()

    def remove_category(self, category_id: UUID):
        self.categories.remove(category_id)
        self.validate()