from uuid import UUID

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.application.usecases import (
    GetCategoryRequest,
    GetCategory,
    ListCategory
)
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.category_app.serializers import (
    ListCategoryResponseSerializer,
    RetrieveCategoryRequestSerializer,
    RetrieveCategoryResponseSerializer
)


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        usecase = ListCategory(repository=DjangoORMCategoryRepository())
        response = usecase.execute()
        serializer = ListCategoryResponseSerializer(instance=response)

        return Response(
            status=HTTP_200_OK,
            data=serializer.data
        )

    def retrieve(self, request: Request, pk: None) -> Response:
        serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        use_case = GetCategory(repository=DjangoORMCategoryRepository())

        try:
            request = GetCategoryRequest(serializer.validated_data["id"])
            response = use_case.execute(request)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        category_out = RetrieveCategoryResponseSerializer(instance=response)

        return Response(
            status=HTTP_200_OK,
            data=category_out.data
        )