import pygame, sys, random	

class vector:
    
    def __init__(self,x,y):
        self.xpos = x
        self.ypos = y 
        self.state = 0 

    def move(self):
        pass

    def display(self):
        pass


class plant:

    def __init__(self,x,y):
        self.xpos = x
        self.ypos = y 
        self.virus = []
        self.size = 10
        
    def display(self):
        pass 



# Simulation model-parameters 

wind_withd = 500
wind_height = 500
n = 15  # number of vectors (they dont day during the whole simulation)

list_vectors = []

for i in range(n):
    list_vectors.append(vector(random.randint(0,wind_withd),random.randint(0,wind_height)))



pygame.init()
screen = pygame.display.set_mode((wind_withd,wind_height))
pygame.display.set_caption('Simulation vectors and plants')
clock = pygame.time.Clock()

white=(255,255,255)
blue=(0,0,255)
green=(0,255,0)

screen.fill(white)

pygame.draw.rect(screen,green,(100,100,300,300))


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()


	
	pygame.display.update()
	clock.tick(120)