import pygame

class Score:
    """
    A class to handle rendering of numeric scores using digit sprites.

    This class loads digit images (0-9) from assets, scales them,
    and provides a method to draw a given score centered at a specified position.
    """

    def __init__(self):
        """
        Initialize the Score object by loading and scaling digit sprites.

        Each digit sprite (0-9) is loaded from the assets folder,
        then scaled down to 90% of its original size to maintain consistent display.
        The processed sprites are stored in a list for quick access during drawing.
        """
        self.digit_sprites = []
        for digit in range(10):
            sprite = pygame.image.load(f"assets/sprites/{digit}.png").convert_alpha()
            width = sprite.get_width()
            height = sprite.get_height()
            scaled_sprite = pygame.transform.scale(sprite, (int(width * 0.9), int(height * 0.9)))
            self.digit_sprites.append(scaled_sprite)

    def draw(self, surface, score, center_x, y):
        """
        Draw the given numeric score on the specified surface.

        The score is centered horizontally around the `center_x` coordinate,
        and drawn at the vertical position `y`.

        Args:
            surface (pygame.Surface): The target surface to draw the score on.
            score (int): The numeric score to display.
            center_x (int): The x-coordinate to center the score horizontally.
            y (int): The y-coordinate at which to draw the score vertically.
        """
        score_str = str(score)
        total_width = sum(self.digit_sprites[int(d)].get_width() for d in score_str)
        x = center_x - total_width // 2

        for char in score_str:
            digit = int(char)
            digit_sprite = self.digit_sprites[digit]
            surface.blit(digit_sprite, (x, y))
            x += digit_sprite.get_width()
