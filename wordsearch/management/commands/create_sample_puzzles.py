from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from wordsearch.models import WordSearchPuzzle
import random
import string

class Command(BaseCommand):
    help = 'Create sample word search puzzles'

    def handle(self, *args, **options):
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}
        )
        
        if created:
            admin_user.set_password('admin123')
            admin_user.save()

        # Sample puzzle data
        puzzles_data = [
            {
                'title': 'Animals',
                'description': 'Find all the animals hidden in this puzzle!',
                'difficulty': 'easy',
                'width': 10,
                'height': 10,
                'words': ['CAT', 'DOG', 'BIRD', 'FISH', 'HORSE']
            },
            {
                'title': 'Colors',
                'description': 'Discover the rainbow of colors in this word search.',
                'difficulty': 'medium',
                'width': 12,
                'height': 12,
                'words': ['RED', 'BLUE', 'GREEN', 'YELLOW', 'PURPLE', 'ORANGE']
            },
            {
                'title': 'Programming Languages',
                'description': 'For the tech-savvy! Find popular programming languages.',
                'difficulty': 'hard',
                'width': 15,
                'height': 15,
                'words': ['PYTHON', 'JAVASCRIPT', 'JAVA', 'CSHARP', 'RUBY', 'GO', 'RUST']
            },
            {
                'title': 'Countries',
                'description': 'Travel the world by finding these country names.',
                'difficulty': 'medium',
                'width': 12,
                'height': 12,
                'words': ['USA', 'CANADA', 'FRANCE', 'GERMANY', 'JAPAN', 'BRAZIL']
            },
            {
                'title': 'Space Adventure',
                'description': 'Explore the cosmos with space-related words.',
                'difficulty': 'extreme',
                'width': 20,
                'height': 20,
                'words': ['GALAXY', 'PLANET', 'ASTEROID', 'NEBULA', 'SUPERNOVA', 'BLACKHOLE', 'UNIVERSE']
            }
        ]

        for puzzle_data in puzzles_data:
            # Check if puzzle already exists
            if not WordSearchPuzzle.objects.filter(title=puzzle_data['title']).exists():
                # Create simple grid (for demo purposes)
                grid = self.create_simple_grid(puzzle_data['width'], puzzle_data['height'], puzzle_data['words'])
                words_data = self.create_words_data(puzzle_data['words'])
                
                puzzle = WordSearchPuzzle.objects.create(
                    title=puzzle_data['title'],
                    description=puzzle_data['description'],
                    difficulty=puzzle_data['difficulty'],
                    width=puzzle_data['width'],
                    height=puzzle_data['height'],
                    grid_data=grid,
                    words_data=words_data,
                    created_by=admin_user,
                    is_public=True
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created puzzle: {puzzle.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Puzzle "{puzzle_data["title"]}" already exists')
                )

    def create_simple_grid(self, width, height, words):
        """Create a simple grid filled with random letters"""
        grid = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append(random.choice(string.ascii_uppercase))
            grid.append(row)
        
        # Place first word horizontally in the middle for demo
        if words and len(words[0]) <= width:
            word = words[0]
            start_col = (width - len(word)) // 2
            middle_row = height // 2
            for i, letter in enumerate(word):
                grid[middle_row][start_col + i] = letter
        
        return grid

    def create_words_data(self, words):
        """Create words data structure"""
        words_data = []
        for i, word in enumerate(words):
            words_data.append({
                'word': word,
                'start_row': 5,  # Simple placement for demo
                'start_col': 2 + i,
                'direction': 'horizontal',
                'found': False
            })
        return words_data
