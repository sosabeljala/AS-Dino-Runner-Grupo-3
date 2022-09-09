import pygame

from dino_runner.components.dinosaur import Dinosaur

from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

from dino_runner.utils.constants import BG, CLOUD, DEFAULT_TYPE, DINO_DEAD, FONT_STYLE, FUNDACION_DEL_SABER_ICON, GAME_OVER, ICON, ICON_START, JALA_ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager() 

        self.running = False 
        self.score = 0
        self.death_count = 0

    def execute(self):
        self.running = True 
        while self.running: 
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.player.power_up_time_up = -1
        self.score = 0
        self.game_speed = 20
        self.power_up_manager.reset_power_ups() 
        self.player.dino_rect.y = self.player.Y_POS  
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False 

    def update(self):
        self.update_score()
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.score, self.game_speed, self.player) 


    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 5

    def draw(self):
        if self.score // 400 == 0:
            game_color = (255, 215, 0)
        else:
            game_color = (255, 0, 0)

        self.clock.tick(FPS)
        self.screen.fill(game_color)
        self.draw_background()
        self.draw_score()
        self.draw_power_up_time()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen) 
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        self.abstractions_for_the_texts(f"Score: {self.score}", 1000, 50)


    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time_up - pygame.time.get_ticks()) / 1000, 2) 
            if time_to_show >= 0:
                self.abstractions_for_the_texts(f"{self.player.type.capitalize()} enable for {time_to_show} seconds.", 500, 40, 18)
            else: 
                self.player.has_power_up = False 
                self.player.type = DEFAULT_TYPE

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()
    
    def show_menu(self):
        
        self.screen.fill((139, 0, 0))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:  
            self.screen.blit(CLOUD, (half_screen_width -150, half_screen_height - 135))
            self.screen.blit(CLOUD, (half_screen_width +60, half_screen_height - 150))
            self.screen.blit(ICON_START, (half_screen_width - 50, half_screen_height - 140))
            self.screen.blit(FUNDACION_DEL_SABER_ICON, (half_screen_width - 100, 35))
            self.screen.blit(JALA_ICON, (half_screen_width - 195, 400))
            self.abstractions_for_the_texts("Press any key to play", 550, 300)
            self.abstractions_for_the_texts("Good luck", 550, 350)
        else: 
            self.screen.blit(DINO_DEAD, (half_screen_width - 30, 50))
            self.screen.blit(GAME_OVER, (half_screen_width - 180, half_screen_height - 100))
            self.abstractions_for_the_texts(f"Your score was: {self.score}", 550, 300)
            self.abstractions_for_the_texts(f"Number of deaths: {self.death_count}", half_screen_width, half_screen_height + 50)
            self.abstractions_for_the_texts("Press any key to restart", 550, 475)
        

        pygame.display.update()
        self.handle_events_on_menu()

    def abstractions_for_the_texts(self, texts, pos_x, pos_y, font_size = 30):
        font = pygame.font.Font(FONT_STYLE, font_size)
        text = font.render(texts, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (pos_x, pos_y)
        self.screen.blit(text, text_rect)