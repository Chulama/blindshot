import pygame
import sys
import entities

width, height = 1024, 1024
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

pygame.display.set_caption("Blindshot v0.0.1")
pygame.init()

# lazy way of making a border
border_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
border = []
rail = []
y = 0
for row in border_map:
    x = 0
    for cell in row:
        if cell == 1:
            border.append(pygame.Rect(x, y, 64, 64))
        elif cell == 2:
            rail.append(pygame.Rect(x, y, 64, 64))
        x += 64
    y += 64

purple_zone = 512
yellow_zone = 512
entity_list = []
entity_hitbox_list = []  # temporary

while True:
    mouse_pos = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                entity_list.append(entities.Infant(mouse_pos[0] // 64 * 64, mouse_pos[1] // 64 * 64, "yellow"))
                entity_hitbox_list.append(entity_list[-1].hitbox)
            elif event.button == 3:
                entity_list.append(entities.Infant(mouse_pos[0] // 64 * 64, mouse_pos[1] // 64 * 64, "purple"))
                entity_hitbox_list.append(entity_list[-1].hitbox)

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (159, 135, 248), (0, 0, 1024, purple_zone))  # purple zone
    pygame.draw.rect(screen, (248, 240, 91), (0, 1024 - yellow_zone, 1024, yellow_zone))  # yellow zone
    pygame.draw.rect(screen,
                     (0, 0, 0),
                     (mouse_pos[0] // 64 * 64, mouse_pos[1] // 64 * 64, 64, 64),
                     )  # snaps a 64x64 rectangle to grid

    # rails
    for n, block in enumerate(rail):
        if n >= len(rail) // 2:
            screen.blit(pygame.transform.scale(pygame.image.load("assets/yellow_rail.png"), (64, 64)), block)
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("assets/purple_rail.png"), (64, 64)), block)

    # entities
    for e in entity_list:
        e.update(entity_list)
        e.draw(screen)

    # border
    for n, block in enumerate(border):
        if n >= len(border) // 2:
            screen.blit(pygame.transform.scale(pygame.image.load("assets/yellow_border.png"), (64, 64)), block)
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("assets/purple_border.png"), (64, 64)), block)
    pygame.display.update()
    clock.tick(60)
