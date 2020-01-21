import pygame


class GameOfLife:
    """ Cell simulation following Conway's Game of Life. Press space to pause/unpause """
    GRID_SIZE = [120, 80]
    GRID_ON_SCREEN = [80, 40]
    GRID_PADDING = 20
    CELL_SIZE = [16, 16]
    LINE_SIZE = 1
    LABEL_HEIGHT = 48
    FONT_SIZE = 36
    SCREEN_SIZE = (GRID_ON_SCREEN[0] * (CELL_SIZE[0] + LINE_SIZE), 
            GRID_ON_SCREEN[1] * (CELL_SIZE[1] + LINE_SIZE) + LABEL_HEIGHT)
    BACKGROUND_COLOR = (0, 0, 0)
    LINE_COLOR = (36, 34, 52)
    CELL_COLOR = (255, 255, 255)
    FONT_COLOR = (255, 255, 255)

    def __init__(self):
        """ Create a new simulation """
        pygame.init()
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        pygame.display.set_caption("Conway's Game of Life")
        self.set_icon()
        self.grid = [[False for x in range(self.GRID_SIZE[0])] for y in range(self.GRID_SIZE[1])]
        self.font = pygame.font.SysFont("Consolas", self.FONT_SIZE)
        self.clock = pygame.time.Clock()
        self.paused = True
        self.loop()

    def set_icon(self):
        """ Create basic icon """
        image = pygame.Surface((32, 32)).convert_alpha()
        image.fill(self.BACKGROUND_COLOR)
        pygame.draw.rect(image, self.CELL_COLOR, (0, 0, 16, 16))
        pygame.draw.rect(image, self.CELL_COLOR, (16, 16, 16, 16))
        pygame.display.set_icon(image)

    def loop(self):
        """ Event, update, and draw loop """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
            if not self.paused:
                self.update_grid()
            self.screen.fill(self.LINE_COLOR)
            self.draw_grid()
            self.draw_label()
            pygame.display.flip()
            self.clock.tick(20)

    def handle_mouse_click(self, mouse_pos):
        """ Flip state of cell at mouse location """
        x = int(mouse_pos[0] / (self.CELL_SIZE[0] + self.LINE_SIZE)) + self.GRID_PADDING
        y = int(mouse_pos[1] / (self.CELL_SIZE[1] + self.LINE_SIZE)) + self.GRID_PADDING
        self.grid[y][x] = not self.grid[y][x]

    def update_grid(self):
        """ Update the state of cells based off the simulation rules """
        self.neighbor_grid = [[self.calculate_neighbors(x, y) for x in range(self.GRID_SIZE[0])] 
                for y in range(self.GRID_SIZE[1])]
        for y in range(self.GRID_SIZE[1]):
            for x in range(self.GRID_SIZE[0]):
                self.determine_fate_of_cell(x, y, self.neighbor_grid[y][x])


    def calculate_neighbors(self, x, y):
        """ Return the number of "alive" neighboring cells """
        neighbors = [self.get_value(x, y - 1), self.get_value(x, y + 1),
                    self.get_value(x - 1, y), self.get_value(x + 1, y),
                    self.get_value(x - 1, y - 1), self.get_value(x - 1, y + 1),
                    self.get_value(x + 1, y - 1), self.get_value(x + 1, y + 1)]
        return neighbors.count(True)

    def determine_fate_of_cell(self, x, y, num_of_neighbors):
        """ Follow the rules of the simulation """
        if num_of_neighbors < 2:
            self.grid[y][x] = False
        elif num_of_neighbors == 3:
            self.grid[y][x] = True
        elif num_of_neighbors > 3:
            self.grid[y][x] = False

    def get_value(self, x, y):
        """ Return the value at x,y or False if out of range """
        try:
            if y < 0 or x < 0:
                raise IndexError
            return self.grid[y][x]
        except IndexError:
            return False

    def draw_grid(self):
        """ Draw cells """
        for y in range(self.GRID_ON_SCREEN[1]):
            for x in range(self.GRID_ON_SCREEN[0]):
                self.draw_cell(x, y)

    def draw_cell(self, x, y):
        """ Draw cell at position """
        rect = pygame.Rect(x * (self.CELL_SIZE[0] + self.LINE_SIZE),
                        y * (self.CELL_SIZE[1] + self.LINE_SIZE),
                        self.CELL_SIZE[0], self.CELL_SIZE[1])
        color = self.BACKGROUND_COLOR
        if self.grid[y+self.GRID_PADDING][x+self.GRID_PADDING]:
            color = self.CELL_COLOR
        pygame.draw.rect(self.screen, color, rect)

    def draw_label(self):
        """ Draw simulation paused/playing label at bottom of screen """
        background = pygame.Surface(self.SCREEN_SIZE)
        background.fill(self.BACKGROUND_COLOR)
        self.screen.blit(background, (0, self.SCREEN_SIZE[1] - self.LABEL_HEIGHT))

        text = "SIMULATION PAUSED" if self.paused else "SIMULATION PLAYING"
        font_image = self.font.render(text, 4, self.FONT_COLOR)
        font_image = font_image.subsurface(font_image.get_bounding_rect())
        x_pos = int(self.SCREEN_SIZE[0]/2 - font_image.get_width()/2)
        y_pos = int(self.SCREEN_SIZE[1] - self.LABEL_HEIGHT / 2 - font_image.get_height()/2)
        self.screen.blit(font_image, (x_pos, y_pos))


if __name__ == "__main__":
    GameOfLife()
