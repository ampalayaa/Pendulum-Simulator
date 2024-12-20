import pygame
import math

class PendulumSimulator:
    def __init__(self):
        pygame.init()

        # Screen settings
        self.WIDTH, self.HEIGHT = 1000, 700
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pendulum Simulator")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GRAY = (200, 200, 200)

        # Pendulum settings
        self.origin = (self.WIDTH // 2, 100)
        self.length = 250
        self.radius = 20
        self.mass = 1
        self.gravity = 9.8
        self.friction = 0.001
        self.angle = math.pi / 4
        self.omega = 0

        # Time settings
        self.FPS = 60
        self.dt = 1 / self.FPS
        self.clock = pygame.time.Clock()

        # Dragging state
        self.is_dragging = False

        # Slider settings
        self.sliders = {
            "gravity": self.create_slider(50, self.HEIGHT - 190, 300, 10, self.gravity / 50),
            "friction": self.create_slider(50, self.HEIGHT - 130, 300, 10, self.friction * 100),
            "length": self.create_slider(50, self.HEIGHT - 70, 300, 10, self.length / 400),
            "mass": self.create_slider(50, self.HEIGHT - 20, 300, 10, self.mass / 10),
        }

        self.running = True

    def create_slider(self, x, y, width, height, ratio):
        handle_x = x + int(ratio * width)
        return {
            "track": pygame.Rect(x, y, width, height),
            "handle": pygame.Rect(handle_x, y - 5, 10, 20),
        }

    def calculate_alpha(self):
        return (-self.gravity / self.length) * math.sin(self.angle) - self.friction * self.omega

    def get_pendulum_position(self):
        x = self.origin[0] + self.length * math.sin(self.angle)
        y = self.origin[1] + self.length * math.cos(self.angle)
        return int(x), int(y)

    def handle_dragging(self):
        if self.is_dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - self.origin[0]
            dy = mouse_y - self.origin[1]
            self.angle = math.atan2(dx, dy)
            self.omega = 0
        else:
            alpha = self.calculate_alpha()
            self.omega += alpha * self.dt
            self.angle += self.omega * self.dt
            self.omega *= (1 - self.friction)

    def draw_pendulum(self):
        position = self.get_pendulum_position()
        pygame.draw.line(self.screen, self.BLACK, self.origin, position, 2)
        pygame.draw.circle(self.screen, self.RED, position, self.radius)

    def draw_sliders(self):
        font = pygame.font.SysFont(None, 24)

        for name, slider in self.sliders.items():
            pygame.draw.rect(self.screen, self.GRAY, slider["track"])
            pygame.draw.rect(self.screen, self.BLACK, slider["handle"])
            value = self.get_slider_value(name)
            label = font.render(f"{name.capitalize()}: {value:.2f}", True, self.BLACK)
            self.screen.blit(label, (slider["track"].x, slider["track"].y - 30))

    def get_slider_value(self, name):
        handle = self.sliders[name]["handle"]
        track = self.sliders[name]["track"]
        ratio = (handle.x - track.x) / track.width

        if name == "gravity":
            self.gravity = ratio * 50
        elif name == "friction":
            self.friction = ratio / 100
        elif name == "length":
            self.length = ratio * 400
        elif name == "mass":
            self.mass = ratio * 10

        return {
            "gravity": self.gravity,
            "friction": self.friction,
            "length": self.length,
            "mass": self.mass,
        }[name]

    def update_sliders(self):
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for name, slider in self.sliders.items():
                if slider["handle"].collidepoint(mouse_x, mouse_y):
                    slider["handle"].x = max(slider["track"].x, min(mouse_x, slider["track"].x + slider["track"].width))

    def run(self):
        while self.running:
            self.screen.fill(self.WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    bob_x, bob_y = self.get_pendulum_position()
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    distance = math.sqrt((mouse_x - bob_x) ** 2 + (mouse_y - bob_y) ** 2)
                    if distance <= self.radius:
                        self.is_dragging = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.is_dragging = False

            self.update_sliders()
            self.handle_dragging()
            self.draw_pendulum()
            self.draw_sliders()

            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()

if __name__ == "__main__":
    PendulumSimulator().run()
