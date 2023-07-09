from django.urls import path
from access_office import views

urlpatterns = [
    path('access-office', views.AccessOffice.as_view(), name='access_office'),
    path('access-office/update-document/<int:pk>', views.UpdateDocument.as_view(), name='update_document'),
    path('create-crossing-point', views.CreateCrossingPoint.as_view(), name='create_crossing_point'),
    path('search-document', views.SearchDocument.as_view(), name='search_document'),
    path('create-document', views.CreateDocument.as_view(), name='create_document'),
    path('security', views.Security.as_view(), name='security'),
    path('security/pass/<int:pk>', views.SecurityPass.as_view(), name='security_pass'),
    path('crossing-point', views.CrossingPointView.as_view(), name='crossing_point'),
    path('crossing-point/update/<int:pk>', views.CrossingPointUpdate.as_view(), name='crossing_point_update'),
    path('crossing-point/delete/<int:pk>', views.CrossingPointDelete.as_view(), name='crossing_point_delete'),
    path('custom-status', views.CreateCustomStatus.as_view(), name='custom_status'),
    path('custom-status/view', views.CustomStatusView.as_view(), name='custom_status_view'),
    path('custom-status/update/<int:pk>', views.CustomStatusUpdate.as_view(), name='custom_status_update'),
    path('custom-status/delete/<int:pk>', views.CustomStatusDelete.as_view(), name='custom_status_delete'),
]
