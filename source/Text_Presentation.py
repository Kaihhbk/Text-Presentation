import pygame
import sys
import csv

def setup_window(width, height, fullscreen=True):
    flags = pygame.FULLSCREEN if fullscreen else 0
    return pygame.display.set_mode((width, height), flags)

def render_text(text_str, font, width, height):
    text = font.render(text_str, True, (255, 255, 255), (0, 0, 0))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    return text, text_rect

def animate_text(text, text_rect, screen, speed, clock, start_wait):
    x_position = screen.get_width()
    running = True

    while running:
        dt = clock.tick(60) / 1000.0  # Delta Time in Sekunden
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill((0, 0, 0))

        if pygame.time.get_ticks() < start_wait:
            pygame.display.update()
            continue

        x_position -= speed * dt
        rounded_x_position = round(x_position)
        screen.blit(text, (rounded_x_position, text_rect.y))

        pygame.display.update()

        if x_position + text_rect.width <= 0:
            running = False

def read_text_from_csv(file_path, delimiter=';'):
    texts = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        for row in reader:
            if row:
                texts.append(row[0])
    return texts

def main():
    fps = 60
    width, height = 1280, 720
    speed = 250  # Geschwindigkeit in Pixel pro Sekunde
    csv_file_path = "text_data.csv"
    start_wait = 4000
    font_size = 80

    screen = setup_window(width, height)
    clock = pygame.time.Clock()
    clock.tick(fps)

    texts = read_text_from_csv(csv_file_path, delimiter=';')

    pygame.init()
    font = pygame.font.Font(None, font_size)

    # Schriftart-Caching (außerhalb der Animationsschleife)
    cached_text = {text: render_text(text, font, width, height) for text in texts}

    for text_str in texts:
        text, text_rect = cached_text[text_str]
        animate_text(text, text_rect, screen, speed, clock, start_wait)

if __name__ == "__main__":
    main()
