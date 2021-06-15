import pygame, sys, random	
from uuid import uuid4
import ctypes
from numpy import linalg as LA
import matplotlib.cm as cm
import matplotlib as matplotlib


random.seed(71017)

#Colours 
white=(255,255,255)
blue=(0,0,255)
green=(0,255,0)
red=(255,0,0)


# Screen parameters 
wind_withd = 500
wind_height = 500

# Model parameters 
a=0           #Ito-trend
sigma=5       #Ito- dif. coef.     
dt=1          #time-step discretization of Ito dif
mu=0        # mutation birth proba
b=1           # birth rate
d=0          # death rate (multiplier of trait (can even be a function))
c=0         # death rate parameter (multiplier considering all traits in  position x) (cuadratic rate)
beta= 1
eta=0.01
gamma=0.0
m=1 

# Initial population paramters 
n = 100   # number of vectors (they dont die during the whole simulation)
p= 0.9  #Proportion of loaded vectors at time zero


pygame.init()
screen = pygame.display.set_mode((wind_withd,wind_height))
pygame.display.set_caption('Simulation vectors and plants')
clock = pygame.time.Clock()



screen.fill(white)

#######################################
########    Recurrent functions  ######
#######################################

####### Computing rates ###############

# This function computes the total birth rate of a group of infected plants
def tot_birth_rate(list):
    r=0
    for element in list:
        r+= b*len(element.trait)
    return (1-mu)*r 

# This function computes the total birth rate with mutation of a group of infected plants
def tot_mutation_birth_rate(list):
    r=0
    for element in list:
        r+= b*len(element.trait)*m     # Uniform case
    return mu*r 

# This function computes the total death rate of a group of infected plants
def tot_death_rate(list):
    r=0
    for element in list:
        r+= d*len(element.trait) + c*len(element.trait)*len(element.trait)   # case: d(z)= d
    return r 

# This function computes the total loading rate of a group of susceptible vectors
def tot_loading_rate(list_vectors,list_plants,radius):
    r=0 
    for vector_element in list_vectors:
        neighbors= neighbour_list(vector_element,list_plants,radius)
        r+=beta*len(neighbors)
    return r 

# This function computes the total unloading rate of a group of charged vectors
def tot_unloading_rate(list_vectors,list_plants,radius):
    r=0 
    for vector_element in list_vectors:
        neighbors= neighbour_list(vector_element,list_plants,radius)
        r+=eta*len(neighbors)
    return r 

# This function computes the total death rate of viruses in a group of charged vectors
# Notice: This function seems complicated for what it does, I am just preparing it for more complex gammas
def tot_death_vector_rate(group):
    r=0
    for element in group:
        r+= gamma
    return r

# This function finds neighbors at a given radius#
def neighbour_list(element,group,radius):
    neigh=[]
    for member in group:
        if pygame.sprite.collide_rect_ratio(radius)(element,member):
            neigh.append(member)
    
    return neigh 


# This function finds an object via the objects id 
def find_object(list,identifier):
    for element in list:
        if element.id == identifier:
            return element

# This functions maps a list of traits to some color 
def coloring_traits(list):
    if len(list)==0:
        color_plant=green
    else:
        norm_value=LA.norm(list)/len(list)
        color_plant=color_map_color(norm_value)
    return color_plant

#Defining the color maping according to: https://matplotlib.org/stable/gallery/color/colormap_reference.html
def color_map_color(value, cmap_name='tab10', vmin=0, vmax=1):
    # norm = plt.Normalize(vmin, vmax)
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    cmap = cm.get_cmap(cmap_name)  # PiYG
    rgb = cmap(norm(abs(value)))[:3]  # will return rgba, we take only first 3 so we get rgb
    color = matplotlib.colors.rgb2hex(rgb)
    return color


#Clases
class vector(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.id = str(uuid4())   # This provides a unique id 
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
        else:
            print('Error: vector has virus')

    def unload(self):
        if self.trait>0:
            self.trait= 0
            self.color = (255*self.trait,0,0) 
            self.image.fill(self.color)
        else:
            print('Error: vector has no virus')

    def death(self):
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
        self.id = str(uuid4())    # This provides a unique id 
        self.xpos = x
        self.ypos = y 
        self.size = 8
        self.color = green 
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(self.color)
        self.rect =self.image.get_rect()
        self.rect.center=(self.xpos,self.ypos)
        self.trait = []  # List of viruses (inititally empty) and its traits  (in [0,1])

    def infection(self,contag_trait):
        self.trait.append(contag_trait)
        self.color = coloring_traits(self.trait)
        self.image.fill(self.color)
        

    def clonebirth(self,parent_trait):
        self.trait.append(parent_trait)
        self.color =coloring_traits(self.trait)
        self.image.fill(self.color)
        

    def mutantbirth(self,parent_trait):
        new_trait=random.random()  #Uniformly among all traits (need to change this to depend on parent_trait)
        self.trait.append(new_trait)
        self.color =coloring_traits(self.trait)
        self.image.fill(self.color)

    def death(self,parent_trait):
        self.trait.remove(parent_trait)
        self.color =coloring_traits(self.trait)
        self.image.fill(self.color)

    def unloads(self,parent_trait):
        self.trait.remove(parent_trait)
        self.color =coloring_traits(self.trait)
        self.image.fill(self.color)


vectors_group = pygame.sprite.Group()
plants_group = pygame.sprite.Group()
infected_plants_group = pygame.sprite.Group()
healthy_plants_group =pygame.sprite.Group()
charged_vectors_group = pygame.sprite.Group()
charged_vectors_id =[]   
vectors_id=[]
plants_id =[]
infected_plants_id =[]
healthy_plants_id=[]

for i in range(n):
    mosco = vector(random.randint(0,wind_withd),random.randint(0,wind_height))
    vectors_group.add(mosco)
    vectors_id.append(mosco.id)



for i in range(105,400,10):
    for j in range(105,400,10):
        planta=plant(i,j)
        plants_group.add(planta)
        healthy_plants_group.add(planta)
        plants_id.append(planta.id)
        healthy_plants_id.append(planta.id)


#Let us load some vectos with viruses

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

    

    # Computing total jump rate of current configuration
    theta_one = tot_birth_rate(infected_plants_group)
    theta_two = tot_mutation_birth_rate(infected_plants_group) +theta_one 
    theta_three = tot_death_rate(infected_plants_group) + theta_two
    theta_four = tot_loading_rate(vectors_group,infected_plants_group,10) +theta_three
    theta_five = tot_unloading_rate(charged_vectors_group,plants_group,10) +theta_four
    theta_six = tot_death_vector_rate(charged_vectors_group)+ theta_five

    # chosing the type of event #

    theta = theta_six*random.random()  #Unif [0,theta_six] random variable to decide the type of event

    if 0 <= theta  and theta <= theta_one:
            ##### Birth of a virus in a plant ########  
        if len(infected_plants_id)>0:
            target_plant_id = random.choice(infected_plants_id)
            target_plant = find_object(infected_plants_group,target_plant_id)
            
            target_plant_trait= random.choice(target_plant.trait)   #selecting new trait (for the moment doesnt make sense)

            target_plant.clonebirth(target_plant_trait)
            ### Notice that in this case we do not update any list or group ####

    elif theta_one <= theta and theta <= theta_two:
        #### Birth with mutation of a virus in a plant ####
        if len(infected_plants_id)>0:
            target_plant_id = random.choice(infected_plants_id)
            target_plant = find_object(infected_plants_group,target_plant_id)
            
            target_plant_trait= random.choice(target_plant.trait)  # Uniformly selecting parent trait (for the moment doesnt make sense)

            target_plant.mutantbirth(target_plant_trait)
            ### Notice that in this case we do not update any list or group ####

    elif theta_two <= theta and theta <= theta_three:
            ##### Death of a virus in a plant ##########
        if len(infected_plants_id)>0:
            target_plant_id=random.choice(infected_plants_id)
            target_plant = find_object(infected_plants_group,target_plant_id)
            target_plant_trait= random.choice(target_plant.trait)   #selecting new trait (for the moment doesnt make sense)
            target_plant.death(target_plant_trait)
            ### updating lists and groups ####
            if len(target_plant.trait)==0:
                infected_plants_id.remove(target_plant_id)
                infected_plants_group.remove(target_plant)
                healthy_plants_group.add(target_plant)
                healthy_plants_id.append(target_plant_id)

    elif theta_three <= theta and theta <= theta_four:
        #####  loading of virus from  plant to vector ######
        if len(vectors_id) > 0:
            target_mosco_id = random.choice(vectors_id)
            target_mosco=find_object(vectors_group,target_mosco_id)

            neighbors=neighbour_list(target_mosco,infected_plants_group,10)

            if len(neighbors)>0:
                planta=random.choice(neighbors)
                planta_target_trait=random.choice(planta.trait)
                target_mosco.load(planta_target_trait)
                planta.unloads(planta_target_trait)  
                #### updating groups and lists ######
                charged_vectors_group.add(target_mosco)
                charged_vectors_id.append(target_mosco_id)
                vectors_group.remove(target_mosco)
                vectors_id.remove(target_mosco_id)
                if len(planta.trait)==0:
                    infected_plants_group.remove(planta)
                    infected_plants_id.remove(planta.id)
                    healthy_plants_group.add(planta)
                    healthy_plants_id.append(planta.id)

    elif theta_four  <= theta and theta <= theta_five:
            #####  Unloading of virus from vector to plant ######
        if len(charged_vectors_id) > 0:
            target_mosco_id = random.choice(charged_vectors_id)
            target_mosco=find_object(charged_vectors_group,target_mosco_id)
            neighbors=neighbour_list(target_mosco,plants_group,10)

            if len(neighbors)>0:
                target_plant = random.choice(neighbors)
                target_plant.infection(target_mosco.trait)
                target_mosco.unload()
                ### updating lists and groups ####
                vectors_group.add(target_mosco)
                vectors_id.append(target_mosco_id)
                charged_vectors_group.remove(target_mosco)
                charged_vectors_id.remove(target_mosco_id)
                if not infected_plants_group.has(target_plant):
                        infected_plants_id.append(target_plant.id)
                        infected_plants_group.add(target_plant)
                        healthy_plants_id.remove(target_plant.id)
                        healthy_plants_group.remove(target_plant)

    elif theta_five <= theta and theta <= theta_six:
        # death of virus on vector #
        if len(charged_vectors_id) > 0:
            target_mosco_id = random.choice(charged_vectors_id)   #Here it makes sense to be uniform
            target_mosco = find_object(charged_vectors_group,target_mosco_id)
            target_mosco.death()
        ### updating lists and groups ####
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

