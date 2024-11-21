# create virtual environment .venv
# python -m venv .venv

# upgrade pip if necessary
# python -m pip install --upgrade pip

# activate virtual environment .venv
# .\.venv\Scripts\activate

# install required libraries
# pip install -r .\requirements.txt
# requirements.txt contains:
# numpy
# tensorflow
# keras==2.12
# matplotlib
# get errors without deprecating keras

# uninstall libraries if needed to start again..
# pip freeze > current.txt
# pip uninstall -r .\current.txt -y

import pygame
import math

WIN_WIDTH, WIN_HEIGHT = 800, 800
BLACK   = (1, 1, 1)
YELLOW  = (255, 255, 0)
BLUE    = (100, 149, 237)
DARK_BLUE    = (50, 70, 250)
RED     = (188, 39, 50)
WHITE   = (255, 255, 255)

DARK_GREY    = (80, 78, 81)

GREY = (120,120,120)

class Planet:
    AU          = 149597870700 # in meters
    MASSOFSUN   = 1.98892e+30
    G           = 6.67428e-11
    SCALE       = 200 / AU  # 1 AU is about 100 pixels...
    TIMESTEP    = 3600 * 24   # seconds in 1 day

    def __init__(self, name, x, y, radius, colour, mass, orbits ):
        self.name = name
        self.x = x
        self.y = y
        self.radius = ( radius / 2 ) + 1
        self.colour = colour
        self.mass = mass
        self.isSun = False

        if orbits == None:
            self.isSun == True
        else:
            self.isSun = False

        self.orbits = orbits 

        self.x_vel = 0
        self.y_vel = 0
        if self.x:
            if ( name == 'Moon'):
                pass

            dist_x = abs(self.x)
            self.y_vel = math.sqrt( abs( (self.G * self.orbits.mass) / dist_x ) )
            print(self.name, self.x, self.y_vel)

        self.distance_to_sun = 0
        self.orbit = []

    def draw(self, win):
        if ( self.name == 'Moon'):
            pass
        
        if len(self.orbit) > 20:
            x0 = None
            y0 = None
            count = 20

            for trace in self.orbit[-20:]:
                orbit_x = trace[0]
                orbit_y = trace[1]
#            if self.orbits:
 #                   x1 = ( orbit_x + self.orbits.x ) * self.SCALE + ( WIN_WIDTH / 2  )
 #                   y1 = ( orbit_y + self.orbits.y ) * self.SCALE + ( WIN_HEIGHT / 2 )
 #               else:
                colR = self.colour[0] * ( 20 - count ) / 20
                colG = self.colour[1] * ( 20 - count ) / 20
                colB = self.colour[2] * ( 20 - count ) / 20           
                col = (colR, colG, colB)                      
                x1 = ( orbit_x ) * self.SCALE + ( WIN_WIDTH / 2  )
                y1 = ( orbit_y ) * self.SCALE + ( WIN_HEIGHT / 2 )
                
                if x0:
                    pygame.draw.line(win, col,  (x0, y0), (x1, y1), 1 )
                x0 = x1
                y0 = y1
                count -= 1

        if self.orbits:
            x = ( self.x + self.orbits.x ) * self.SCALE + ( WIN_WIDTH / 2  )
            y = ( self.y + self.orbits.y) * self.SCALE + ( WIN_HEIGHT / 2 )
        else:
            x = ( self.x ) * self.SCALE + ( WIN_WIDTH / 2  )
            y = ( self.y ) * self.SCALE + ( WIN_HEIGHT / 2 )
        pygame.draw.circle(win, self.colour, (x, y), self.radius)
        font = pygame.font.SysFont("arial", 12)
        text = font.render(self.name, True, self.colour)
        win.blit(text, (x - int(self.radius),y + self.radius))


    def attraction(self, other):
        other_x, other_y = (0,0)  #other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x **2 + distance_y ** 2)
        if other.isSun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / ( distance ** 2 )

        theta = math.atan2( distance_y, distance_x )

        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y
    
    def update_position(self, planets):
        total_force_x = total_force_y = 0
        if self.orbits:
            total_force_x, total_force_y = self.attraction(self.orbits)
   #     for planet in planets:
   #         if self == planet:
   #             continue
   #         fx, fy = self.attraction(planet)
   #         total_force_x += fx
   #         total_force_y += fy    

        self.x_vel += total_force_x / self.mass * self.TIMESTEP      
        self.y_vel += total_force_y / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP 
        self.y += self.y_vel * self.TIMESTEP 
        self.orbit.append((self.x, self.y))

def initPygame() -> pygame.surface.Surface:
    pygame.init()
    WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Planet Simulation")
    print (type(WIN))
    return WIN

def main() -> None:
    pyWin = initPygame()

    run = True
    clock = pygame.time.Clock()

    sun     = Planet("Sun",     0,                     0, 30,  YELLOW,     1.98892 * 10**30,   None)
    earth   = Planet("Earth",   -1 * Planet.AU,        0, 16,  BLUE,       5.9742 * 10**24,    sun)
    mars    = Planet("Mars",    -1.524 * Planet.AU,    0, 12,  RED,        6.39 * 10**23,      sun)
    mercury = Planet("Mercury", 0.387 * Planet.AU,     0, 8,   DARK_GREY,  3.30 * 10**23,      sun)
    venus   = Planet("Venus",   0.723 * Planet.AU,     0, 14,  WHITE,      4.8685 * 10**24,    sun)

 #   moon   = Planet("Moon",     384400 * 1000,         0, 0.2731 * 16,      GREY,         7.34767309 * 10**22,    earth)

    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)
        pyWin.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(pyWin)

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
