from django.urls import path
from .views import transform_data, get_transformed_data

urlpatterns = [
    path('transform/', transform_data, name='transform_data'),
    path('transformed-data/', get_transformed_data, name='get_transformed_data'),
]