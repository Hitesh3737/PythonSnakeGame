## Made By Hitesh Sajnani ##

import numpy as np
import pygame
import sys
import imageio

# Set up the screen
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Menu")

# Load background GIF
background_gif_path = "assets/backgroundgif.gif"
reader = imageio.get_reader(background_gif_path)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Font
def get_font(size):
    return pygame.font.Font(None, size)

# Text content
menu_text_content = "MAIN MENU"

# Border properties
border_thickness = 4
border_color = black

clock = pygame.time.Clock()

class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.text = font.render(text_input, True, "#d7fcd4")
        self.base_color = base_color
        self.hovering_color = hovering_color

    def change_color(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.image.fill(pygame.Color(self.hovering_color))
        else:
            self.image.fill(pygame.Color("#31021f"))

    def update(self, screen):
        screen.blit(self.image, self.rect.topleft)
        text_rect = self.text.get_rect(center=self.rect.center)
        screen.blit(self.text, text_rect.topleft)

    def check_for_input(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

def play_background_music():
    pygame.mixer.music.load('resources/bg_music_1.mp3')
    pygame.mixer.music.play(-1, 0)

def play_sound(sound_name):
    if sound_name == 'ding':
        sound = pygame.mixer.Sound("resources/ding.mp3")
        pygame.mixer.Sound.play(sound)

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def play():
    play_sound("ding")
    pygame.display.set_caption("Game")
    
    print("Creating an instance of the Main class...")
    from snake import Main
    game = Main()  # Create an instance of the Main class
    while game.in_game:
          game.run()

    print("Game finished. Creating play_again_button...")

    play_again_button = Button(image=None, pos=(640, 460),
                               text_input="PLAY AGAIN", font=get_font(75), base_color="black", hovering_color="green")

    play_again_button.change_color(pygame.mouse.get_pos())
    play_again_button.update(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.K_BACKSPACE:
            if play_again_button.check_for_input(pygame.mouse.get_pos()):
                # Reset the game state before returning to the menu
                game.reset_game()
                return
    pygame.display.update()

def ensure_valid_array(frame):
    # Ensure 3D structure (height, width, depth)
    if frame.ndim == 2:
        frame = np.expand_dims(frame, axis=2)
    elif frame.ndim == 1:
        # Handle 1D array (grayscale)
        frame = np.expand_dims(frame, axis=0)
        frame = np.expand_dims(frame, axis=0)
    return frame
pygame.display.update()

def options():
    play_sound("ding")
    pygame.display.set_caption("Options")
    
    print("Creating an instance of the Main class...")
    from options import main_menu2
    main_menu2()
    pygame.display.update()
    pygame.quit()
    sys.exit()
    
def main_menu():
    frame_index = 0

    while True:
        # Clear the screen
        screen.fill((255, 255, 255))
        
        try:
            # Blit the current frame onto the screen
            frame = reader.get_data(frame_index)
            frame = ensure_valid_array(frame)

            # Ensure the frame is a valid 3D array
            if frame.ndim == 3 and frame.shape[2] == 3:
                frame_surface = pygame.surfarray.make_surface(frame)

                # Get the original dimensions of the frame
                original_width, original_height, _ = frame.shape

                # Calculate the scaling factors to maintain the original aspect ratio
                aspect_ratio = original_width / original_height
                new_height = int(1400 / aspect_ratio)  # Calculate new height based on the desired width (720)
                frame_surface = pygame.transform.scale(frame_surface, (1280, new_height))

                screen.blit(frame_surface, (0, 0))
            else:
                print("Invalid frame format.")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Update the frame index
        frame_index = (frame_index + 1) % len(reader)

        menu_mouse_pos = pygame.mouse.get_pos()
        
        # Render the text with a border
        menu_text_surface = get_font(100).render(menu_text_content, True, border_color)
        menu_text_rect = menu_text_surface.get_rect(center=(width // 2 + border_thickness, 100 + border_thickness))
        screen.blit(menu_text_surface, menu_text_rect)

        # Render the actual text on top of the border
        menu_text_surface = get_font(100).render(menu_text_content, True, "#454B1B")
        menu_text_rect = menu_text_surface.get_rect(center=(width // 2, 100))
        screen.blit(menu_text_surface, menu_text_rect)
        
        play_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#606c38", hovering_color="#454B1B")
        options_button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#606c38", hovering_color="#454B1B")
        quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#606c38", hovering_color="#454B1B")

        for button in [play_button, options_button, quit_button]:
            button.change_color(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    play()
                if options_button.check_for_input(menu_mouse_pos):
                    options()
                if quit_button.check_for_input(menu_mouse_pos):
                    pygame.mixer.music.pause()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    
    play_background_music()
    main_menu()
    
## Made By Hitesh Sajnani ##