import pygame
import struct
from pygame.locals import *

def hex2rgb(hex_str):
    return struct.unpack('BBB', hex_str.decode('hex'))

# initially haxed & adapted from http://stackoverflow.com/a/19120806
grid = {"x": 12, "y": 12}
resolution = (400, 400)
player_character = "@"
water_character = "~"
# we have colors! (maybe we shouldn't have colors tho; B/W is a clean aesthetic)
player_color = hex2rgb("B23530")
water_color = hex2rgb("143365")
bg_color = hex2rgb("000000")
# screen horizontal res / grid width
font_size =  resolution[0] / grid["x"]
current_position = [0, 1]

def main():
    pygame.init()
    screen = pygame.display.set_mode(resolution)
    screen.fill(bg_color)
    # save the Surfaces for the player character, and tile characters
    player = pygame.font.SysFont("monspace", font_size).render(player_character, False, player_color)
    tile = pygame.font.SysFont("monospace", font_size).render(water_character, False, water_color)

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
    # fill the entire screen with the background color
    screen.fill(bg_color)
    isOdd = False
    for row in xrange(grid["x"]):
        for column in xrange(grid["y"]):
            pos = get_cell_rect((row, column), screen)
            # debug-draw a filled rectangle every odd tile
            if not isOdd:
                # screen.fill((255, 0, 0), pos)
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
    cell_width = screen.get_width() / grid["x"]
    cell_width = font_size
    return pygame.Rect(row * cell_width,
                       column * cell_width,
                       cell_width, cell_width)

def get_font_rect(coordinates, screen, tile):
    row, column = coordinates
    cell_width = screen.get_width() / grid["x"]
    # Rect uses Top and Left, so we need to add half of the cell_width to get
    # to the center of the cell, and then subtract half of the e.g. tile width
    # to get the ~true~ center for displaying the character surface
    return pygame.Rect(row * cell_width + cell_width/2 - tile.get_width() / 2,
                       column * cell_width + cell_width/2 - tile.get_height() / 2,
                       cell_width, cell_width)

def draw_player(player, screen):
    rect = player.get_rect()
    current_pos = get_cell_rect(current_position, screen)
    screen.fill(bg_color, current_pos)
    rect.center = current_pos.center
    screen.blit(player, rect)

def move(dx, dy):
    x, y = current_position
    nx, ny = x + dx, y + dy
    if nx >= 0 and nx < grid["x"] and ny >= 0 and ny < grid["y"]:
        current_position[0] = nx
        current_position[1] = ny

if __name__ == "__main__":
    main()
    pygame.quit()

