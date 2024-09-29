from django.urls import path
from .views import FormView, FormResponseView, FormAnalyticsView, FormListView


urlpatterns = [
    path('forms/', FormListView.as_view(), name='form_list'),
    path('forms/create/', FormView.as_view(), name='form_create'),
    path('forms/<str:form_id>/', FormView.as_view(), name='form_detail'),
    path('forms/<str:form_id>/submit/', FormResponseView.as_view(), name='form_submit'),
    path('forms/<str:form_id>/responses/', FormResponseView.as_view(), name='form_responses'),
    path('forms/<str:form_id>/analytics/', FormAnalyticsView.as_view(), name='form_analytics'),
]