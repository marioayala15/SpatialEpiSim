import pygame, sys, random	
from uuid import uuid4
import ctypes

#Colours 
white=(255,255,255)
blue=(0,0,255)
green=(0,255,0)
red=(255,0,0)


# Model-parameters 

wind_withd = 500
wind_height = 500
a=0
sigma=5
dt=1

n = 1000 # number of vectors (they dont die during the whole simulation)

pygame.init()
screen = pygame.display.set_mode((wind_withd,wind_height))
pygame.display.set_caption('Simulation vectors and plants')
clock = pygame.time.Clock()



screen.fill(white)

########    Recurrent functions  ######

# This function finds an object via the objects id 
def find_object(list,identifier):
    for element in list:
        if element.id == identifier:
            return element


#Clases
class vector(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.id = str(uuid4())
        self.size = 4
        self.xpos = x
        self.ypos = y 
        self.trait = 0   #  Taking values in [0,1] ( initially not carrying viruses) 
        self.color = (255*self.trait,0,0)    #Black is healthy,  255 red is infected (in betweeen traits)
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(self.color)
        self.rect =self.image.get_rect()
        self.rect.center=(self.xpos,self.ypos)
         
    def load(self,contag_trait):
        if self.trait==0:
            self.trait= contag_trait 
            self.color = (255*self.trait,0,0) 
            self.image.fill(self.color)

    def unload(self):
        if self.trait>0:
            self.trait= 0
            self.color = (255*self.trait,0,0) 
            self.image.fill(self.color)


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
        self.id = str(uuid4())
        self.xpos = x
        self.ypos = y 
        self.size = 2
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(green)
        self.rect =self.image.get_rect()
        self.rect.center=(self.xpos,self.ypos)
        self.trait = []  # List of viruses (inititally empty) and its traits  (in [0,1])

    def infection(self,contag_trait):
        self.size += 2
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(green)
        self.trait.append(contag_trait)

    def clonebirth(self,parent_trait):
        self.size+=2
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(green)
        self.trait.append(parent_trait)




vectors_group = pygame.sprite.Group()
plants_group = pygame.sprite.Group()
infected_plants_group = pygame.sprite.Group()
vectors_id=[]
plants_id =[]
infected_plants_id =[]

for i in range(n):
    mosco = vector(random.randint(0,wind_withd),random.randint(0,wind_height))
    vectors_group.add(mosco)
    vectors_id.append(mosco.id)



for i in range(105,400,10):
    for j in range(105,400,10):
        planta=plant(i,j)
        plants_group.add(planta)
        plants_id.append(planta.id)


#Let us load some vectos with viruses
p= 0.4  #Proportion of loaded vectors at time zero
charged_vectors_group = pygame.sprite.Group()
charged_vectors_id =[]   #Empty list with ids

for mosco in vectors_group:
    unif= random.random()
    new_trait= random.random()  #we pick the new trait at random
    if unif <= p:
        mosco.load(new_trait)
        charged_vectors_group.add(mosco)
        charged_vectors_id.append(mosco.id)
        vectors_group.remove(mosco)
        vectors_id.remove(mosco.id)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    theta = random.random  #Unif [0,1] random variable to decide the type of event

    ###############################
    ####### Types of events #######
    ###############################

    ##### Birth of a virus in a plant ########  (BETA version, is not following the models logic)
    if len(infected_plants_id)>0:
        target_plant_id=random.choice(infected_plants_id)

        target_plant = find_object(infected_plants_group,target_plant_id)
        target_plant_trait= random.choice(target_plant.trait)   #selecting new trait (for the moment doesnt make sense)

        target_plant.clonebirth(target_plant_trait)

    #####  Unloading of virus from vector to plant ######
    if len(charged_vectors_id) > 0:
        target_mosco_id = random.choice(charged_vectors_id)

        target_mosco=find_object(charged_vectors_group,target_mosco_id)

        for planta in plants_group:
            if pygame.sprite.collide_rect_ratio(1)(target_mosco, planta):
                planta.infection(target_mosco.trait)
                

                infected_plants_id.append(planta)

                infected_plants_group.add(planta)
                target_mosco.unload()
                vectors_group.add(target_mosco)
                vectors_id.append(target_mosco_id)
                charged_vectors_group.remove(target_mosco)
                charged_vectors_id.remove(target_mosco_id)

    screen.fill(white)
    plants_group.draw(screen)
    vectors_group.update()
    vectors_group.draw(screen)
    charged_vectors_group.update()
    charged_vectors_group.draw(screen)
    pygame.display.update()
    clock.tick(60)

