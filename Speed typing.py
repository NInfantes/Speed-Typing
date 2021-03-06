# import pygame and other built-in python functions
import pygame
from pygame.locals import *
import sys
import time
import random

# define variables of the project
class Game:

# define width and height of the window as 750x500
# define variables that are needed for the calculation
# self as a convention to refer to instance attributes
    def __init__(self):
        self.w = 750
        self.h = 500
        self.reset = True
        self.active = False
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Time:0 Accuracy:0 % Wpm:0 '
        self.wpm = 0
        self.end = False
        self.HEAD_C = (145, 213, 102)
        self.TEXT_C = (240, 240, 240)
        self.RESULT_C = (255, 70, 70)

# load images
        pygame.init()
        self.open_img = pygame.image.load ('First screen.jpg')
        self.open_img = pygame.transform.scale(self.open_img, (self.w, self.h))

        self.bg = pygame.image.load('Final.jpeg')
        self.bg = pygame.transform.scale(self.bg, (750, 500))

        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Type Speed test')

# define the font,text ,size and color of the screen
    def draw_text(self, screen, msg, y, fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1, color)
        text_rect = text.get_rect(center=(self.w / 2, y))
        screen.blit(text, text_rect)
        pygame.display.update()

# define where and how to get a sentence for the test
    def get_sentence(self):
        f = open('sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence

# define the results of the typing test
    def show_results(self, screen):
        if (not self.end):
            # Calculate time
            self.total_time = time.time() - self.time_start

            # Calculate accuracy
            count = 0
            for i, c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count / len(self.word) * 100

            # Calculate words per minute
            self.wpm = len(self.input_text.split()) * 60 / self.total_time
            self.end = True
            print(self.total_time)

            # write results line
            self.results = 'Time: ' + str(round(self.total_time)) + " secs   Accuracy: " + str(
                round(self.accuracy)) + "%" + '   Words/Minute: ' + str(round(self.wpm))

            # draw icon image with reset option
            self.time_img = pygame.image.load('keep-calm-and-try-again.png')
            self.time_img = pygame.transform.scale(self.time_img, (225, 150))
            # screen.blit(self.time_img, (80,320))
            screen.blit(self.time_img, (self.w / 2 - 110, self.h - 140))


            print(self.results)
            pygame.display.update()

# run the game with all events
    def run(self):
        self.reset_game()

        self.running = True
        while (self.running):
            clock = pygame.time.Clock()
            self.screen.fill((0, 0, 0), (50, 250, 650, 50))
            pygame.draw.rect(self.screen, self.HEAD_C, (50, 250, 650, 50), 2)
            # update the text of user input
            self.draw_text(self.screen, self.input_text, 274, 26, (250, 250, 250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # position of input box
                    if (x >= 50 and x <= 650 and y >= 250 and y <= 300):
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time()
                        # position of reset box
                    if (x >= 310 and x <= 510 and y >= 390 and self.end):
                        self.reset_game()
                        x, y = pygame.mouse.get_pos()


                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_results(self.screen)
                            print(self.results)
                            self.draw_text(self.screen, self.results, 350, 28, self.RESULT_C)
                            self.end = True

                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass

            pygame.display.update()

        clock.tick(60)

# reset all variables to repeat the typing test
    def reset_game(self):
        self.screen.blit(self.open_img, (0, 0))

        pygame.display.update()
        time.sleep(1)

        self.reset = False
        self.end = False
        self.active = False

        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        # Get random sentence
        self.word = self.get_sentence()
        if (not self.word): self.reset_game()
        # drawing heading
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        msg = "Typing Speed Test"
        self.draw_text(self.screen, msg, 40, 80, self.HEAD_C)
        # drawing introduction sentence
        msg2 = "Click on the box and write the below sentence (Press ENTER to submit):"
        self.draw_text(self.screen, msg2, 100, 20, self.HEAD_C)
        # draw the rectangle for input box
        pygame.draw.rect(self.screen, (255, 192, 25), (50, 250, 650, 50), 2)

        # draw the sentence string
        self.draw_text(self.screen, self.word, 200, 28, self.TEXT_C)

        pygame.display.update()


Game().run()

