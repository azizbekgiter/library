from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.book_views import BookViewSet
from .views.user_views import UserViewSet
from .views.borrow_views import BorrowRecordViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'users', UserViewSet)
router.register(r'borrow', BorrowRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
