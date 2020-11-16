import pygame, random

WIDTH = 600
HEIGHT = 400

pygame.init()

white = pygame.Color(255, 255, 255)
blue = pygame.Color(0, 200, 255)
yellow = pygame.Color(255, 255, 0)
green = pygame.Color(0, 255, 0)

clock = pygame.time.Clock()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("*** Game ***")

birds = []


class Bird:
    def __init__(self):
        self.radius = 30
        self.speed = random.uniform(0.4, 1.5)
        self.x = random.randint(WIDTH, WIDTH*2)
        self.y = random.randint(0, HEIGHT-self.radius)

    def show(self):
        pygame.draw.ellipse(display, yellow, (self.x, self.y, self.radius, self.radius))
    
    def move(self):
        self.x -= self.speed
    
    def new(self):
        self.x = WIDTH
        self.y = random.randint(0, HEIGHT-self.radius)
        self.speed = random.uniform(0.5, 1.5)
    
    def update(self, *argv):
        if self.x <= 0-self.radius:     
            self.new()
        
        if len(argv) == 2:
            if isinstance(argv[0], int) and isinstance(argv[1], int):
                if argv[0] > self.x and argv[0] < self.x+self.radius and argv[1] > self.y and argv[1] < self.y+self.radius:
                    self.new()



for _ in range(5):
    bird = Bird()
    birds.append(bird)

while True:
    display.fill(blue)
    
    for bird in birds:
        bird.move()
        bird.show()
        bird.update()
    
    # ===
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.MOUSEBUTTONUP:
            for bird in birds:
                bird.update(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    
    # ===
    pygame.display.update()
    clock.tick(60)