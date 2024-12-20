import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pendulum Simulator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Pendulum properties
class Pendulum:
    def __init__(self, origin, length, angle, mass=1, gravity=9.8, friction=0.001):
        self.origin = origin
        self.length = length
        self.angle = angle
        self.mass = mass
        self.gravity = gravity
        self.friction = friction
        self.omega = 0

    def calculate_alpha(self):
        return (-self.gravity / (self.length / 100)) * math.sin(self.angle) - self.friction * self.omega

    def update_position(self, dt):
        alpha = self.calculate_alpha()
        self.omega += alpha * dt
        self.angle += self.omega * dt
        self.omega *= (1 - self.friction)

    def get_position(self):
        x = self.origin[0] + self.length * math.sin(self.angle)
        y = self.origin[1] + self.length * math.cos(self.angle)
        return int(x), int(y)

# Slider properties
class Slider:
    def __init__(self, x, y, width, value, max_value, step=1):
        self.rect = pygame.Rect(x, y, width, 10)
        self.handle = pygame.Rect(x + int(value / max_value * width), y - 5, 10, 20)
        self.value = value
        self.max_value = max_value
        self.step = step
        self.dragging = False

    def draw(self, label, font):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.handle)
        label_surface = font.render(label, True, BLACK)
        screen.blit(label_surface, (self.rect.x, self.rect.y - 25))

    def update_value(self, mouse_x):
        self.handle.x = max(self.rect.x, min(mouse_x, self.rect.x + self.rect.width))
        self.value = ((self.handle.x - self.rect.x) / self.rect.width) * self.max_value

# Main loop
def main():
    origin = (WIDTH // 2, 100)
    pendulum = Pendulum(origin, 250, math.pi / 4)
    sliders = {
        "gravity": Slider(50, HEIGHT - 190, 300, pendulum.gravity, 50),
        "friction": Slider(50, HEIGHT - 130, 300, pendulum.friction * 100, 100),
        "length": Slider(50, HEIGHT - 70, 300, pendulum.length, 400),
        "mass": Slider(50, HEIGHT - 20, 300, pendulum.mass, 10)
    }

    FPS = 60
    dt = 1 / FPS
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 24)

    running = True
    is_dragging = False

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                bob_x, bob_y = pendulum.get_position()
                distance = math.sqrt((mouse_x - bob_x) ** 2 + (mouse_y - bob_y) ** 2)
                if distance <= 20:
                    is_dragging = True
                for slider in sliders.values():
                    if slider.handle.collidepoint(mouse_x, mouse_y):
                        slider.dragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                is_dragging = False
                for slider in sliders.values():
                    slider.dragging = False

        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if is_dragging:
                dx = mouse_x - pendulum.origin[0]
                dy = mouse_y - pendulum.origin[1]
                pendulum.angle = math.atan2(dx, dy)
                pendulum.omega = 0
            else:
                for name, slider in sliders.items():
                    if slider.dragging:
                        slider.update_value(mouse_x)
                        if name == "gravity":
                            pendulum.gravity = slider.value
                        elif name == "friction":
                            pendulum.friction = slider.value / 100
                        elif name == "length":
                            pendulum.length = slider.value
                        elif name == "mass":
                            pendulum.mass = slider.value

        if not is_dragging:
            pendulum.update_position(dt)

        # Draw the y-line (vertical reference line)
        pygame.draw.line(screen, BLACK, pendulum.origin, (pendulum.origin[0], HEIGHT), 1)

        # Draw the x-line (horizontal reference line at the top of the y-line)
        pygame.draw.line(screen, BLACK, (0, pendulum.origin[1]), (WIDTH, pendulum.origin[1]), 1)

        pygame.draw.line(screen, BLACK, pendulum.origin, pendulum.get_position(), 2)
        pygame.draw.circle(screen, RED, pendulum.get_position(), 20)

        for name, slider in sliders.items():
            slider.draw(f"{name.capitalize()}: {slider.value:.2f}", font)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
