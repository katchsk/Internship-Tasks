from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemListGetAPIView, ItemListPostAPIView, ItemViewSet, ItemUpdateAPIView,  ItemDeleteAPIView, ItemPartialUpdateAPIView

router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('items/', ItemListGetAPIView.as_view(), name='item-list-get'),
    path('items/create/', ItemListPostAPIView.as_view(), name='item-list-post'),
    path('items/<int:pk>/', ItemUpdateAPIView.as_view(), name='item-list-put'),
    path('items/<int:pk>/delete/', ItemDeleteAPIView.as_view(), name='items-list-delete'),
    path('items/<int:pk>/patch/', ItemPartialUpdateAPIView.as_view(), name='items-list-patch'),
]