from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .services import FormService
from bson import errors as bson_errors
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


class FormView(APIView):
    @extend_schema(
        request=OpenApiTypes.OBJECT,
        responses={201: OpenApiTypes.OBJECT},
        description="Create a new form",
        examples=[
            OpenApiExample(
                'Valid input example',
                value={
                    'title': 'Sample Form',
                    'description': 'A sample form description',
                    'fields': [
                        {'name': 'Name', 'field_type': 'text', 'required': True},
                        {'name': 'Age', 'field_type': 'number', 'required': False}
                    ],
                    'created_by': 'admin'
                },
                request_only=True,
            ),
            OpenApiExample(
                'Valid output example',
                value={'id': '5f7b5b9b0b5b9b0b5b9b0b5b'},
                response_only=True,
            ),
        ]
    )
    def post(self, request):
        """Create a new form"""
        try:
            form_id = FormService.create_form(request.data)
            return Response({"id": form_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[OpenApiParameter("form_id", OpenApiTypes.STR, OpenApiParameter.PATH)],
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        description="Retrieve a form by ID"
    )
    def get(self, request, form_id):
        """Retrieve a form by ID"""
        try:
            form = FormService.get_form(form_id)
            if form:
                return Response(form)
            return Response({"error": "Form not found"}, status=status.HTTP_404_NOT_FOUND)
        except bson_errors.InvalidId:
            return Response({"error": "Invalid form ID"}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[OpenApiParameter("form_id", OpenApiTypes.STR, OpenApiParameter.PATH)],
        request=OpenApiTypes.OBJECT,
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        description="Update a form"
    )
    def put(self, request, form_id):
        """Update a form"""
        try:
            updated = FormService.update_form(form_id, request.data)
            if updated:
                return Response({"message": "Form updated successfully"})
            return Response({"error": "Form not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[OpenApiParameter("form_id", OpenApiTypes.STR, OpenApiParameter.PATH)],
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        description="Delete a form"
    )
    def delete(self, request, form_id):
        """Delete a form"""
        try:
            deleted = FormService.delete_form(form_id)
            if deleted:
                return Response({"message": "Form deleted successfully"})
            return Response({"error": "Form not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class FormResponseView(APIView):
    @extend_schema(
        parameters=[OpenApiParameter("form_id", OpenApiTypes.STR, OpenApiParameter.PATH)],
        request=OpenApiTypes.OBJECT,
        responses={201: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        description="Submit a response to a form"
    )
    def post(self, request, form_id):
        """Submit a response to a form"""
        try:
            response_id = FormService.submit_response(form_id, request.data)
            return Response({"id": response_id}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        parameters=[OpenApiParameter("form_id", OpenApiTypes.STR, OpenApiParameter.PATH)],
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        description="Get all responses for a form"
    )
    def get(self, request, form_id):
        """Get all responses for a form"""
        try:
            responses = FormService.get_form_responses(form_id)
            return Response(responses)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class FormAnalyticsView(APIView):
    @extend_schema(
        parameters=[OpenApiParameter("form_id", OpenApiTypes.STR, OpenApiParameter.PATH)],
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        description="Get analytics for a form"
    )
    def get(self, request, form_id):
        """Get analytics for a form"""
        try:
            analytics = FormService.get_form_analytics(form_id)
            return Response(analytics)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class FormListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class FormListView(APIView):
    pagination_class = FormListPagination

    @extend_schema(
        parameters=[
            OpenApiParameter("page", OpenApiTypes.INT, OpenApiParameter.QUERY),
            OpenApiParameter("page_size", OpenApiTypes.INT, OpenApiParameter.QUERY),
        ],
        responses={200: OpenApiTypes.OBJECT},
        description="Get all forms with pagination"
    )
    def get(self, request):
        """Get all forms with pagination"""
        try:
            forms = FormService.get_all_forms()
            paginator = self.pagination_class()
            paginated_forms = paginator.paginate_queryset(forms, request)
            return paginator.get_paginated_response(paginated_forms)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)