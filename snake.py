import pygame


scr_size = (800, 600)
snake_pos = (400, 200)
snake_size = (50, 50)
snake_color = (255, 165, 0)
# Keys
key_up = "k_W"
key_down = "k_S"
key_left = "k_A"
key_right = "k_D"


def main():
    scr = pygame.display.set_mode(scr_size)
    clock = pygame.time.Clock()
    snake = pygame.rect.Rect(snake_pos, snake_size)

    pressed_key = 
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
            elif event.type == pygame.KEYDOWN:
                event.key = pygame.key.name(event.key)
                pressed_key = event.key
            elif event.type == pygame.KEYUP:
                pressed_key = None

        if pressed_key == key_up:
            if snake.bottom < scr.get_height():
                snake.bottom -= snake.h
            else:
                snake.bottom = snake.bottom - scr.get_height()
        elif pressed_key == key_down:
            

        scr.fill((0, 0, 0))
        pygame.draw.rect(scr, snake_color, snake)

        pygame.display.flip()
        pygame.display.update()

        clock.tick(3)


if __name__ == "__main__":
    main()
