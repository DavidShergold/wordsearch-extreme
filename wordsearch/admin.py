from django.contrib import admin
from .models import WordSearchPuzzle, WordSearchAttempt, PuzzleRating


@admin.register(WordSearchPuzzle)
class WordSearchPuzzleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'difficulty', 'word_count', 'play_count', 'is_public', 'created_at']
    list_filter = ['difficulty', 'is_public', 'created_at']
    search_fields = ['title', 'description', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at', 'play_count']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'created_by', 'is_public')
        }),
        ('Puzzle Configuration', {
            'fields': ('width', 'height', 'difficulty')
        }),
        ('Puzzle Data', {
            'fields': ('grid_data', 'words_data'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('play_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(WordSearchAttempt)
class WordSearchAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'puzzle', 'is_completed', 'completion_percentage', 'started_at']
    list_filter = ['is_completed', 'started_at']
    search_fields = ['user__username', 'puzzle__title']
    readonly_fields = ['started_at', 'completion_percentage']
    
    def completion_percentage(self, obj):
        return f"{obj.completion_percentage:.1f}%"
    completion_percentage.short_description = "Completion %"


@admin.register(PuzzleRating)
class PuzzleRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'puzzle', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'puzzle__title']
    readonly_fields = ['created_at']
