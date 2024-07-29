import math
import random
import pygame


def knockback(e, timer, speed, face):
    timer -= 1
    if timer > 0:
        if speed > 0:
            speed -= 0.1
        if face == "right":
            e.hitbox.x += speed
        if face == "left":
            e.hitbox.x -= speed
        if face == "top":
            e.hitbox.y -= speed
        if face == "bottom":
            e.hitbox.y += speed
    return timer, speed


class Infant:
    def __init__(self, x, y, team):
        self.hitbox = pygame.FRect(x, y, 64, 64)
        self.team = team
        self.pathfind = False
        self.target_timer = 0
        self.speed = 1
        self.health = 5

    def update(self, entity_list):
        keys = pygame.key.get_pressed()

        # collision
        for e in entity_list:
            if e != self:
                if self.hitbox.colliderect(e.hitbox):  # necessary clause to see if the infant is actually hitting anything

                    # damaging the enemy
                    if e.team:
                        if e.team != self.team:
                            # e.health -= 1
                            if e.hitbox.left <= self.hitbox.right <= e.hitbox.right:  # right
                                knockback(e, 100, 5, "right")
                            if e.hitbox.left <= self.hitbox.left <= e.hitbox.right:  # left
                                knockback(e, 100, 5, "left")
                            if e.hitbox.top <= self.hitbox.top <= e.hitbox.bottom:  # top
                                knockback(e, 100, 5, "top")
                            if e.hitbox.top <= self.hitbox.bottom <= e.hitbox.bottom:  # bottom
                                knockback(e, 100, 5, "bottom")

                    # regular collision
                    if e.hitbox.left <= self.hitbox.right <= e.hitbox.right:  # right-side collision
                        self.hitbox.x -= self.speed
                    if e.hitbox.left <= self.hitbox.left <= e.hitbox.right:  # left-side collision
                        self.hitbox.x += self.speed
                    if e.hitbox.top <= self.hitbox.top <= e.hitbox.bottom:  # top-side collision
                        self.hitbox.y += self.speed
                    if e.hitbox.top <= self.hitbox.bottom <= e.hitbox.bottom:  # bottom-side collision
                        self.hitbox.y -= self.speed

        if len(entity_list) > 1 and self.pathfind:
            closest_target = ()

            # constantly check for closest entity
            ranges = []
            hypes = []
            for e in entity_list:
                if e != self and e.team != self.team:
                    ranges.append((e.hitbox.x, e.hitbox.y))
                    hypes.append(math.hypot(e.hitbox.x - self.hitbox.x, e.hitbox.y - self.hitbox.y))

            if len(ranges) > 0 and self.health:
                closest_target = tuple(ranges[hypes.index(min(hypes))])

            # pathfind to closest target
            if closest_target:
                if self.hitbox.x > closest_target[0]:
                    self.hitbox.x -= self.speed
                elif self.hitbox.x < closest_target[0]:
                    self.hitbox.x += self.speed
                if self.hitbox.y > closest_target[1]:
                    self.hitbox.y -= self.speed
                elif self.hitbox.y < closest_target[1]:
                    self.hitbox.y += self.speed

        if self.health <= 0:
            print("Dead")
            entity_list.remove(self)

        if keys[pygame.K_SPACE]:
            self.pathfind = True

    def draw(self, surf):
        if self.team == "yellow":
            surf.blit(pygame.transform.scale(pygame.image.load("assets/yellow_blindshot_infant.png"), (64, 64)), self.hitbox)
        elif self.team == "purple":
            surf.blit(pygame.transform.scale(pygame.image.load("assets/purple_blindshot_infant.png"), (64, 64)), self.hitbox)