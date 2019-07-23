from chaos import *
from abilities import *
import threading
pygame.font.init()
clock = pygame.time.Clock()

#CONSTANTS
SPEEDCONSTANT = 1

#FONTS
normalFont = pygame.font.Font(None,30)
battleFont = pygame.font.Font(None,50)
main_menu_titleFont = pygame.font.Font(None,70)

#CURSOR VARIABLES
mainMenuCursor = 200
pokemonSelectCursor = 200
interactionCursor = 480
battleCursor = [50,480] 

#OTHER VARIABLES
playerX, playerY = 0,0
battleAnimationSteps = [0,0]
aiBattleAnimationSteps = [0,0]
normalMusic = './sounds/music/Sea Shanty2.ogg'
battleMusic = './sounds/music/Halogen - U Got That-9W6AN_eQeZo.ogg'

class pokemon():
    def __init__(self,width,height):
        self.width, self.height = width,height
        self.x, self.y = 0,0
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.sprite = None
        self.speed = 3
        self.name = None

        self.pokeType = None
        self.lastUsed = None
        self.abilities = []
        self.damage = 5
        self.power = 5
        self.level = 1
        self.maxHealth = (20 * self.level) - ((20*self.level)*0.25)
        self.health = self.maxHealth
        self.xp = 0
        self.xpCap = 100
        self.defence = 0 #this is a percent
        self.poison = [False,None,0] #who applied the poison, and how many turns it has left
        self.sleep = False
        self.fireBoi = False 

    def draw_self(self):
        if self.sprite != None:
            draw_image(self.sprite,self.x,self.y)
        else:
            print("Error drawing sprite for pokemon: " + str(name))

    def update_stats(self):
        self.maxHealth = int((20 * self.level) - ((20*self.level)*0.25))
        self.health = self.maxHealth
        self.damage = int((5 * self.level) * .5)
        self.power = int((5 * self.level)*.5)

npcList = []
trainers = []
class trainer():
    def __init__(self,x,y,width,height):
        self.x, self.y, self.width, self.height = x,y,width,height
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.sprite = None
        self.name = None
        
        self.pokemon = []
        self.selectedPokemon = None

        self.inventory = []
        self.money = 0

        self.pokeballCount = 5
        self.healthPotCount = 0

    def draw_self(self):
        if self.sprite != None:
            draw_image(self.sprite,self.x,self.y)
        else:
            print("Error drawing sprite for " + str(name))

    def draw_selected_pokemon(self):
        if self.selectedPokemon != None:
            self.selectedPokemon.x, self.selectedPokemon.y = self.x - self.width/2, self.y
            self.selectedPokemon.draw_self()

class item():
    def __init__(self,cost,name):
        self.cost = cost
        self.name = name
        
        #stuff for drawing item, not required
        self.sprite = None
        self.x, self.y = None, None

    def draw_self(self):
        draw_image(self.image,self.x,self.y)

#OTHER FUNCTIONS

def ai_action(user,target):
    #aiBattleAnimationSteps = [0,0]
    if user.sleep == False:
        x = random.randint(0,len(user.abilities)-1)
        user.abilities[x](user,target)
        assign_lastUsed(user,x)
        uncleRicky.selectedPokemon.lastUsed = None
        aiBattleAnimationSteps[0] = 1

    #apply/update poison
    if user.poison[0] == True:
        user.health -= user.poison[1].damage * 0.25
        user.poison[2] -= 1
        if user.poison[2] == 0:
            user.poison[0], user.poison[1] = None,None
    if user.sleep == True:
        user.sleep = False

def assign_lastUsed(p,n):
    if p.type == 'fire':
        if n == 0:
            p.lastUsed = 'Inferno'
        if n == 1:
            p.lastUsed = 'Self Immolate'
        if n == 2:
            p.lastUsed = 'Fire Boi'
        if n == 3:
            p.lastUsed = 'Stolen Ability'

    if p.type == 'water':
        if n == 0:
            p.lastUsed = 'Drink Water'
        if n == 1:
            p.lastUsed = 'Squirt'
        if n == 2:
            p.lastUsed = 'Drown'
        if n == 3:
            p.lastUsed = 'Tsunami'

    if p.type == 'earth':
        if n == 0:
            p.lastUsed = 'Overgrowth'
        if n == 1:
            p.lastUsed = 'Climate Change'
        if n == 2:
            p.lastUsed = 'Rock'
        if n == 3:
            p.lastUsed = 'Rock Pillar'

    if p.type == 'air':
        if n == 0:
            p.lastUsed = 'Deep Breath'
        if n == 1:
            p.lastUsed = 'Blow'
        if n == 2:
            p.lastUsed = 'Fart'
        if n == 3:
            p.lastUsed = 'Stop Breathing'

#TRAINERS
uncleRicky = trainer(W_width/2,W_height/2,100,100)
uncleRicky.sprite = load_image("./images/uncleRicky.png")
uncleRicky.sprite = pygame.transform.scale(uncleRicky.sprite, (100,100))
uncleRicky.name = "Uncle Ricky"
uncleRicky.selectedNPC = None

worldTrainer = trainer(0,0,0,0)
worldTrainer.name = "world"

trainer1 = trainer(500,200,100,100)
trainer1.sprite = load_image("./images/trainer1.png")
trainer1.sprite = pygame.transform.scale(trainer1.sprite, (100,100))
trainer1.name = "Some Bitch"
trainers.append(trainer1)
npcList.append(trainer1)
trainer1.npcMessages = [
    "Do you want to fight me cunt?"
]
trainer1.npcMessageNum = 0

trainer2 = trainer(2000,200,100,100)
trainer2.sprite = load_image("./images/trainer2.png")
trainer2.sprite = pygame.transform.scale(trainer2.sprite, (100,100))
trainer2.name = "Tall Fuck"
trainers.append(trainer2)
npcList.append(trainer2)
trainer2.npcMessages = [
    "Do you want to fight me cunt?"
]
trainer2.npcMessageNum = 0

trainer3 = trainer(500,2000,100,100)
trainer3.sprite = load_image("./images/trainer3.png")
trainer3.sprite = pygame.transform.scale(trainer3.sprite, (100,100))
trainer3.name = "Some Nerd"
trainers.append(trainer3)
npcList.append(trainer3)
trainer3.npcMessages = [
    "Do you want to fight me cunt?"
]
trainer3.npcMessageNum = 0

trainer4 = trainer(2000,2000,100,100)
trainer4.sprite = load_image("./images/trainer4.png")
trainer4.sprite = pygame.transform.scale(trainer4.sprite, (100,100))
trainer4.name = "Some Thot"
trainers.append(trainer4)
npcList.append(trainer4)
trainer4.npcMessages = [
    "Do you want to fight me cunt?"
]
trainer4.npcMessageNum = 0

#POKEMON
def generate_pokemon(x):
    if x == 0:
        hotpi = pokemon(50,50)
        hotpi.sprite = load_image("./images/hotpi.png")
        hotpi.sprite = pygame.transform.scale(hotpi.sprite, (100,100))
        hotpi.name = "Hotpi"
        hotpi.type = 'fire'
        hotpi.abilities = [inferno,immolate,fire_boi,stolen_ability]
        return(hotpi)
    if x == 1:
        peanis = pokemon(50,50)
        peanis.sprite = load_image("./images/peanis.png")
        peanis.sprite = pygame.transform.scale(peanis.sprite, (100,100))
        peanis.name = "Peanis"
        peanis.type = 'water'
        peanis.abilities = [drink_water,squirt,drown,tsunami]
        return(peanis)
    if x == 2:
        flampod = pokemon(50,50)
        flampod.sprite = load_image("./images/Flampod.PNG")
        flampod.sprite = pygame.transform.scale(flampod.sprite, (100,100))
        flampod.name = "Flampod"
        flampod.type = 'air'
        flampod.abilities = [deep_breath,blow,fart,stop_breathing]
        return(flampod)
    if x == 3:
        pourpiss = pokemon(50,50)
        pourpiss.sprite = load_image("./images/pourpiss.png")
        pourpiss.sprite = pygame.transform.scale(pourpiss.sprite, (100,100))
        pourpiss.name = "Pourpiss"
        pourpiss.type = 'fire'
        pourpiss.abilities = [inferno,immolate,fire_boi,stolen_ability]
        return(pourpiss)
    if x == 4:
        thorbon = pokemon(50,50)
        thorbon.sprite = load_image("./images/thorbon.png")
        thorbon.sprite = pygame.transform.scale(thorbon.sprite,(100,100))
        thorbon.name = "Thorbon"
        thorbon.type = 'earth'
        thorbon.abilities = [overgrowth,climate_change,rock,rock_pillar]
        return(thorbon)

#OTHER
background = load_image("./images/grassBackground.png")
background = pygame.transform.scale(background,(800,600))

healerBoi = Object(400,50,50,50)
healerBoi.sprite = load_image("./images/healerBoi.png")
healerBoi.sprite = pygame.transform.scale(healerBoi.sprite,(50,50))
healerBoi.name = "Daddy"
npcList.append(healerBoi)
healerBoi.npcMessages = [
    "Do ya need some heals ;)",
    "There ya go, all your pokemon are very healthy ;)))))"
]
healerBoi.npcMessageNum = 0

shopBoi = Object(800,50,50,50)
shopBoi.sprite = load_image("./images/shopBoi.png")
shopBoi.sprite = pygame.transform.scale(shopBoi.sprite,(50,50))
shopBoi.name = "Baldy"
npcList.append(shopBoi)
shopBoi.npcMessages = [
    "What can I get for ya?"
]
shopBoi.npcMessageNum = 0

#Give trainers their pokemon
trainer1.pokemon.append(generate_pokemon(1))
trainer1.selectedPokemon = trainer1.pokemon[0]
trainer1.selectedPokemon.level = 25
trainer1.selectedPokemon.update_stats()

trainer2.pokemon.append(generate_pokemon(2))
trainer2.selectedPokemon = trainer2.pokemon[0]
trainer2.selectedPokemon.level = 25
trainer2.selectedPokemon.update_stats()

trainer3.pokemon.append(generate_pokemon(3))
trainer3.selectedPokemon = trainer3.pokemon[0]
trainer3.selectedPokemon.level = 25
trainer3.selectedPokemon.update_stats()

trainer4.pokemon.append(generate_pokemon(4))
trainer4.selectedPokemon = trainer4.pokemon[0]
trainer4.selectedPokemon.level = 25
trainer4.selectedPokemon.update_stats()