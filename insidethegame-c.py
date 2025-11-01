import pygame
import random
import time
from moviepy import VideoFileClip

pygame.init()

screen_width = 1280
screen_height = 720
screen_size = (screen_width, screen_height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Matikka")

#Game state para maglipat ng screen
game_state = "menu"

#fonts
FONT = pygame.font.Font("fonts/Six Hands Web Marker.ttf", 55)
FONTXS = pygame.font.Font("fonts/Six Hands Web Marker.ttf", 39)
FONTS = pygame.font.Font("fonts/Six Hands Web Marker.ttf", 45)
FONTL = pygame.font.Font("fonts/Six Hands Web Marker.ttf", 80)
BIG_FONT = pygame.font.Font("fonts/Six Hands Web Marker.ttf", 150)

#extra fonts for credits and progress bar
CREDITS_FONT = pygame.font.Font("fonts/Six Hands Web Marker.ttf", 20)
PROGRESS_FONT = pygame.font.Font("fonts/Six Hands Web Marker.ttf", 32)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#sounds
tick_sound = pygame.mixer.Sound("sounds/ticking.WAV")
correct_sound = pygame.mixer.Sound("sounds/passcode.wav")
wrong_sound = pygame.mixer.Sound("sounds/minus3.wav")

tick_sound.set_volume(0.5)    
correct_sound.set_volume(0.5)
wrong_sound.set_volume(0.5)

correct_channel = pygame.mixer.Channel(1)
wrong_channel = pygame.mixer.Channel(2)

#menu assets
menu_bg_image = pygame.image.load("images/menu_bg.png")
menu_bg_image = menu_bg_image.convert()

no_title_bg = pygame.image.load("images/menu bg no title.png")
no_title_bg = no_title_bg.convert()

start_button = pygame.image.load("images/start_button-c.png")
start_button = start_button.convert_alpha()
start_button_x = (screen_width - start_button.get_width()) // 2
start_button_y = (screen_height - start_button.get_height()) // 2
start_button_rect = start_button.get_rect(topleft=(start_button_x, start_button_y))

credits_button = pygame.image.load("images/credits_button-c.png")
credits_button = credits_button.convert_alpha()
credits_button_x = (screen_width - credits_button.get_width()) // 2
credits_button_y = start_button_rect.bottom + 20
credits_button_rect = credits_button.get_rect(topleft=(credits_button_x, credits_button_y))

return_button = pygame.image.load("images/arrow-left.png").convert_alpha()
return_button_rect = return_button.get_rect(topleft=(150, 20))

next_button = pygame.image.load("images/arrow-down.png").convert_alpha()
next_button_rect = next_button.get_rect(bottomright=(screen_width - 150, screen_height - 20))

#images
background_img = pygame.image.load("images/background with kent.png").convert()
background_img_rect = background_img.get_rect(center=(screen_width // 2, screen_height // 2))

game_over_img = pygame.image.load("images/game over screen.png").convert_alpha()
game_over_img_rect = game_over_img.get_rect(center=(screen_width // 2, screen_height // 2))

victory_img = pygame.image.load("images/victory screen.png").convert_alpha()
victory_img_rect = victory_img.get_rect(center=(screen_width // 2, screen_height // 2))

problem_box = pygame.image.load("images/problem box.png").convert_alpha()
problem_box_rect = problem_box.get_rect(topleft=(screen_width * 0.10, screen_height * 0.0))

input_bar = pygame.image.load("images/input bar.png").convert_alpha()
input_bar_rect = input_bar.get_rect()
input_bar_rect = input_bar.get_rect(topleft=(problem_box_rect.left, problem_box_rect.top))

progress_bar = pygame.image.load("images/progress bar.png").convert_alpha()
progress_bar_rect = progress_bar.get_rect()
progress_bar_rect.midbottom = (screen_width // 2, screen_height - screen_height * 0.02)

logo = pygame.image.load("images/logo graffitsss.png").convert_alpha()
logo_rect = logo.get_rect(topright=(screen_width - screen_width * 0.10, screen_height * 0.02))

#Faces
face_correct = pygame.image.load("images/right answer face.png").convert_alpha()
face_wrong = pygame.image.load("images/wrong answer face.png").convert_alpha()

#Video
cutscene_vid = None
video_started = False

#Questions
def generate_question(question_number):
    if question_number <= 3:  # 1–3 Addition
        a, b = random.randint(1, 20), random.randint(1, 20)
        return f"{a} + {b}", a + b
    elif question_number <= 5:  # 4–5 Subtraction
        a, b = random.randint(10, 30), random.randint(1, 10)
        return f"{a} - {b}", a - b
    elif question_number == 6:  # 6 Multiplication
        a, b = random.randint(2, 10), random.randint(2, 10)
        return f"{a} × {b}", a * b
    elif question_number == 7:  # 7 Division
        b = random.randint(2, 10)
        a = b * random.randint(2, 10)
        return f"{a} ÷ {b}", a // b
    elif question_number == 8:  # 8 Arithmetic sequence 
        a, d = random.randint(1, 10), random.randint(1, 5)
        n = random.randint(4, 6)
        return f"{a}, {a+d}, {a+2*d}, ...\nfind term {n}", a + (n-1)*d #HEREEEEEEEE ദ്ദി(—ᴗ— )
    elif question_number == 9:  # 9 Geometric sequence
        a, r = random.randint(1, 5), random.randint(2, 4)
        n = random.randint(4, 6)
        return f"{a}, {a*r}, {a*r*r}, ...\nfind term {n}", a * (r**(n-1)) #AND HEREEEEEEEE then drawing code next ↓    
    elif question_number == 10:  # 10 PEMDAS
        a, b, c = random.randint(1, 20), random.randint(1,20), random.randint(1,20)
        expr = f"{a} + ({b} * {c})"
        return expr, eval(expr)
    else:  # Random after 10
        q_type = random.randint(1, 7)
        return generate_question(q_type)


#Timer
start_time = 45
time_left = start_time

#Game
answer_input = ""
current_question = ""
current_answer = 0
revealed_digits = ["_"] * 10
correct_count = 0
game_over = False
win = False

#Face overlay
reaction_face = None
face_timer = 0  #how long to show correct/wrong face

#Cursor
cursor_visible = True
cursor_timer = 0

# First question
current_question, current_answer = generate_question(1)
clock = pygame.time.Clock()

#for playing music each game state
current_song = None
def play_music(game_state):
    global current_song
    
    tick_sound.stop()
    correct_channel.stop()
    wrong_channel.stop()

    if game_state in ["menu", "credits", "credits_2"]:
        if current_song != "menu":
            pygame.mixer.music.load("bg music/menu theme.wav")
            pygame.mixer.music.play(-1)
            current_song = "menu"

    elif game_state == "game":
        if current_song != "game":
            pygame.mixer.music.load("bg music/main game bgm.wav")
            pygame.mixer.music.play(-1)
            current_song = "game"

    elif game_state == "win":
        if current_song != "win":
            pygame.mixer.music.load("bg music/win bgm final.wav")
            pygame.mixer.music.play(-1)
            current_song = "win"

    elif game_state == "lose":
        if current_song != "lose":
            pygame.mixer.music.load("bg music/lose bg.wav")
            pygame.mixer.music.play(-1)
            current_song = "lose"

#pang reset ng game every new round --- babalik sa default values
def reset_game():
    global time_left, correct_count, revealed_digits, game_over, win, video_started, cutscene_vid
    global answer_input, current_question, current_answer, reaction_face
    time_left = start_time
    correct_count = 0
    revealed_digits = ["_"] * 10
    game_over = False
    win = False
    answer_input = ""
    current_question, current_answer = generate_question(1)
    reaction_face = None
    tick_sound.play(-1)
    video_started = False
    cutscene_vid = None

play_music(game_state)
last_game_state = game_state

game_running = True
while game_running:
    dt = clock.tick(45) / 1000 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

        #previous game state ay saved in memory to check if nagbago
        if game_state != last_game_state:
            play_music(game_state)
            last_game_state = game_state

        if game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    game_state = "game"
                    reset_game()
                elif credits_button_rect.collidepoint(event.pos):
                    game_state = "credits"

        elif game_state == "credits":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_button_rect.collidepoint(event.pos):
                    game_state = "menu"
                elif next_button_rect.collidepoint(event.pos):
                    game_state = "credits_2"
        
        elif game_state == "credits_2":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_button_rect.collidepoint(event.pos):
                    game_state = "menu"

        elif game_state == "game":
            if event.type == pygame.USEREVENT + 10:
                correct_channel.stop()
                pygame.time.set_timer(pygame.USEREVENT + 10, 0)

            if event.type == pygame.USEREVENT + 11:
                wrong_channel.stop()
                pygame.time.set_timer(pygame.USEREVENT + 11, 0)

            if not game_over: 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if answer_input.strip() != "":
                            try:
                                if int(answer_input) == current_answer:
                                    revealed_digits[correct_count] = str(random.randint(0, 9))
                                    correct_count += 1
                                    reaction_face = face_correct
                                    face_timer = time.time()

                                    correct_channel.play(correct_sound)
                                    pygame.time.set_timer(pygame.USEREVENT + 10, 300)

                                    if correct_count == 10:
                                        game_over = True
                                        win = True
                                        correct_channel.stop()
                                        pygame.time.set_timer(pygame.USEREVENT + 10, 0)
                                else:
                                    time_left -= 3
                                    reaction_face = face_wrong
                                    face_timer = time.time()

                                    wrong_channel.play(wrong_sound)
                                    pygame.time.set_timer(pygame.USEREVENT + 11, 1500)

                                #New question
                                current_question, current_answer = generate_question(correct_count + 1)
                            except:
                                pass
                            answer_input = ""

                    elif event.key == pygame.K_BACKSPACE:
                        answer_input = answer_input[:-1]

                    else:
                        if event.unicode.isdigit():
                            answer_input += event.unicode

        #nilipat ko to dito para mareset pag space sa game over
        #nasira kasi yung SPACE gawa ng bagong game states
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_state = "menu"
            reset_game()
            tick_sound.play(-1)

    #drawing logic if menu or game state or credits hahaha
    if game_state == "menu":
        screen.blit(menu_bg_image, (0,0))
        screen.blit(start_button, start_button_rect)
        screen.blit(credits_button, credits_button_rect)
        
        grp_name = "Developed by LOG Studios"
        grp_text = CREDITS_FONT.render(grp_name, True, BLACK)
        grp_rect = grp_text.get_rect(bottomleft=(150, screen_height - 10))
        screen.blit(grp_text, grp_rect)

    elif game_state == "credits":
        screen.blit(no_title_bg, (0,0))
        screen.blit(return_button, return_button_rect)
        screen.blit(next_button, next_button_rect)
        
        conceptualization_text = FONT.render("Conceptualization:", True, BLACK)
        conceptualization_name = FONT.render("Glaezel Revano, Oz Rodas", True, BLACK)

        art_text = FONT.render("Art & Music:", True, BLACK)
        art_name = FONT.render("Oz Rodas", True, BLACK)

        programming_text = FONT.render("Programming:", True, BLACK)
        programming_name = FONT.render("Glaezel Revano, Lawrence Carmona", True, BLACK)

        center_x = screen_width // 2
        start_y = screen_height // 2 - 200

        screen.blit(conceptualization_text, conceptualization_text.get_rect(center=(center_x, start_y)))
        screen.blit(conceptualization_name, conceptualization_name.get_rect(center=(center_x, start_y + 60)))

        screen.blit(art_text, art_text.get_rect(center=(center_x, start_y + 150)))
        screen.blit(art_name, art_name.get_rect(center=(center_x, start_y + 200)))

        screen.blit(programming_text, programming_text.get_rect(center=(center_x, start_y + 290)))
        screen.blit(programming_name, programming_name.get_rect(center=(center_x, start_y + 350)))

    elif game_state == "credits_2":
        screen.blit(no_title_bg, (0,0))
        screen.blit(return_button, return_button_rect)

        about_font = pygame.font.Font("fonts/Six Hands Web Marker.ttf", 30)

        text_lines = [
            "MATIKKA serves as our passion project,",
            "wanting to showcase the thrill of mathematics",
            "and the charm of it through stylized graphics.",
            "Creating this game was a first-time experience",
            "for the three of us. It was fun, yet frustrating.",
            "But in the end, we are proud of what we accomplished.",
            "We hope you enjoyed playing!"
        ]

        center_x = screen_width // 2
        start_y = screen_height // 2 - 200
        line_spacing = 60

        for i, line in enumerate(text_lines):
            text_surface = about_font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(center=(center_x, start_y + i * line_spacing))
            screen.blit(text_surface, text_rect)

    elif game_state == "game":
        if not game_over:
            time_left -= dt
            if time_left <= 0:
                time_left = 0
                game_over = True
                win = False

        if reaction_face in (face_correct, face_wrong):
            if time.time() - face_timer > 1:
                reaction_face = None  

        #Cursor blinking
        cursor_timer += dt
        if cursor_timer >= 0.5:  #blinkspeed
            cursor_visible = not cursor_visible
            cursor_timer = 0

        #Images&text
        screen.blit(background_img, background_img_rect)

        if not game_over:
            # Question NAITO PO HUHU (╥ ᴗ ╥)
            screen.blit(problem_box, problem_box_rect)

            if 8 <= (correct_count + 1) <= 10:  # Questions 8 to 10
                lines = current_question.split("\n")
                y_offset = 50
                for line in lines:
                    q_text = FONTXS.render(line, True, BLACK)  
                    screen.blit(q_text, (190, y_offset))
                    y_offset += q_text.get_height() + 5
            else:
                q_text = FONTL.render(current_question, True, BLACK)  
                screen.blit(q_text, (215, 50))

            #Input
            screen.blit(input_bar, input_bar_rect)
            ans_text = FONTS.render(answer_input, True, BLACK)
            text_rect = ans_text.get_rect()
            text_rect.topleft = (input_bar_rect.x + 80, input_bar_rect.y + 230)
            screen.blit(ans_text, text_rect)

            #cursor
            if cursor_visible:
                if answer_input == "":
                    cursor_x = input_bar_rect.x + 90
                else:
                    cursor_x = text_rect.right + 5
                cursor_y = text_rect.y
                cursor_height = text_rect.height
                pygame.draw.line(screen, BLACK, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 3)

            #passcode
            screen.blit(progress_bar, progress_bar_rect)
            pass_text = PROGRESS_FONT.render(" ".join(revealed_digits), True, BLACK)
            screen.blit(pass_text, (500, 610))

            #timer
            timer_text_shadow = FONT.render(f"{int(time_left)} sec.", True, BLACK)
            timer_text = FONT.render(f"{int(time_left)} sec.", True, RED)
            screen.blit(timer_text, (860, 600))
            screen.blit(timer_text_shadow, (864, 600)) 
            screen.blit(timer_text, (860, 600))

            #reaction
            if reaction_face is not None:
                screen.blit(reaction_face, (130, 1))
            
            #logo
            screen.blit(logo, logo_rect)

        else:
            #Win/GameOver
            if win:
                if game_state != "win":
                    game_state = "win"

                if not video_started:
                    pygame.mixer.music.stop()
                    cutscene_vid = VideoFileClip("videos/VICTORY.mp4")
                    cutscene_vid.preview()
                    video_started = True
                    play_music("win")
                screen.blit(victory_img, victory_img_rect)
            else:
                if game_state != "lose":
                    game_state = "lose"
                if not video_started:
                    cutscene_vid = VideoFileClip("videos/explosion.mp4")
                    cutscene_vid.preview()
                    video_started = True
                screen.blit(game_over_img, game_over_img_rect)
                
    pygame.display.update()
pygame.quit()
