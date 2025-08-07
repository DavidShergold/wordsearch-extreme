from rest_framework import serializers
from django.contrib.auth.models import User
from .models import WordSearchPuzzle, WordSearchAttempt, PuzzleRating


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class WordSearchPuzzleSerializer(serializers.ModelSerializer):
    """Serializer for WordSearchPuzzle model."""
    
    created_by = UserSerializer(read_only=True)
    word_count = serializers.ReadOnlyField()
    
    class Meta:
        model = WordSearchPuzzle
        fields = [
            'id', 'title', 'description', 'created_by', 'created_at', 'updated_at',
            'width', 'height', 'difficulty', 'grid_data', 'words_data',
            'is_public', 'is_completed', 'play_count', 'word_count'
        ]
        read_only_fields = ['created_at', 'updated_at', 'play_count']
    
    def validate_grid_data(self, value):
        """Validate grid data structure."""
        if not isinstance(value, list):
            raise serializers.ValidationError("Grid data must be a list of lists.")
        
        height = self.initial_data.get('height', 15)
        width = self.initial_data.get('width', 15)
        
        if len(value) != height:
            raise serializers.ValidationError(f"Grid must have {height} rows.")
        
        for row in value:
            if not isinstance(row, list) or len(row) != width:
                raise serializers.ValidationError(f"Each row must have {width} columns.")
        
        return value
    
    def validate_words_data(self, value):
        """Validate words data structure."""
        if not isinstance(value, list):
            raise serializers.ValidationError("Words data must be a list.")
        
        for word_data in value:
            required_fields = ['word', 'start_row', 'start_col', 'direction']
            if not all(field in word_data for field in required_fields):
                raise serializers.ValidationError(
                    f"Each word must have: {', '.join(required_fields)}"
                )
        
        return value


class WordSearchAttemptSerializer(serializers.ModelSerializer):
    """Serializer for WordSearchAttempt model."""
    
    user = UserSerializer(read_only=True)
    puzzle = WordSearchPuzzleSerializer(read_only=True)
    puzzle_id = serializers.IntegerField(write_only=True)
    completion_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = WordSearchAttempt
        fields = [
            'id', 'puzzle', 'puzzle_id', 'user', 'started_at', 'completed_at',
            'words_found', 'time_taken', 'is_completed', 'completion_percentage'
        ]
        read_only_fields = ['started_at']


class PuzzleRatingSerializer(serializers.ModelSerializer):
    """Serializer for PuzzleRating model."""
    
    user = UserSerializer(read_only=True)
    puzzle_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = PuzzleRating
        fields = [
            'id', 'puzzle', 'puzzle_id', 'user', 'rating', 'comment', 'created_at'
        ]
        read_only_fields = ['created_at']


class PuzzleDetailSerializer(WordSearchPuzzleSerializer):
    """Extended serializer for puzzle detail view with additional data."""
    
    attempts_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()
    
    class Meta(WordSearchPuzzleSerializer.Meta):
        fields = WordSearchPuzzleSerializer.Meta.fields + [
            'attempts_count', 'average_rating', 'user_rating'
        ]
    
    def get_attempts_count(self, obj):
        return obj.attempts.count()
    
    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if not ratings:
            return None
        return round(sum(r.rating for r in ratings) / len(ratings), 2)
    
    def get_user_rating(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                rating = obj.ratings.get(user=request.user)
                return rating.rating
            except PuzzleRating.DoesNotExist:
                pass
        return None
