import pygame
from sudoku import validate, solve, new_board


def grid_next_space(index):
    x, y = index
    if x == 8:
        x = 0
        if y == 8:
            y = 0
        else:
            y += 1
    else:
        x += 1
    return x, y


def grid_previous_space(index):
    x, y = index
    if x == 0:
        x = 8
        if y == 0:
            y = 8
        else:
            y -= 1
    else:
        x -= 1
    return x, y


def grid_vert_up(index):
    x, y = index
    if y == 0:
        y = 8
    else:
        y -= 1
    return x, y


def grid_vert_down(index):
    x, y = index
    if y == 8:
        y = 0
    else:
        y += 1
    return x, y


class Grid:
    def __init__(self, win_width):
        self.init = pygame.init()
        self.board = new_board()
        self.board_before = new_board()
        self.text_font = pygame.font.Font("freesansbold.ttf", 30)
        self.win_width = win_width
        self.win_height = int(3 * win_width / 2)
        self.box_width = win_width / 9
        self.box_dimensions = (self.box_width, self.box_width)
        self.rect_height = (self.win_height - win_width) / 3
        self.rect_width = win_width / 3
        self.rect_vert_spacing = 2 * (self.win_height - win_width) / 5
        self.rect_hor_spacing = self.rect_width / 3
        self.rect_dimensions = (self.rect_width, self.rect_height)
        self.left_clear = self.rect_hor_spacing
        self.right_clear = self.left_clear + self.rect_width
        self.left_solve = self.right_clear + self.rect_hor_spacing
        self.right_solve = self.left_solve + self.rect_width
        self.top_clear = self.win_width + self.rect_vert_spacing
        self.bot_clear = self.top_clear + self.rect_height
        self.top_solve = self.win_width + self.rect_vert_spacing
        self.bot_solve = self.top_clear + self.rect_height
        self.win = pygame.display.set_mode((self.win_width, self.win_height))
        self.index = None
        self.text_color = None
        self.text = None
        self.text_y = self.win_width + (self.win_height - self.win_width) / 6  # y displacement for textbox
        self.black = (0, 0, 0)
        self.dark_grey = (50, 50, 50)
        self.white = (255, 255, 255)
        self.grey = (100, 100, 100)
        self.red = (200, 0, 0)
        self.green = (0, 200, 0)
        self.blue = (0, 0, 200)

    def display_board(self):
        for y in range(9):
            for x in range(9):
                if self.board[y][x] != 0:
                    key = str(self.board[y][x])
                    width = self.box_width
                    x_cor = x * width
                    y_cor = y * width
                    if self.board[y][x] == self.board_before[y][x]:
                        color = self.white
                    else:
                        color = self.green
                    self.display_text(key, x_cor, y_cor, width, width, color)

    def display_text(self, text, x, y, width, height, color):
        text_surface = self.text_font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = ((x + (width / 2)), (y + (height / 2)))
        self.win.blit(text_surface, text_rect)

    def append_grid(self, num, next_grid=True):
        if num == 0 or validate(self.board, self.index, num):
            x, y = self.index
            self.board[y][x] = num
            self.board_before[y][x] = num
            self.text = None
            self.text_color = None
            if next_grid:
                self.index = grid_next_space(self.index)
        else:  # prints invalid number
            self.text = "Invalid Number, Try Again"
            self.text_color = self.red

    def clear(self):
        self.board = new_board()
        self.board_before = new_board()
        self.text = "Cleared Board"
        self.text_color = self.red

    def init_solve(self):
        solve(self.board)
        self.text = "Solved Board"
        self.text_color = self.green

    def button(self, x, y, width, height, color, text, text_color):
        pygame.draw.rect(self.win, color, (x, y, width, height))
        self.display_text(text, x, y, width, height, text_color)

    def index_grid(self, mouse):
        x = (mouse[0] // self.box_width)
        y = (mouse[1] // self.box_width)
        return int(x), int(y)

    def hover_grid(self, mouse):
        index = self.index_grid(mouse)
        x, y = index
        pos = (x * self.box_width, y * self.box_width)
        s = pygame.Surface(self.box_dimensions)
        s.set_alpha(100)
        s.fill(self.white)
        self.win.blit(s, pos)

    def selected_grid(self, index):
        x, y = index
        pos = (x * self.box_width, y * self.box_width)
        s = pygame.Surface(self.box_dimensions)
        s.set_alpha(100)
        s.fill(self.white)
        self.win.blit(s, pos)

    def hover_button(self, cor, color):
        s = pygame.Surface(self.rect_dimensions)
        s.set_alpha(100)
        s.fill(color)
        self.win.blit(s, cor)

    def run(self):
        pygame.display.set_caption("Sudoku Solver")
        run = True

        while run:
            self.win.fill(self.dark_grey)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if 0 < mouse[0] < self.win_width and 0 < mouse[1] < self.win_width:  # within grid
                        self.index = self.index_grid(mouse)
                    elif self.left_clear < mouse[0] < self.right_clear and self.top_clear < mouse[1] < self.bot_clear:
                        self.clear()
                    elif self.left_solve < mouse[0] < self.right_solve and self.top_solve < mouse[1] < self.bot_solve:
                        self.init_solve()
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_ESCAPE]:  # ends game
                        run = False
                        break
                    if self.index:
                        if keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]:  # solves puzzle
                            self.init_solve()
                        if keys[pygame.K_1] or keys[pygame.K_KP1]:  # for num row and numpad
                            self.append_grid(1)
                        if keys[pygame.K_2] or keys[pygame.K_KP2]:
                            self.append_grid(2)
                        if keys[pygame.K_3] or keys[pygame.K_KP3]:
                            self.append_grid(3)
                        if keys[pygame.K_4] or keys[pygame.K_KP4]:
                            self.append_grid(4)
                        if keys[pygame.K_5] or keys[pygame.K_KP5]:
                            self.append_grid(5)
                        if keys[pygame.K_6] or keys[pygame.K_KP6]:
                            self.append_grid(6)
                        if keys[pygame.K_7] or keys[pygame.K_KP7]:
                            self.append_grid(7)
                        if keys[pygame.K_8] or keys[pygame.K_KP8]:
                            self.append_grid(8)
                        if keys[pygame.K_9] or keys[pygame.K_KP9]:
                            self.append_grid(9)
                        if keys[pygame.K_0] or keys[pygame.K_KP0] or keys[pygame.K_SPACE] or keys[pygame.K_BACKSPACE]:
                            self.append_grid(0, False)
                        if keys[pygame.K_DELETE]:
                            if keys[pygame.K_LCTRL]:
                                self.clear()
                            else:
                                self.append_grid(0, False)
                        if keys[pygame.K_TAB]:
                            if keys[pygame.K_LSHIFT]:
                                self.index = grid_previous_space(self.index)
                            else:
                                self.index = grid_next_space(self.index)
                        if keys[pygame.K_RIGHT]:
                            self.index = grid_next_space(self.index)
                        if keys[pygame.K_LEFT]:
                            self.index = grid_previous_space(self.index)
                        if keys[pygame.K_UP]:
                            self.index = grid_vert_up(self.index)
                        if keys[pygame.K_DOWN]:
                            self.index = grid_vert_down(self.index)

            # draw GUI elements
            for x in range(1, 9):
                pos = (x / 9) * self.win_width
                if x % 3 == 0:
                    line_color = self.white
                else:
                    line_color = self.grey
                pygame.draw.line(self.win, line_color, (pos, 0), (pos, self.win_width))
                pygame.draw.line(self.win, line_color, (0, pos), (self.win_width, pos))
            self.button(self.left_clear, self.top_clear, self.rect_width, self.rect_height, self.red, "CLEAR", self.black)
            self.button(self.left_solve, self.top_solve, self.rect_width, self.rect_height, self.green, "SOLVE", self.black)
            self.display_board()

            # hover
            mouse = pygame.mouse.get_pos()
            if 0 < mouse[0] < self.win_width and 0 < mouse[1] < self.win_width:  # mouse is in grid
                self.hover_grid(mouse)
            if self.left_clear < mouse[0] < self.right_clear and self.top_clear < mouse[1] < self.bot_clear:
                self.hover_button((self.left_clear, self.top_clear), self.white)
            if self.left_solve < mouse[0] < self.right_solve and self.top_solve < mouse[1] < self.bot_solve:
                self.hover_button((self.left_solve, self.top_solve), self.white)

            # non-static GUI elements
            if self.index:
                self.selected_grid(self.index)
            if self.text_color:
                self.display_text(self.text, 0, self.text_y, self.win_width, self.box_width, self.text_color)

            pygame.display.update()

        pygame.quit()


game = Grid(603)
game.run()
