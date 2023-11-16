import pygame
import sys
import csv

def setup_window(width, height, fullscreen=False):
    flags = pygame.FULLSCREEN if fullscreen else 0
    return pygame.display.set_mode((width, height), flags)

def render_text(text_str, font, width, height):
    text = font.render(text_str, True, (255, 255, 255), (0, 0, 0))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    return text, text_rect

def animate_text(text, text_rect, screen, speed, dt):
    x_position = screen.get_width()
    running = True
    fullscreen = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    fullscreen = not fullscreen
                    screen = setup_window(screen.get_width(), screen.get_height(), fullscreen)

        # Führe die Animation durch
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
    fps = 120
    width, height = 1280, 720
    speed = 17  # Geschwindigkeit in Pixel pro Sekunde
    font_size = 80
    csv_file_path = "text_data.csv"
    start_wait = 3000  # Sec.
    stop_wait = 2000   # Sec.

    fullscreen = True
    screen = setup_window(width, height, fullscreen)

    texts = read_text_from_csv(csv_file_path)

    clock = pygame.time.Clock()
    dt = clock.tick(fps) / 1000.0  # Delta Time in Sekunden

    pygame.init()

    font = pygame.font.Font(None, font_size)

    # Schriftart-Caching
    cached_text = {text: render_text(text, font, width, height) for text in texts}

    # Fülle den Bildschirm mit Schwarz
    screen.fill((0, 0, 0))
    pygame.time.wait(start_wait)

    for text_str in texts:
        text, text_rect = cached_text[text_str]
        animate_text(text, text_rect, screen, speed, dt)

    pygame.time.wait(stop_wait)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
