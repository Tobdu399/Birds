import pathlib, pygame, random

path = pathlib.Path(__file__).resolve().parent

WIDTH = 570
DISPLAY_HEIGHT = 400
HEIGHT = 500

SCORE = 0

pygame.init()

white = pygame.Color(255, 255, 255)
blue = pygame.Color(0, 200, 255)
yellow = pygame.Color(255, 255, 0)
green = pygame.Color(0, 255, 0)

clock = pygame.time.Clock()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("*** BIRDS ***")

birds = []

# ===
bird_img = pygame.image.load(str(path) + "/lib/bird.png")
bird_img = pygame.transform.scale(bird_img, (64, 48))

cloud_img = pygame.image.load(str(path) + "/lib/clouds.png")



class Bird:
    def __init__(self):
        self.width = 64
        self.height = 48
        self.speed = random.uniform(0.4, 1.5)
        self.x = random.randint(WIDTH, WIDTH*2)
        self.y = random.randint(0, DISPLAY_HEIGHT-self.height)

    def show(self):       
        bird_rect = bird_img.get_rect()
        bird_rect = bird_rect.move((self.x, self.y))
        display.blit(bird_img, bird_rect)
    
    def show_hitbox(self):
        pygame.draw.rect(display, yellow, (self.x, self.y, self.width, self.height), width=1)
    
    def move(self):
        self.x -= self.speed
    
    def new(self):
        self.x = WIDTH
        self.y = random.randint(0, DISPLAY_HEIGHT-self.height)
        self.speed = random.uniform(0.5, 1.5)
    
    def update(self, *argv):
        if self.x <= 0-self.width:     
            self.new()
        
        if len(argv) == 2:
            if isinstance(argv[0], int) and isinstance(argv[1], int):
                if argv[0] > self.x and argv[0] < self.x+self.width and argv[1] > self.y and argv[1] < self.y+self.height:
                    global SCORE
                    SCORE += 1
                    self.new()


def draw_scoreboard():
    pygame.draw.rect(display, white, (0, DISPLAY_HEIGHT, WIDTH, HEIGHT))



for _ in range(5):
    bird = Bird()
    birds.append(bird)

while True:
    display.fill(blue)
    display.blit(cloud_img, (0, 0))
    
    for bird in birds:
        bird.move()
        bird.show()
        bird.update()
        bird.show_hitbox()
        
    draw_scoreboard()
    
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