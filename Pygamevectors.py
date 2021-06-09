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

n = 5000 # number of vectors (they dont die during the whole simulation)

pygame.init()
screen = pygame.display.set_mode((wind_withd,wind_height))
pygame.display.set_caption('Simulation vectors and plants')
clock = pygame.time.Clock()



screen.fill(white)


class vector(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.size = 4
        self.xpos = x
        self.ypos = y 
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(red)
        self.rect =self.image.get_rect()
        self.rect.center=(self.xpos,self.ypos)
        self.state = 0 
        

    def update(self):
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
        self.rect.center=(self.xpos,self.ypos)


class plant(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.xpos = x
        self.ypos = y 
        self.image = pygame.Surface([8, 8])
        self.image.fill(green)
        self.rect =self.image.get_rect()
        self.rect.center=(self.xpos,self.ypos)
        self.state = 0 




vectors_group = pygame.sprite.Group()
plants_group = pygame.sprite.Group()

for i in range(n):
    vectors_group.add(vector(random.randint(0,wind_withd),random.randint(0,wind_height)))


#pygame.draw.rect(screen,white,(100,100,300,300))


for i in range(105,400,10):
    for j in range(105,400,10):
        plants_group.add(plant(i,j))






while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(white)
    plants_group.draw(screen)
    vectors_group.update()
    vectors_group.draw(screen)
    pygame.display.update()
    clock.tick(120)

