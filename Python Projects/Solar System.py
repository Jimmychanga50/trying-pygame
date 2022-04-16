#My first time trying Pygame...
#Huge thanks to the Youtube channel "Tech With Tim"


import pygame
import math
pygame.init()



WIN = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Solar System")
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 132, 255)
MERC = (184, 78, 37)
VEN = (87, 158, 146)

FONT = pygame.font.SysFont("comicsans", 20)


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    scale = 250 / AU
    timestep = 3600 * 24
    
    def __init__(self, pos_x, pos_y, colour, mass, radius, name):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.colour = colour
        self.mass = mass
        self.radius = radius
        self.name = name

        self.sun = False

        self.x_vel = 0
        self.y_vel = 0

        self.dist_sun = 0

    def place(self, win):
        pos_x = self.pos_x * self.scale + 400
        pos_y = self.pos_y * self.scale + 400
        pygame.draw.circle(win, self.colour, (pos_x, pos_y), self.radius)
        if not self.sun:
            name_txt = FONT.render(f"{self.name}", 1, WHITE)
            win.blit(name_txt, (pos_x, pos_y))
        else:
            name_txt = FONT.render(f"{self.name}", 1, RED)
            win.blit(name_txt, (pos_x, pos_y))

    def attraction(self, other):
        other_x, other_y = other.pos_x, other.pos_y
        distance_x = other_x - self.pos_x
        distance_y = other_y - self.pos_y
        distance = math.sqrt((distance_x ** 2) + (distance_y ** 2))

        force = self.G * self.mass * other.mass / distance**2 #physics formula
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.timestep 
        self.y_vel += total_fy / self.mass * self.timestep  #more physics...

        self.pos_x += self.x_vel * self.timestep
        self.pos_y += self.y_vel * self.timestep


def main_loop():
    run = True
    clock = pygame.time.Clock()
    bg = pygame.image.load("bg.jpg")

    sun = Planet(0, 0, YELLOW, 1.98892 * 10**30, 30, "SUN")
    sun.sun = True
    
    mercury = Planet(0.387 * Planet.AU, 0, MERC, 0.330 * 10**24, 8, "Mercury")
    mercury.y_vel = -47.4 * 1000
    
    venus = Planet(0.723 * Planet.AU, 0, VEN, 4.8685 * 10**24, 14, "Venus")
    venus.y_vel = -35.02 * 1000
    
    earth = Planet(-1 * Planet.AU , 0, BLUE, 5.9742 * 10**24, 16, "Earth")
    earth.y_vel = 29.783 * 1000
    
    planets = [sun, earth, mercury, venus]
    
    while run:
        clock.tick(60)
        WIN.blit(bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.place(WIN)

        pygame.display.update()

    pygame.quit()


main_loop()
