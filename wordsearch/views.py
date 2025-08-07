from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db import models
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import json
import random
import string
from .models import WordSearchPuzzle, WordSearchAttempt, PuzzleRating
from .serializers import (
    WordSearchPuzzleSerializer,
    WordSearchAttemptSerializer,
    PuzzleRatingSerializer
)


def generate_word_search_grid(words, grid_size):
    """Generate a word search grid with the given words placed randomly."""
    words = [word.upper() for word in words]
    grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]
    placed_words = []
    
    # Directions: right, down, diagonal down-right, diagonal down-left
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
        (0, -1),  # left
        (-1, 0),  # up
        (-1, -1), # diagonal up-left
        (-1, 1),  # diagonal up-right
    ]
    
    def can_place_word(word, row, col, direction):
        dr, dc = direction
        for i, letter in enumerate(word):
            r, c = row + i * dr, col + i * dc
            if not (0 <= r < grid_size and 0 <= c < grid_size):
                return False
            if grid[r][c] != '' and grid[r][c] != letter:
                return False
        return True
    
    def place_word(word, row, col, direction):
        dr, dc = direction
        positions = []
        for i, letter in enumerate(word):
            r, c = row + i * dr, col + i * dc
            grid[r][c] = letter
            positions.append({'row': r, 'col': c})
        return positions
    
    # Try to place each word
    for word in words:
        placed = False
        attempts = 0
        max_attempts = 100
        
        while not placed and attempts < max_attempts:
            direction = random.choice(directions)
            row = random.randint(0, grid_size - 1)
            col = random.randint(0, grid_size - 1)
            
            if can_place_word(word, row, col, direction):
                positions = place_word(word, row, col, direction)
                placed_words.append({
                    'word': word,
                    'positions': positions,
                    'direction': direction
                })
                placed = True
            
            attempts += 1
        
        if not placed:
            # If we couldn't place the word, skip it for now
            continue
    
    # Fill remaining cells with random letters
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == '':
                grid[i][j] = random.choice(string.ascii_uppercase)
    
    return {
        'grid': grid,
        'words': [item['word'] for item in placed_words],
        'placed_words': placed_words
    }


# Traditional Django views
def generate_random_puzzle(level):
    """Generate a random word search puzzle for a given level."""
    import random
    
    # Use level as seed for consistent puzzles per level
    random.seed(level)
    
    # Common word lists for random selection
    word_lists = [
        ['PYTHON', 'DJANGO', 'CODE', 'WEB', 'APP', 'DATA', 'API', 'JSON', 'HTML', 'CSS'],
        ['OCEAN', 'MOUNTAIN', 'FOREST', 'RIVER', 'BEACH', 'VALLEY', 'DESERT', 'LAKE', 'HILL', 'CAVE'],
        ['MUSIC', 'GUITAR', 'PIANO', 'DRUMS', 'VIOLIN', 'SONG', 'RHYTHM', 'MELODY', 'HARMONY', 'BEAT'],
        ['SCIENCE', 'ATOM', 'MOLECULE', 'ENERGY', 'FORCE', 'GRAVITY', 'LIGHT', 'MATTER', 'SPACE', 'TIME'],
        ['FOOD', 'PIZZA', 'PASTA', 'BURGER', 'SALAD', 'SOUP', 'BREAD', 'CHEESE', 'FRUIT', 'MEAT'],
        ['SPORT', 'SOCCER', 'TENNIS', 'BASKETBALL', 'FOOTBALL', 'BASEBALL', 'HOCKEY', 'GOLF', 'SWIM', 'RUN'],
        ['ANIMAL', 'LION', 'TIGER', 'ELEPHANT', 'GIRAFFE', 'ZEBRA', 'MONKEY', 'BEAR', 'WOLF', 'EAGLE'],
        ['COLOR', 'RED', 'BLUE', 'GREEN', 'YELLOW', 'PURPLE', 'ORANGE', 'BLACK', 'WHITE', 'PINK', 'BROWN'],
        ['WEATHER', 'SUNNY', 'RAINY', 'CLOUDY', 'WINDY', 'STORMY', 'FOGGY', 'SNOWY', 'HOT', 'COLD', 'WARM'],
        ['TRAVEL', 'PLANE', 'TRAIN', 'CAR', 'BOAT', 'BIKE', 'WALK', 'HOTEL', 'BEACH', 'CITY', 'COUNTRY']
    ]
    
    # Select random word list
    words = random.choice(word_lists).copy()
    
    # Adjust difficulty based on level
    if level <= 5:
        num_words = min(6, len(words))
    elif level <= 10:
        num_words = min(8, len(words))
    elif level <= 15:
        num_words = min(10, len(words))
    else:
        num_words = len(words)
    
    # Select random words
    selected_words = random.sample(words, num_words)
    
    # Generate grid
    grid_result = generate_word_search_grid(selected_words, 20)
    
    # Create puzzle data structure
    puzzle_data = {
        'id': level,
        'title': f'Level {level}',
        'description': f'Find {num_words} hidden words',
        'difficulty': 'easy' if level <= 5 else 'medium' if level <= 15 else 'hard',
        'grid_data': grid_result['grid'],
        'words_data': [
            {
                'word': word,
                'found': False
            } for word in grid_result['words']
        ],
        'grid_size': 20,
        'words_list': grid_result['words']
    }
    
    return puzzle_data


def home(request):
    """Home page with the current puzzle to solve."""
    context = {}
    
    # Get leaderboard data - top 10 players by highest level reached
    from django.db.models import Max
    leaderboard = User.objects.annotate(
        highest_level=Max('puzzle_attempts__puzzle__id', 
                         filter=models.Q(puzzle_attempts__is_completed=True))
    ).exclude(
        highest_level__isnull=True
    ).order_by('-highest_level')[:10]
    
    context['leaderboard'] = leaderboard
    
    if request.user.is_authenticated:
        # Get the next level the user hasn't completed
        completed_levels = set(WordSearchAttempt.objects.filter(
            user=request.user, 
            is_completed=True
        ).values_list('puzzle_id', flat=True))
        
        # Find next uncompleted level (starting from 1)
        current_level = 1
        while current_level in completed_levels:
            current_level += 1
        
        # Generate current puzzle
        current_puzzle_data = generate_random_puzzle(current_level)
        
        # Convert to object-like structure for template compatibility
        class PuzzleObject:
            def __init__(self, data):
                for key, value in data.items():
                    setattr(self, key, value)
        
        current_puzzle = PuzzleObject(current_puzzle_data)
        
        # Calculate progress (show progress for first 100 levels)
        max_display_level = 100
        completed_count = len([l for l in completed_levels if l <= max_display_level])
        total_levels = max_display_level
        progress_percentage = int((completed_count / total_levels) * 100)
        
        context.update({
            'current_puzzle': current_puzzle,
            'completed_count': completed_count,
            'total_puzzles': f'{completed_count + 1}+',  # Show as "5+" for example
            'progress_percentage': min(progress_percentage, 100),
            'current_level': current_level,
        })
        
    else:
        # For anonymous users, show level 1
        current_puzzle_data = generate_random_puzzle(1)
        
        class PuzzleObject:
            def __init__(self, data):
                for key, value in data.items():
                    setattr(self, key, value)
        
        current_puzzle = PuzzleObject(current_puzzle_data)
        
        context.update({
            'current_puzzle': current_puzzle,
            'show_login_prompt': True,
            'completed_count': 0,
            'total_puzzles': '∞',
            'progress_percentage': 0,
            'current_level': 1,
        })
    
    return render(request, 'wordsearch/home.html', context)


@login_required
def complete_level(request):
    """Mark a level as completed for the current user."""
    if request.method == 'POST':
        level = request.POST.get('level')
        if level:
            try:
                level = int(level)
                # Create or get a puzzle record for this level
                puzzle, created = WordSearchPuzzle.objects.get_or_create(
                    id=level,
                    defaults={
                        'title': f'Level {level}',
                        'description': f'Randomly generated puzzle for level {level}',
                        'created_by': request.user,
                        'width': 20,
                        'height': 20,
                        'grid_data': {},  # We don't need to store the grid
                        'words_data': [],
                        'is_public': True
                    }
                )
                
                # Mark as completed
                attempt, created = WordSearchAttempt.objects.get_or_create(
                    user=request.user,
                    puzzle=puzzle,
                    defaults={'is_completed': True}
                )
                
                if not attempt.is_completed:
                    attempt.is_completed = True
                    attempt.save()
                
                return JsonResponse({'success': True, 'next_level': level + 1})
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid level'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


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
@require_http_methods(["GET", "POST"])
def puzzle_create(request):
    """Create a new puzzle."""
    if request.method == 'POST':
        try:
            # Get form data
            title = request.POST.get('title', '').strip()
            category = request.POST.get('category', '').strip()
            difficulty = request.POST.get('difficulty', '').strip()
            description = request.POST.get('description', '').strip()
            words = [word.strip().upper() for word in request.POST.getlist('words[]') if word.strip()]
            
            # Validation
            if not title:
                messages.error(request, 'Title is required.')
                return render(request, 'wordsearch/puzzle_create.html')
            
            if not difficulty:
                messages.error(request, 'Difficulty level is required.')
                return render(request, 'wordsearch/puzzle_create.html')
            
            if len(words) < 3:
                messages.error(request, 'At least 3 words are required.')
                return render(request, 'wordsearch/puzzle_create.html')
            
            # Validate words
            for word in words:
                if not word.isalpha() or len(word) < 3 or len(word) > 12:
                    messages.error(request, f'Word "{word}" must be 3-12 letters only.')
                    return render(request, 'wordsearch/puzzle_create.html')
            
            # Check for duplicates
            if len(words) != len(set(words)):
                messages.error(request, 'Duplicate words are not allowed.')
                return render(request, 'wordsearch/puzzle_create.html')
            
            # Set grid size based on difficulty
            grid_sizes = {'easy': 8, 'medium': 12, 'hard': 16, 'extreme': 20}
            grid_size = grid_sizes.get(difficulty, 12)
            
            # Generate the puzzle grid
            puzzle_data = generate_word_search_grid(words, grid_size)
            
            # Create the puzzle
            puzzle = WordSearchPuzzle.objects.create(
                title=title,
                category=category,
                difficulty=difficulty,
                description=description,
                grid_size=grid_size,
                grid_data=puzzle_data['grid'],
                words=puzzle_data['words'],
                solution_data=puzzle_data['placed_words'],
                created_by=request.user,
                is_public=True
            )
            
            messages.success(request, f'Puzzle "{title}" created successfully!')
            return redirect('wordsearch:puzzle_detail', pk=puzzle.pk)
            
        except Exception as e:
            messages.error(request, f'Error creating puzzle: {str(e)}')
            return render(request, 'wordsearch/puzzle_create.html')
    
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
