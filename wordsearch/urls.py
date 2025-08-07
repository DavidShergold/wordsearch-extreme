from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API router
router = DefaultRouter()
router.register(r'puzzles', views.WordSearchPuzzleViewSet)
router.register(r'attempts', views.WordSearchAttemptViewSet, basename='attempt')
router.register(r'ratings', views.PuzzleRatingViewSet, basename='rating')

app_name = 'wordsearch'

urlpatterns = [
    # Web views
    path('', views.home, name='home'),
    path('complete-level/', views.complete_level, name='complete_level'),
    path('puzzles/', views.puzzle_list, name='puzzle_list'),
    path('puzzles/<int:pk>/', views.puzzle_detail, name='puzzle_detail'),
    path('puzzles/create/', views.puzzle_create, name='puzzle_create'),
    
    # API endpoints
    path('api/', include(router.urls)),
]
