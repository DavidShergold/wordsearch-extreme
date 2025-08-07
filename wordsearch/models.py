from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import json


class WordSearchPuzzle(models.Model):
    """Model for word search puzzles."""
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('extreme', 'Extreme'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='puzzles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Puzzle configuration
    width = models.IntegerField(
        validators=[MinValueValidator(5), MaxValueValidator(50)],
        default=15
    )
    height = models.IntegerField(
        validators=[MinValueValidator(5), MaxValueValidator(50)],
        default=15
    )
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    
    # Puzzle data (stored as JSON)
    grid_data = models.JSONField(default=dict, help_text="The letter grid as 2D array")
    words_data = models.JSONField(default=list, help_text="List of words with positions")
    
    # Meta information
    is_public = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    play_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    @property
    def word_count(self):
        """Return the number of words in the puzzle."""
        return len(self.words_data) if self.words_data else 0
    
    def increment_play_count(self):
        """Increment the play count."""
        self.play_count += 1
        self.save(update_fields=['play_count'])


class WordSearchAttempt(models.Model):
    """Model to track user attempts at solving puzzles."""
    
    puzzle = models.ForeignKey(WordSearchPuzzle, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='puzzle_attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Progress tracking
    words_found = models.JSONField(default=list, help_text="List of found word IDs")
    time_taken = models.DurationField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['puzzle', 'user']
        ordering = ['-started_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.puzzle.title}"
    
    @property
    def completion_percentage(self):
        """Calculate completion percentage."""
        if not self.puzzle.word_count:
            return 0
        return (len(self.words_found) / self.puzzle.word_count) * 100


class PuzzleRating(models.Model):
    """Model for user ratings of puzzles."""
    
    puzzle = models.ForeignKey(WordSearchPuzzle, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='puzzle_ratings')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['puzzle', 'user']
        
    def __str__(self):
        return f"{self.user.username} rated {self.puzzle.title}: {self.rating}/5"
