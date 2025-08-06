import pygame

class Score:
    def __init__(self):
        self.digits = []
        for i in range(10):
            sprite = pygame.image.load(f"assets/sprites/{i}.png").convert_alpha()
            width = sprite.get_width()
            height = sprite.get_height()
            scaled_sprite = pygame.transform.scale(sprite, (int(width * 0.8), int(height * 0.8)))
            self.digits.append(scaled_sprite)

    def draw(self, surface, score, x, y):
        score_str = str(score)
        
        total_width = sum(self.digits[int(d)].get_width() for d in score_str)
        start_x = x - total_width // 2
        
        for char in score_str:
            digit = int(char)
            digit_img = self.digits[digit]
            surface.blit(digit_img, (start_x, y))
            start_x += digit_img.get_width()
