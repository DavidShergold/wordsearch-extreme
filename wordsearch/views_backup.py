from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import WordSearchPuzzle, WordSearchAttempt, PuzzleRating
from .serializers import (
    WordSearchPuzzleSerializer, 
    WordSearchAttemptSerializer,
    PuzzleRatingSerializer
)


# Traditional Django views
def home(request):
    """Home page with featured puzzles."""
    featured_puzzles = WordSearchPuzzle.objects.filter(is_public=True)[:6]
    context = {
        'featured_puzzles': featured_puzzles,
    }
    return render(request, 'wordsearch/home.html', context)


def puzzle_list(request):
    """List all public puzzles."""
    puzzles = WordSearchPuzzle.objects.filter(is_public=True)
    difficulty = request.GET.get('difficulty')
    if difficulty:
        puzzles = puzzles.filter(difficulty=difficulty)
    
    context = {
        'puzzles': puzzles,
        'difficulty_choices': WordSearchPuzzle.DIFFICULTY_CHOICES,
        'selected_difficulty': difficulty,
    }
    return render(request, 'wordsearch/puzzle_list.html', context)


def puzzle_detail(request, pk):
    """Display a specific puzzle."""
    puzzle = get_object_or_404(WordSearchPuzzle, pk=pk, is_public=True)
    puzzle.increment_play_count()
    
    user_attempt = None
    if request.user.is_authenticated:
        user_attempt, created = WordSearchAttempt.objects.get_or_create(
            puzzle=puzzle,
            user=request.user
        )
    
    context = {
        'puzzle': puzzle,
        'user_attempt': user_attempt,
    }
    return render(request, 'wordsearch/puzzle_detail.html', context)


@login_required
def puzzle_create(request):
    """Create a new puzzle."""
    return render(request, 'wordsearch/puzzle_create.html')


# API ViewSets for REST API
class WordSearchPuzzleViewSet(viewsets.ModelViewSet):
    """ViewSet for WordSearch puzzles."""
    
    queryset = WordSearchPuzzle.objects.filter(is_public=True)
    serializer_class = WordSearchPuzzleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def play(self, request, pk=None):
        """Increment play count when puzzle is played."""
        puzzle = self.get_object()
        puzzle.increment_play_count()
        return Response({'status': 'play count incremented'})
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get puzzle statistics."""
        puzzle = self.get_object()
        attempts = puzzle.attempts.count()
        completions = puzzle.attempts.filter(is_completed=True).count()
        avg_rating = puzzle.ratings.aggregate(avg=models.Avg('rating'))['avg']
        
        return Response({
            'play_count': puzzle.play_count,
            'attempts': attempts,
            'completions': completions,
            'completion_rate': (completions / attempts * 100) if attempts > 0 else 0,
            'average_rating': round(avg_rating, 2) if avg_rating else None,
        })


class WordSearchAttemptViewSet(viewsets.ModelViewSet):
    """ViewSet for puzzle attempts."""
    
    serializer_class = WordSearchAttemptSerializer
    
    def get_queryset(self):
        return WordSearchAttempt.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PuzzleRatingViewSet(viewsets.ModelViewSet):
    """ViewSet for puzzle ratings."""
    
    serializer_class = PuzzleRatingSerializer
    
    def get_queryset(self):
        return PuzzleRating.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
