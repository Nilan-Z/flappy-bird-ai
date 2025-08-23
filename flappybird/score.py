import pygame

class Score:
    def __init__(self):
        #Load sprites form 0 to 9
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
