import pygame, sys, random	

#Colours 
white=(255,255,255)
blue=(0,0,255)
green=(0,255,0)
red=(255,0,0)



# Simulation model-parameters 

wind_withd = 500
wind_height = 500
a=0
sigma=1
dt=1


class vector:
    
    def __init__(self,x,y):
        self.xpos = x
        self.ypos = y 
        self.colour= red
        self.state = 0 
        self.size = 2

    def move(self):
        self.xpos = self.xpos + a*dt + sigma*random.normalvariate(0,dt)
        self.ypos = self.ypos + a*dt + sigma*random.normalvariate(0,dt)
        if self.xpos >= wind_withd:
            self.xpos=self.xpos-1
        elif self.xpos <=0:
            self.xpos= self.xpos+1

        if self.ypos >= wind_height:
            self.ypos=self.ypos-1
        elif self.ypos <=0:
            self.ypos= self.ypos+1
        
    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.xpos), int(self.ypos)), self.size, self.size)


class plant:

    def __init__(self,x,y):
        self.xpos = x
        self.ypos = y 
        self.virus = []
        self.size = 4
        self.colour = (0,150,0)
        
    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.xpos), int(self.ypos)), self.size, self.size) 




n = 150  # number of vectors (they dont die during the whole simulation)

list_vectors = []
list_plants =[]

for i in range(n):
    list_vectors.append(vector(random.randint(0,wind_withd),random.randint(0,wind_height)))



pygame.init()
screen = pygame.display.set_mode((wind_withd,wind_height))
pygame.display.set_caption('Simulation vectors and plants')
clock = pygame.time.Clock()



screen.fill(white)

pygame.draw.rect(screen,white,(100,100,300,300))

for i in range(105,400,10):
    for j in range(105,400,10):
        list_plants.append(plant(i,j))

for planta in list_plants:
    planta.display()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    for vec in list_vectors:
        vec.move()
        vec.display()
    pygame.display.update()
    clock.tick(120)

