from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("categories", CategoryViewSet)
router.register("comments", CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('toggle_like/<int:r_id>/', toggle_like),
    path('add_rating/<int:h_code>/', add_rating),
    path('add_to_favorites/<int:r_id>/', add_to_favorites),
]