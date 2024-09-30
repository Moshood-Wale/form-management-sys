from django.urls import path
from .views import FormViewSet, FormResponseViewSet, FormAnalyticsViewSet, FormListViewSet

urlpatterns = [
    path('forms/', FormListViewSet.as_view({'get': 'list'}), name='form_list'),
    path('forms/create/', FormViewSet.as_view({'post': 'create'}), name='form_create'),
    path('forms/<str:form_id>/', FormViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='form_detail'),
    path('forms/<str:form_id>/submit/', FormResponseViewSet.as_view({'post': 'submit'}), name='form_submit'),
    path('forms/<str:form_id>/responses/', FormResponseViewSet.as_view({'get': 'list'}), name='form_responses'),
    path('forms/<str:form_id>/analytics/', FormAnalyticsViewSet.as_view({'get': 'retrieve'}), name='form_analytics'),
]