import pygame
from pygame.locals import *


# haxed & adapted from http://stackoverflow.com/a/19120806
grid = [[1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]]
resolution = (360, 360)
# hm yeah dunno about this margin thing
cell_margin = 0
cell_colors = (255, 255, 255), (0, 0, 0)
player_character = "@"
water_character = "."
player_color = (127, 127, 127)
player_size = 40
water_size = 20
current_position = [0, 1]

def main():
    pygame.init()
    screen = pygame.display.set_mode(resolution)
    screen.fill(cell_colors[1])
    player = pygame.font.Font(None, player_size).render(player_character, False, player_color)
    tile_font = pygame.font.Font(None, water_size)
    tile = tile_font.render(water_character, False, (255,255,255))
    while True:
        # handle the different event types
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                key = event.key
                # INPUT TOWN
                if key == K_UP:
                    move(0, -1)
                elif key == K_RIGHT:
                    move(1, 0)
                elif key == K_DOWN:
                    move(0, 1)
                elif key == K_LEFT:
                    move(-1, 0)
            # player quits q.q
            elif event.type == QUIT:
                return
        draw_world(screen, tile)
        draw_player(player, screen)
        pygame.display.update()

def draw_world(screen, tile):
    # fill the entire screen with BLACK
    screen.fill((0,0,0))
    isOdd = False
    for row in xrange(len(grid)):
        for column in xrange(len(grid[0])):
            pos = get_cell_rect((row, column), screen)
            # debug-draw a filled rectangle every odd tile
            if not isOdd:
                screen.fill((255, 0, 0), pos)
                isOdd = True
            else:
                isOdd = False

            # get the screen position for the tile
            font_pos = get_font_rect((row, column), screen, tile)
            # draw the tile
            screen.blit(tile, font_pos)

# determine the screen position of a simple surface within the grid
def get_cell_rect(coordinates, screen):
    row, column = coordinates
    cell_width = screen.get_width() / len(grid)
    return pygame.Rect(row * cell_width,
                       column * cell_width,
                       cell_width, cell_width)

def get_font_rect(coordinates, screen, tile):
    row, column = coordinates
    cell_width = screen.get_width() / len(grid)
    # Rect uses Top and Left, so we need to add half of the cell_width to get
    # to the center of the cell, and then subtract half of the e.g. tile width
    # to get the ~true~ center for displaying the character surface
    return pygame.Rect(row * cell_width + cell_width/2 - tile.get_width() / 2,
                       column * cell_width + cell_width/2 - tile.get_height() / 2,
                       cell_width, cell_width)



def draw_player(player, screen):
    rect = player.get_rect()
    rect.center = get_cell_rect(current_position, screen).center
    screen.blit(player, rect)

def move(dx, dy):
    x, y = current_position
    nx, ny = x + dx, y + dy
    if nx >= 0 and nx < len(grid) and ny >= 0 and ny < len(grid[0]) and \
       grid[ny][nx]:
        current_position[0] = nx
        current_position[1] = ny

if __name__ == "__main__":
    main()
    pygame.quit()

