from drf_spectacular.utils import extend_schema, extend_schema_view
from .serializers import (
    ListCategoryResponseSerializer,
    CreateCategoryRequestSerializer,
    CreateCategoryResponseSerializer,
    DeleteCategoryRequestSerializer,
    PartialUpdateCategoryRequestSerializer,
    RetrieveCategoryRequestSerializer,
    RetrieveCategoryResponseSerializer,
    UpdateCategoryRequestSerializer,
)

category_viewset_schema = extend_schema_view(
    list=extend_schema(
        tags=['Category'],
        responses={200: ListCategoryResponseSerializer},
    ),
    create=extend_schema(
        tags=['Category'],
        request=CreateCategoryRequestSerializer,
        responses={201: CreateCategoryResponseSerializer},
    ),
    retrieve=extend_schema(
        tags=['Category'],
        request=RetrieveCategoryRequestSerializer,
        responses={
            200: RetrieveCategoryResponseSerializer,
            404: {
                'description': 'Category not found',
                'content': {
                    'application/json': {
                        'example': {
                            'detail': 'Not found.'
                        }
                    }
                }
            }
        },
    ),
    update=extend_schema(
        tags=['Category'],
        request=UpdateCategoryRequestSerializer,
        responses={
            204: None,
            404: {
                'description': 'Category not found',
                'content': {
                    'application/json': {
                        'example': {
                            'detail': 'Not found.'
                        }
                    }
                }
            }
        }
    ),
    partial_update=extend_schema(
        tags=['Category'],
        request=PartialUpdateCategoryRequestSerializer,
        responses={
            204: None,
            404: {
                'description': 'Category not found',
                'content': {
                    'application/json': {
                        'example': {
                            'detail': 'Not found.'
                        }
                    }
                }
            }
        }
    ),
    destroy=extend_schema(
        tags=['Category'],
        request=DeleteCategoryRequestSerializer,
        responses={
            204: None,
            404: {
                'description': 'Category not found',
                'content': {
                    'application/json': {
                        'example': {
                            'detail': 'Not found.'
                        }
                    }
                }
            }
        }
    )
)
