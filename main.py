import pygame


paused = True

foreground_colour = (255, 255, 255)
grid_colour = (125, 125, 125)
background_colour = (0, 0, 0)
grid_size = [80, 40]
cell_size = [16, 16]
line_size = 1
label_height = 48
icon_size = 32

grid = [[False for x in range(grid_size[0])] for y in range(grid_size[1])]
grid_image_height = grid_size[1] * (cell_size[1] + line_size)
screen_width = grid_size[0] * (cell_size[0] + line_size)
screen_height = grid_image_height + label_height

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Conway's Game of Life")
pygame.font.init()
font = pygame.font.SysFont("Consolas", 36)

image = pygame.Surface((icon_size, icon_size)).convert_alpha()
image.fill(background_colour)
square = pygame.Surface((icon_size / 2, icon_size / 2))
square.fill(foreground_colour)
image.blit(square, (0, 0))
image.blit(square, (icon_size / 2, icon_size / 2))
pygame.display.set_icon(image)
    
def game_loop():
    global paused
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused:
            update_grid()
        screen.fill(grid_colour)
        draw_grid()
        draw_label()
        pygame.display.flip()
        clock.tick(20)


def handle_mouse_click(mouse_pos):
    x = int(mouse_pos[0] / (cell_size[0] + line_size))
    y = int(mouse_pos[1] / (cell_size[1] + line_size))
    grid[y][x] = not grid[y][x]


def update_grid():
    neighbor_grid = [[calculate_neighbors(x, y) for x in range(grid_size[0])]
                     for y in range(grid_size[1])]

    for y in range(grid_size[1]):
        for x in range(grid_size[0]):
            determine_fate_of_cell(x, y, neighbor_grid[y][x])


def calculate_neighbors(x, y):
    neighbors = [get_value(x, y - 1), get_value(x, y + 1),
                 get_value(x - 1, y), get_value(x + 1, y),
                 get_value(x - 1, y - 1), get_value(x - 1, y + 1),
                 get_value(x + 1, y - 1), get_value(x + 1, y + 1)]
    return neighbors.count(True)


def determine_fate_of_cell(x, y, num_of_neighbors):
    if num_of_neighbors < 2:
        grid[y][x] = False
    elif num_of_neighbors == 3:
        grid[y][x] = True
    elif num_of_neighbors > 3:
        grid[y][x] = False


def get_value(x, y):
    try:
        if y < 0 or x < 0:
            raise IndexError
        return grid[y][x]
    except IndexError:
        return False


def draw_grid():
    for y in range(grid_size[1]):
        for x in range(grid_size[0]):
            draw_cell(x, y)


def draw_cell(x, y):
    rect = pygame.Rect(x * (cell_size[0] + line_size),
                       y * (cell_size[1] + line_size),
                       cell_size[0], cell_size[1])
    colour = foreground_colour if grid[y][x] else background_colour
    pygame.draw.rect(screen, colour, rect)


def draw_label():
    background = pygame.Surface((screen_width, label_height))
    background.fill(background_colour)
    screen.blit(background, (0, grid_image_height))

    text = "SIMULATION PAUSED" if paused else "SIMULATION PLAYING"
    font_image = font.render(text, 4, foreground_colour)
    font_image = font_image.subsurface(font_image.get_bounding_rect())
    x_pos = screen_width/2 - font_image.get_width()/2
    y_pos = grid_image_height + label_height / 2 - font_image.get_height()/2
    screen.blit(font_image, (x_pos, y_pos))

if __name__ == "__main__":
    game_loop()
