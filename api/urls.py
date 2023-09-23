from django.urls import path

from rest_framework.routers import DefaultRouter
from api.views import BookReviewViewSet
# from api.views import BookReviewApiView, BookReviewDetailApiView

app_name = "api"

router = DefaultRouter()
router.register('reviews', BookReviewViewSet, basename="review")

urlpatterns = router.urls



# urlpatterns = [
#     path('reviews/', BookReviewApiView.as_view(), name='reviews_app'),
#     path('reviews/<int:pk>/', BookReviewDetailApiView.as_view(), name='review_detail_api'),
# ]
