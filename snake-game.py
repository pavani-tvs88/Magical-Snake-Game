import pygame
import random
import sys
import time
import os

# Screen Dimensions
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 32  # Increased grid size to accommodate images better
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Initialize Pygame and set up display
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Magic Snake Adventure')

# Clock to control game speed
clock = pygame.time.Clock()

# Colors and Backgrounds
CREATURE_COLORS = {
    'Snake': {
        'head': (85, 255, 170),    # Bright green
        'body': (45, 175, 100),    # Darker green
        'background': (40, 42, 54), # Dark forest
        'food': {
            'apple': (255, 95, 95),    # Red apple
            'mouse': (150, 150, 150),  # Grey mouse
            'insect': (165, 42, 42)    # Brown insect
        }
    },
    'Dragon': {
        'head': (255, 140, 0),     # Orange
        'body': (200, 80, 0),      # Dark orange
        'background': (70, 40, 40), # Dark volcanic
        'food': {
            'sheep': (255, 255, 255),  # White sheep
            'deer': (139, 69, 19),     # Brown deer
            'fish': (70, 130, 180)     # Steel blue fish
        }
    },
    'Butterfly': {
        'head': (255, 192, 203),   # Pink
        'body': (219, 112, 147),   # Dark pink
        'background': (135, 206, 235), # Sky blue
        'food': {
            'flower': (255, 182, 193),  # Light pink flower
            'nectar': (255, 215, 0),    # Golden nectar
            'pollen': (255, 255, 0)     # Yellow pollen
        }
    },
    'Dolphin': {
        'head': (0, 191, 255),     # Deep sky blue
        'body': (30, 144, 255),    # Dodger blue
        'background': (0, 105, 148),# Deep ocean
        'food': {
            'fish': (70, 130, 180),    # Steel blue fish
            'squid': (238, 130, 238),  # Violet squid
            'shrimp': (255, 182, 193)  # Pink shrimp
        }
    },
    'Whale': {
        'head': (65, 105, 225),    # Royal blue
        'body': (25, 25, 112),     # Midnight blue
        'background': (0, 51, 102), # Deep sea
        'food': {
            'krill': (255, 160, 122),  # Light salmon
            'plankton': (176, 224, 230),# Powder blue
            'fish': (70, 130, 180)     # Steel blue fish
        }
    }
}

TEXT_COLOR = (248, 248, 242)      # Light text color
MENU_HIGHLIGHT = (85, 255, 170)    # Highlight color for menu

# Game configuration
FOOD_POINTS = {
    'apple': 1, 'mouse': 2, 'insect': 3,
    'sheep': 3, 'deer': 2, 'fish': 1,
    'flower': 1, 'nectar': 2, 'pollen': 3,
    'squid': 2, 'shrimp': 1,
    'krill': 1, 'plankton': 2
}

POWERUP_DURATION = 5  # Duration in seconds
INITIAL_MOVE_DELAY = 15  # Initial movement delay

# Asset loading function
def load_image(name):
    try:
        # Use absolute path to assets folder
        assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
        image_path = os.path.join(assets_dir, name)
        print(f"Loading image from: {image_path}")
        
        if not os.path.exists(image_path):
            print(f"Image file not found: {image_path}")
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Load the image with proper alpha channel support    
        image = pygame.image.load(image_path).convert_alpha()
        
        # Scale the image to fit the grid while preserving aspect ratio
        scaled_image = pygame.transform.smoothscale(image, (GRID_SIZE - 2, GRID_SIZE - 2))
        print(f"Successfully loaded and scaled image: {name}")
        return scaled_image
        
    except Exception as e:
        print(f"Error loading image {name}: {str(e)}")
        # Create a more visually distinct fallback image
        surface = pygame.Surface((GRID_SIZE - 2, GRID_SIZE - 2), pygame.SRCALPHA)
        if 'head' in name.lower():
            # Triangle for heads
            pygame.draw.polygon(surface, (255, 255, 255, 255), 
                              [(0, GRID_SIZE//2), (GRID_SIZE-2, 0), (GRID_SIZE-2, GRID_SIZE-2)])
        elif 'body' in name.lower():
            # Circle for body segments
            pygame.draw.circle(surface, (255, 255, 255, 255), 
                            (GRID_SIZE//2 - 1, GRID_SIZE//2 - 1), (GRID_SIZE-2)//2)
        else:
            # Square with X for food items
            pygame.draw.rect(surface, (255, 255, 255, 255), (0, 0, GRID_SIZE-2, GRID_SIZE-2))
            pygame.draw.line(surface, (0, 0, 0, 255), (0, 0), (GRID_SIZE-2, GRID_SIZE-2))
            pygame.draw.line(surface, (0, 0, 0, 255), (0, GRID_SIZE-2), (GRID_SIZE-2, 0))
        return surface

# Image dictionaries
CREATURE_IMAGES = {
    'Snake': {
        'head': load_image('snake_head.png'),
        'body': load_image('snake_body.png'),
        'food': {
            'apple': load_image('apple.png'),
            'mouse': load_image('mouse.png'),
            'insect': load_image('insect.png')
        }
    },
    'Dragon': {
        'head': load_image('dragon_head.png'),
        'body': load_image('dragon_body.png'),
        'food': {
            'sheep': load_image('sheep.png'),
            'deer': load_image('deer.png'),
            'fish': load_image('fish.png')
        }
    },
    'Butterfly': {
        'head': load_image('butterfly_head.png'),
        'body': load_image('butterfly_body.png'),
        'food': {
            'flower': load_image('flower.png'),
            'nectar': load_image('nectar.png'),
            'pollen': load_image('pollen.png')
        }
    },
    'Dolphin': {
        'head': load_image('dolphin_head.png'),
        'body': load_image('dolphin_body.png'),
        'food': {
            'fish': load_image('fish.png'),
            'squid': load_image('squid.png'),
            'shrimp': load_image('shrimp.png')
        }
    },
    'Whale': {
        'head': load_image('whale_head.png'),
        'body': load_image('whale_body.png'),
        'food': {
            'krill': load_image('krill.png'),
            'plankton': load_image('plankton.png'),
            'fish': load_image('fish.png')
        }
    }
}

# Load or create high score
try:
    with open('highscore.txt', 'r') as f:
        HIGH_SCORE = int(f.read())
except:
    HIGH_SCORE = 0

class CreatureSelection:
    def __init__(self):
        self.font = pygame.font.Font(None, 48)
        self.creatures = list(CREATURE_COLORS.keys())
        self.selected = 0
        self.selected_creature = self.creatures[0]

    def draw(self, surface):
        title = self.font.render("Select Your Creature", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        surface.blit(title, title_rect)

        for i, creature in enumerate(self.creatures):
            color = MENU_HIGHLIGHT if i == self.selected else TEXT_COLOR
            text = self.font.render(creature, True, color)
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
            surface.blit(text, rect)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.creatures)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.creatures)
            elif event.key == pygame.K_RETURN:
                self.selected_creature = self.creatures[self.selected]
                return self.selected_creature
        return None

class Creature:
    def __init__(self, creature_type):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow = False
        self.creature_type = creature_type
        self.colors = CREATURE_COLORS[creature_type]
        self.images = CREATURE_IMAGES[creature_type]
        self.rotation = 0  # For rotating the head image based on direction

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        new_head = (new_head[0] % GRID_WIDTH, new_head[1] % GRID_HEIGHT)
        
        # Update rotation based on direction
        if self.direction == (1, 0):
            self.rotation = 270
        elif self.direction == (-1, 0):
            self.rotation = 90
        elif self.direction == (0, 1):
            self.rotation = 180
        elif self.direction == (0, -1):
            self.rotation = 0
            
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def grow_creature(self):
        self.grow = True

    def check_collision(self):
        return len(self.body) != len(set(self.body))

    def draw(self, surface):
        for i, segment in enumerate(self.body):
            rect = pygame.Rect(
                segment[0] * GRID_SIZE + 1,
                segment[1] * GRID_SIZE + 1,
                GRID_SIZE - 2,
                GRID_SIZE - 2
            )
            if i == 0:  # Head
                # Rotate the head image based on direction
                rotated_head = pygame.transform.rotate(self.images['head'], self.rotation)
                surface.blit(rotated_head, rect)
            else:  # Body
                surface.blit(self.images['body'], rect)

class Food:
    def __init__(self, creature_body, creature_type):
        self.creature_type = creature_type
        self.foods = list(CREATURE_COLORS[creature_type]['food'].keys())
        self.current_food = random.choice(self.foods)
        self.position = self.generate_position(creature_body)
        self.colors = CREATURE_COLORS[creature_type]['food']
        self.images = CREATURE_IMAGES[creature_type]['food']

    def generate_position(self, creature_body):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in creature_body:
                return pos

    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE + 1,
            self.position[1] * GRID_SIZE + 1,
            GRID_SIZE - 2,
            GRID_SIZE - 2
        )
        surface.blit(self.images[self.current_food], rect)

class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, 64)
        self.options = ['Start Game', 'High Scores', 'Quit']
        self.selected = 0

    def draw(self, surface):
        for i, option in enumerate(self.options):
            color = MENU_HIGHLIGHT if i == self.selected else TEXT_COLOR
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 70))
            surface.blit(text, rect)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.selected
        return None

def show_high_scores(surface):
    running = True
    font = pygame.font.Font(None, 48)
    
    while running:
        surface.fill(CREATURE_COLORS['Snake']['background'])
        
        # Display high score
        score_text = font.render(f"High Score: {HIGH_SCORE}", True, TEXT_COLOR)
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        surface.blit(score_text, score_rect)
        
        # Display return instruction
        return_font = pygame.font.Font(None, 36)
        return_text = return_font.render("Press ESC to return to menu", True, TEXT_COLOR)
        return_rect = return_text.get_rect(center=(WIDTH // 2, HEIGHT * 3 // 4))
        surface.blit(return_text, return_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

def select_creature():
    creature_selection = CreatureSelection()
    running = True
    
    while running:
        screen.fill(CREATURE_COLORS['Snake']['background'])
        creature_selection.draw(screen)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            selected = creature_selection.handle_input(event)
            if selected:
                return selected

def game_loop(creature_type):
    creature = Creature(creature_type)
    food = Food(creature.body, creature_type)
    score = 0
    global HIGH_SCORE
    
    font = pygame.font.Font(None, 36)
    move_delay = INITIAL_MOVE_DELAY
    move_counter = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and creature.direction != (0, 1):
                    creature.direction = (0, -1)
                elif event.key == pygame.K_DOWN and creature.direction != (0, -1):
                    creature.direction = (0, 1)
                elif event.key == pygame.K_LEFT and creature.direction != (1, 0):
                    creature.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and creature.direction != (-1, 0):
                    creature.direction = (1, 0)
                elif event.key == pygame.K_ESCAPE:
                    return

        move_counter += 1
        if move_counter >= move_delay:
            creature.move()
            move_counter = 0

        if creature.body[0] == food.position:
            creature.grow_creature()
            food = Food(creature.body, creature_type)
            score += FOOD_POINTS.get(food.current_food, 1)

        if creature.check_collision():
            if score > HIGH_SCORE:
                HIGH_SCORE = score
                with open('highscore.txt', 'w') as f:
                    f.write(str(HIGH_SCORE))
            return

        screen.fill(CREATURE_COLORS[creature_type]['background'])
        creature.draw(screen)
        food.draw(screen)

        score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
        screen.blit(score_text, (10, 10))

        high_score_text = font.render(f"High Score: {HIGH_SCORE}", True, TEXT_COLOR)
        screen.blit(high_score_text, (10, 50))

        current_food_text = font.render(f"Food: {food.current_food.title()}", True, TEXT_COLOR)
        screen.blit(current_food_text, (10, 90))

        pygame.display.flip()
        clock.tick(102)

def main():
    menu = Menu()
    running = True
    
    while running:
        screen.fill(CREATURE_COLORS['Snake']['background'])
        menu.draw(screen)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            selection = menu.handle_input(event)
            if selection is not None:
                if selection == 0:  # Start Game
                    creature_type = select_creature()
                    game_loop(creature_type)
                elif selection == 1:  # High Scores
                    show_high_scores(screen)
                elif selection == 2:  # Quit
                    running = False
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
