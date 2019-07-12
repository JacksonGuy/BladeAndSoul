#FIRE
def inferno(user,target):
    if user.fireBoi == False:
        user.health -= (user.damage - (user.damage * user.defence))
    if target.fireBoi == False:
        target.health -= (user.damage - (user.damage * target.defence))

def immolate(user,target):
    user.health = 0
    target.health = 0

def fire_boi(user,target):
    user.damage += int(user.damage * 0.25)
    user.fireBoi = True

def stolen_ability(user,target):
    if user.defence < 0.5:
        user.defence += 0.1

#WATER
def drink_water(user,target):
    if user.health != user.maxHealth:
    	user.health += user.power
    	if user.health > user.maxHealth:
        	user.health -= (user.health - user.maxHealth)

def squirt(user,target):
    target.health -= (user.damage - (user.damage * target.defence))

def drown(user,target):
    target.sleep = True

def tsunami(user,target):
    user.health -= int(user.damage - (user.damage * user.defence)*1.5)
    target.health -= int(user.damage - (user.damage * target.defence)*1.5)

#EARTH
def overgrowth(user,target):
    user.health += user.power
    if user.health > user.maxHealth:
        user.health -= (user.health - user.maxHealth)

def climate_change(user,target):
    target.poison = [True,user,4]

def rock(user,target):
    if user.defence < 0.5:
        user.defence += 0.1
    if target.defence > 0:
        target.defence -= 0.1

def rock_pillar(user,target):
    target.health -= int(user.damage - (user.damage * target.defence)*1.5)

#AIR
def deep_breath(user,target):
    user.health += user.power
    if user.health > user.maxHealth:
        user.health -= (user.health - user.maxHealth)

def blow(user,target):
    target.health -= int(user.damage - (user.damage * target.defence)*1.5)

def fart(user, target):
    target.sleep = True

def stop_breathing(user,target):
    if target.defence > 0:
        target.defence -= 0.1