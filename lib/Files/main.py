import pygame, pathlib, random, pickle, threading

path = pathlib.Path(__file__).resolve().parent.parent
font = str(path) + "/Font/font.ttf"

# Try to load the config.dat:
# If an exception occures, use the default settings
# And if this ^ happens, the file is propably missing or corrupted
try:
    config = pickle.load(open(str(path) + "/Files/config.dat", "rb"))
except:
    config = [
        {   # Settings
            "draw_background": True,
            "show_crosshair": False,
            "bird_show_hitbox": False,
            "bird_show": True,
        },
        
        [0]  # Best Score
    ]

WIDTH = 570
DISPLAY_HEIGHT = 400
HEIGHT = 500

SCORE = 0
GAMEOVER = False
DIFFICULTY = None

difficulties = {
    "Easy" : 50,
    "Medium" : 25,
    "Hard" : 10,
}
cursor = 0

pygame.init()

white = pygame.Color(255, 255, 255)
blue = pygame.Color(0, 200, 255)
yellow = pygame.Color(255, 255, 0)
black = pygame.Color(0, 0, 0)
green = pygame.Color(100, 255, 100)

clock = pygame.time.Clock()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Birds")

bird_width = 66
bird_height = 46
crosshair_size = 25

# ===
bird_img1 = pygame.image.load(str(path) + "/Bird/bird1.png")
bird_img2 = pygame.image.load(str(path) + "/Bird/bird2.png")
bird_img3 = pygame.image.load(str(path) + "/Bird/bird3.png")
bird_img4 = pygame.image.load(str(path) + "/Bird/bird4.png")

bird_img1 = pygame.transform.scale(bird_img1, (bird_width, bird_height))
bird_img2 = pygame.transform.scale(bird_img2, (bird_width, bird_height))
bird_img3 = pygame.transform.scale(bird_img3, (bird_width, bird_height))
bird_img4 = pygame.transform.scale(bird_img4, (bird_width, bird_height))

cloud_img = pygame.image.load(str(path) + "/Background/clouds.png")
grass = pygame.image.load(str(path) + "/Background/grass.png")
crosshair = pygame.image.load(str(path) + "/Miscellaneous/crosshair.png")
scoreboard = pygame.image.load(str(path) + "/Miscellaneous/scoreboard.png")

# ===
birds = []
bird_images = [bird_img1, bird_img2, bird_img3, bird_img4, bird_img3, bird_img2]


class Bird:
    def __init__(self):
        self.speed = random.uniform(0.4, 1.5)
        self.x = random.randint(WIDTH, WIDTH*2)
        self.y = random.randint(0, DISPLAY_HEIGHT-bird_height)
        self.image = 0

    def show(self):        
        bird_img = bird_images[(int(self.image / 5) * 5) % len(bird_images)]
        
        bird_rect = bird_img.get_rect()
        bird_rect = bird_rect.move((self.x, self.y))
        
        if config[0]["bird_show"]:
            display.blit(bird_img, bird_rect)
        
        self.image += 1
    
    def show_hitbox(self):
        if config[0]["bird_show_hitbox"]:
            pygame.draw.rect(display, yellow, (self.x, self.y, bird_width, bird_height), width=1)
    
    def move(self):
        self.x -= self.speed
    
    def new(self):
        self.x = WIDTH
        self.y = random.randint(0, DISPLAY_HEIGHT-bird_height)
        self.speed = random.uniform(0.5, 1.5)
    
    def update(self, *argv):
        if self.x <= 0-bird_width:     
            self.new()
        
        if len(argv) == 2:
            if isinstance(argv[0], int) and isinstance(argv[1], int):
                if argv[0] > self.x and argv[0] < self.x+bird_width and argv[1] > self.y and argv[1] < self.y+bird_height:
                    global SCORE
                    SCORE += self.x/10
                    self.new()


def draw_scoreboard():
    global cursor
    pygame.draw.rect(display, white, (0, DISPLAY_HEIGHT, WIDTH, HEIGHT))
    display.blit(scoreboard, (0, DISPLAY_HEIGHT))
    
    score_font = pygame.font.Font(font, 20)
    score_text = score_font.render(f"Score: {SCORE:.1f}", black, True)
    score_text_height = score_text.get_rect().height
    
    best_score_text = score_font.render(f"Best Score: {config[1][0]:.1f}", black, True)
    best_score_text_height = best_score_text.get_rect().height
    
    difficulty_text = score_font.render(f"Difficulty: {list(difficulties.keys())[cursor % len(list(difficulties.keys()))]}", black, True)
    difficulty_text_height = difficulty_text.get_rect().height
    
    display.blit(score_text, (20, DISPLAY_HEIGHT+score_text_height*0.5))
    display.blit(best_score_text, (20, DISPLAY_HEIGHT+best_score_text_height*1.5))
    display.blit(difficulty_text, (20, DISPLAY_HEIGHT+difficulty_text_height*2.5))
        
def show_settings():
    settings_font = pygame.font.Font(font, 15)
    keys = list(config[0])

    for setting in range(len(config[0])):
        settings_text = settings_font.render(f"{keys[setting]}: {config[0][keys[setting]]}", black, True)
        settings_text_height = settings_text.get_rect().height
        
        display.blit(settings_text, (WIDTH/2, DISPLAY_HEIGHT+settings_text_height/2 + (20*setting)))
    
def draw_background():
    if config[0]["draw_background"]:
        display.blit(cloud_img, (0, 0))
        display.blit(grass, (0, DISPLAY_HEIGHT-grass.get_height()))

def show_crosshair():
    if config[0]["show_crosshair"]:
        global crosshair
        pygame.mouse.set_visible(False)
        
        x = pygame.mouse.get_pos()[0] - crosshair_size/2
        y = pygame.mouse.get_pos()[1] - crosshair_size/2
        
        crosshair = pygame.transform.scale(crosshair, (crosshair_size, crosshair_size))
        crosshair_rect = crosshair.get_rect()
        crosshair_rect = crosshair_rect.move((x, y))
        display.blit(crosshair, crosshair_rect)
    else:
        pygame.mouse.set_visible(True)
        

def spawn_birds():
    while not GAMEOVER:
        for _ in range(difficulties[DIFFICULTY]):     # Spawning rate: 5 seconds
            pygame.time.wait(100)
            if GAMEOVER:
                return

        bird = Bird()
        birds.append(bird)


for _ in range(5):
    bird = Bird()
    birds.append(bird)
    
    
def menu():
    header_font = pygame.font.Font(font, 60)
    header = header_font.render("Select Difficulty", True, black)
    header_rect = header.get_rect()
    header_rect.midtop = (int(WIDTH/2), int(DISPLAY_HEIGHT/5))

    dif_font = pygame.font.Font(font, 25)
    for dif in difficulties:
        if cursor % len(difficulties) == list(difficulties.keys()).index(dif):
            dif_option = dif_font.render(dif, True, white)
        else: dif_option = dif_font.render(dif, True, black)

        dif_option_rect = dif_option.get_rect()
        dif_option_rect.center = (int(WIDTH/2), int(DISPLAY_HEIGHT/2) + list(difficulties.keys()).index(dif)*40)
        display.blit(dif_option, dif_option_rect)

    display.blit(header, header_rect)

def game():    
    global GAMEOVER
    global DIFFICULTY
    while not GAMEOVER:
        display.fill(blue)
        
        draw_scoreboard()
        draw_background()

        if DIFFICULTY == None:
            menu()
        else:
            # if threading.Thread(target = spawn_birds).start().is_alive():
            #     print("moi")            
            for bird in birds:
                bird.move()
                bird.show()
                bird.update()
                bird.show_hitbox()

            show_settings()
            show_crosshair()
            
            # Save current progress
            if SCORE > config[1][0]:
                config[1][0] = SCORE
            pickle.dump(config, open(str(path) + "/Files/config.dat", "wb"))
            
        # ===
        for event in pygame.event.get():            
            if event.type == pygame.QUIT:
                GAMEOVER = True
                pygame.quit()
                exit()
            
            keys = list(config[0])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    config[0][keys[0]] = not config[0][keys[0]]
                    
                if event.key == pygame.K_2:
                    config[0][keys[1]] = not config[0][keys[1]]
                
                if event.key == pygame.K_3:
                    config[0][keys[2]] = not config[0][keys[2]]
                
                if event.key == pygame.K_4:
                    config[0][keys[3]] = not config[0][keys[3]]
                
                if DIFFICULTY == None:
                    global cursor
                    if event.key == pygame.K_UP:
                        cursor -= 1
                    if event.key == pygame.K_DOWN:
                        cursor += 1
                    if event.key == pygame.K_RETURN:
                        for dif in difficulties:
                            if cursor%len(difficulties) == list(difficulties.keys()).index(dif):
                                DIFFICULTY = difficulties[dif]
            
            if event.type == pygame.MOUSEBUTTONUP:
                for bird in birds:
                    bird.update(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        
        # ===
        pygame.display.update()
        clock.tick(60)
