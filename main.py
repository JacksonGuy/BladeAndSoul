from header1 import *

pygame.mixer.init()

def random_encounter(a):
    global displayBattleScreen
    global displayGame
    x = random.randint(0,a)
    if x == 0:
        #create random pokemon
        num = random.randint(0,4)
        randomPokemon = generate_pokemon(num)
        randomPokemon.level = uncleRicky.selectedPokemon.level
        randomPokemon.update_stats()
        worldTrainer.pokemon.append(randomPokemon)
        worldTrainer.selectedPokemon = worldTrainer.pokemon[0]
        uncleRicky.selectedNPC = worldTrainer

        displayBattleScreen = True
        displayGame = False
        uncleRicky.selectedPokemon.x, uncleRicky.selectedPokemon.y = 0,300
        uncleRicky.selectedNPC.selectedPokemon.x, uncleRicky.selectedNPC.selectedPokemon.y = 500,100
        battleCursor = [50,480]
        pygame.mixer.music.load(battleMusic)
        pygame.mixer.music.play(-1)

# DISPLAY VARIABLES
displayMainMenu = True
displayPokemonSelect = False
displayGame = False
displayPokemonStats = True
displayInventory = False
displayBattleScreen = False
displayNPCInteraction = False
displayTrainerInteraction = False
displayFightMenu = False
displayFightPokemonMenu = False
displayFightBagMenu = False

while True:
    #EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if displayPokemonStats == False:
                    displayPokemonStats = True
                else:
                    displayPokemonStats = False

            if event.key == pygame.K_i:
                if displayInventory == False:
                    displayInventory = True
                else:
                    displayInventory = False

            if event.key == pygame.K_SPACE:
                if displayMainMenu:
                    if mainMenuCursor == 200:
                        displayPokemonSelect = True
                        displayMainMenu = False
                        
                if displayNPCInteraction:
                    if uncleRicky.selectedNPC.name == "Daddy":
                        if uncleRicky.selectedNPC.npcMessageNum == 0:
                            if interactionCursor == 480:
                                uncleRicky.selectedNPC.npcMessageNum = 1
                                for p in uncleRicky.pokemon: #heals players pokemon
                                    p.health = p.maxHealth
                                for t in trainers: #and all the trainers pokemon
                                    for p in t.pokemon:
                                        p.health = p.maxHealth
                            else:
                                displayNPCInteraction = False
                        else:
                            if interactionCursor == 480 or interactionCursor == 510:
                                displayNPCInteraction = False
                                uncleRicky.selectedNPC.npcMessageNum = 0

                    if uncleRicky.selectedNPC.name == "Baldy":
                        if uncleRicky.selectedNPC.npcMessageNum == 0:
                            if interactionCursor == 480:
                                if uncleRicky.money >= 10:
                                    #create pokeball object
                                    ball = item(10,"Pokeball")
                                    ball.sprite = load_image("./pokeball.png")
                                    ball.sprite = pygame.transform.scale(ball.sprite,(30,30))

                                    #add pokeball to player inventory
                                    uncleRicky.pokeballCount += 1

                                    #subtract currency
                                    uncleRicky.money -= 10

                            if interactionCursor == 510:
                                if uncleRicky.money >= 10:
                                    #create potion item
                                    hpPot = item(10,"Health Potion")
                                    hpPot.sprite = load_image("./healthPot.png")
                                    hpPot.sprite = pygame.transform.scale(ball.sprite,(30,30))

                                    #add health potion to player inventory
                                    uncleRicky.healthPotCount += 1

                                    #subtract currency
                                    uncleRicky.money -= 10

                if displayBattleScreen:
                    if displayFightMenu:
                        if uncleRicky.selectedPokemon.health > 0 and uncleRicky.selectedNPC.selectedPokemon.health > 0:
                            if uncleRicky.selectedPokemon.sleep == False:
                                if battleCursor[0] == 50 and battleCursor[1] == 480:
                                    uncleRicky.selectedPokemon.abilities[0](uncleRicky.selectedPokemon, uncleRicky.selectedNPC.selectedPokemon)
                                    assign_lastUsed(uncleRicky.selectedPokemon,0)
                                
                                if battleCursor[0] == 50 and battleCursor[1] == 530:
                                    uncleRicky.selectedPokemon.abilities[1](uncleRicky.selectedPokemon, uncleRicky.selectedNPC.selectedPokemon)
                                    assign_lastUsed(uncleRicky.selectedPokemon,1)
                                
                                if battleCursor[0] == 350 and battleCursor[1] == 480:
                                    uncleRicky.selectedPokemon.abilities[2](uncleRicky.selectedPokemon, uncleRicky.selectedNPC.selectedPokemon)
                                    assign_lastUsed(uncleRicky.selectedPokemon,2)
                                
                                if battleCursor[0] == 350 and battleCursor[1] == 530:
                                    uncleRicky.selectedPokemon.abilities[3](uncleRicky.selectedPokemon, uncleRicky.selectedNPC.selectedPokemon)
                                    assign_lastUsed(uncleRicky.selectedPokemon,3)

                                battleAnimationSteps[0] = 1

                                uncleRicky.selectedNPC.selectedPokemon.lastUsed = None
                            
                            #apply/update poison
                            if uncleRicky.selectedPokemon.poison[0] == True:
                                uncleRicky.selectedPokemon.health -= uncleRicky.selectedPokemon.poison[1].damage * 0.25
                                uncleRicky.selectedPokemon.poison[2] -= 1
                                if uncleRicky.selectedPokemon.poison[2] == 0:
                                    uncleRicky.selectedPokemon.poison[1], uncleRicky.selectedPokemon.poison[0] = None,None
                            
                            if uncleRicky.selectedPokemon.sleep == True:
                                uncleRicky.selectedPokemon.sleep = False
                        
                            ai_action(uncleRicky.selectedNPC.selectedPokemon,uncleRicky.selectedPokemon)
                        
                        else:
                            displayFightMenu = False
                            displayBattleScreen = False
                            displayGame = True
                            pygame.mixer.music.load(normalMusic)
                            pygame.mixer.music.play(-1)

                    if displayFightBagMenu:
                        if battleCursor[0] == 50 and battleCursor[1] == 480:
                            if len(uncleRicky.pokemon) < 5:
                                if uncleRicky.pokeballCount >= 1:
                                    if uncleRicky.selectedNPC.name == 'world':
                                        #1/3 chance that you capture the pokemon 
                                        x = random.randint(0,3)
                                        if x == 0: #good job, you caught the pokemon
                                            uncleRicky.pokemon.append(uncleRicky.selectedNPC.selectedPokemon)
                                            worldTrainer.pokemon.remove(worldTrainer.selectedPokemon)
                                            #worldTrainer.selectedPokemon = None
                                            uncleRicky.pokeballCount -= 1
                                            displayFightBagMenu = False
                                            displayBattleScreen = False
                                            displayGame = True
                                            pygame.mixer.music.load(normalMusic)
                                            pygame.mixer.music.play(-1)
                                        else:
                                            pass

                        if battleCursor[0] == 50 and battleCursor[1] == 530:
                            if uncleRicky.healthPotCount >= 1:
                                uncleRicky.selectedPokemon.health += 10
                                if uncleRicky.selectedPokemon.health > uncleRicky.selectedPokemon.maxHealth:
                                    uncleRicky.selectedPokemon.health -= (uncleRicky.selectedPokemon.health - uncleRicky.selectedPokemon.maxHealth)
                                uncleRicky.healthPotCount -= 1

                    if displayFightPokemonMenu:
                        if battleCursor[0] == 50 and battleCursor[1] == 480:
                            uncleRicky.pokemon[0], uncleRicky.pokemon[1] = uncleRicky.pokemon[1], uncleRicky.pokemon[0]
                        if battleCursor[0] == 50 and battleCursor[1] == 530:
                            uncleRicky.pokemon[0], uncleRicky.pokemon[2] = uncleRicky.pokemon[2], uncleRicky.pokemon[0]
                        if battleCursor[0] == 350 and battleCursor[1] == 480:
                            uncleRicky.pokemon[0], uncleRicky.pokemon[3] = uncleRicky.pokemon[3], uncleRicky.pokemon[0]
                        if battleCursor[0] == 350 and battleCursor[1] == 530:
                            uncleRicky.pokemon[0], uncleRicky.pokemon[4] = uncleRicky.pokemon[4], uncleRicky.pokemon[0]
                        uncleRicky.selectedPokemon = uncleRicky.pokemon[0]
                        uncleRicky.selectedPokemon.x, uncleRicky.selectedPokemon.y = 0,300 

                    if displayFightMenu == False and displayFightBagMenu == False and displayFightPokemonMenu == False:
                        if battleCursor[0] == 50 and battleCursor[1] == 480:
                            if displayFightMenu == False:
                                displayFightMenu = True
                        if battleCursor[0] == 50 and battleCursor[1] == 530:
                            if displayFightPokemonMenu == False:
                                displayFightPokemonMenu = True
                        if battleCursor[0] == 350 and battleCursor[1] == 480:
                            if displayFightBagMenu == False:
                                displayFightBagMenu = True
                                battleCursor[0] = 50
                        if battleCursor[0] == 350 and battleCursor[1] == 530:
                            displayBattleScreen = False
                            displayGame = True
                            pygame.mixer.music.load(normalMusic)
                            pygame.mixer.music.play(-1)
                            if uncleRicky.selectedNPC.name == 'world':
                                worldTrainer.pokemon.remove(worldTrainer.selectedPokemon)
                                #worldTrainer.selectedPokemon = None
                
                if displayTrainerInteraction:
                    if interactionCursor == 480:
                        #start pokemon battle
                        displayBattleScreen = True
                        displayGame = False
                        displayTrainerInteraction = False
                        battleCursor = [50,480]
                        battleAnimationSteps = [0,0]
                        #set pokemon starting positions
                        uncleRicky.selectedPokemon.x, uncleRicky.selectedPokemon.y = 0,300
                        uncleRicky.selectedNPC.selectedPokemon.x, uncleRicky.selectedNPC.selectedPokemon.y = 500,100 
                        pygame.mixer.music.load(battleMusic)
                        pygame.mixer.music.play(-1)
                    else:
                        displayTrainerInteraction = False
                    
            if event.key == pygame.K_e:
                #find closest npc/trainer
                a = None
                for t in npcList:
                    if a == None:
                        a = t
                    else:
                        if find_distance(uncleRicky.x,uncleRicky.y,t.x,t.y) < find_distance(uncleRicky.x,uncleRicky.y,a.x,a.y):
                            a = t
                uncleRicky.selectedNPC = a
                #start interaction with selected NPC/trainer
                if find_distance(uncleRicky.x,uncleRicky.y,uncleRicky.selectedNPC.x,uncleRicky.selectedNPC.y) < 250:
                    if uncleRicky.selectedNPC in trainers:
                        displayTrainerInteraction = True
                    else:
                        displayNPCInteraction = True
            
            if event.key == pygame.K_ESCAPE:
                if displayGame:
                    displayTrainerInteraction = False
                    displayNPCInteraction = False
                if displayBattleScreen:
                    displayFightMenu = False
                    displayFightPokemonMenu = False
                    displayFightBagMenu = False
            
            if event.key == UP:
                if displayMainMenu:
                    if mainMenuCursor > 200:
                        mainMenuCursor -= 30
                if displayPokemonSelect:
                    if pokemonSelectCursor > 200:
                        pokemonSelectCursor -= 100
                    else:
                        pokemonSelectCursor = 400
                if displayTrainerInteraction or displayNPCInteraction:
                    if interactionCursor > 480:
                        interactionCursor -= 30
                    else:
                        interactionCursor = 510
                if displayBattleScreen:
                    if battleCursor[1] > 480:
                        battleCursor[1] -= 50
                    else:
                        battleCursor[1] = 530
            
            if event.key == DOWN:
                if displayMainMenu:
                    #TODO: add more stuff to main menu
                    pass
                if displayPokemonSelect:
                    if pokemonSelectCursor < 400:
                        pokemonSelectCursor += 100
                    else:
                        pokemonSelectCursor = 200
                if displayTrainerInteraction or displayNPCInteraction:
                    if interactionCursor < 510:
                        interactionCursor += 30
                    else:
                        interactionCursor = 480
                if displayBattleScreen:
                    if battleCursor[1] < 530:
                        battleCursor[1] += 50
                    else:
                        battleCursor[1] = 480
            if event.key == RIGHT:
                if displayBattleScreen and displayFightBagMenu == False:
                    if battleCursor[0] < 350:
                        battleCursor[0] += 300
                    else:
                        battleCursor[0] = 50
            if event.key == LEFT:
                if displayBattleScreen and displayFightBagMenu == False:
                    if battleCursor[0] > 50:
                        battleCursor[0] -= 300
                    else:
                        battleCursor[0] = 350
    #MAIN MENU
    if displayMainMenu:
        screen.fill(black)
        draw_rect(10,mainMenuCursor,20,20,orange)
        draw_text("Pokemon Blade and Soul",30,100,white,main_menu_titleFont)
        draw_text("Play",50,200,white,normalFont)
        mainMenuPic = load_image("./uncleRicky.png")
        mainMenuPic = pygame.transform.scale(mainMenuPic, (400,300))
        draw_image(mainMenuPic,300,200)
        pygame.display.update()

    #POKEMON SELECT
    if displayPokemonSelect:
        screen.fill(black)
        draw_rect(50,pokemonSelectCursor,20,20,orange)
        
        #draw name
        draw_text("Choose your starting Pokemon", 100,100,white,normalFont)
        draw_text("Hotpi (Fire type)", 100,200,white,normalFont)
        draw_text("Peanis (Water Type)",100,300,white,normalFont)
        draw_text("Flampod (Air Type)",100,400,white,normalFont)
        
        #load pictures
        if pokemonSelectCursor == 200:
            pic = load_image("./hotpi.png")
            pic = pygame.transform.scale(pic, (150,150))
        if pokemonSelectCursor == 300:
            pic = load_image("./peanis.png")
            pic = pygame.transform.scale(pic, (150,150))
        if pokemonSelectCursor == 400:
            pic = load_image("./Flampod.PNG")
            pic = pygame.transform.scale(pic, (150,150))

        #draw picture
        draw_image(pic,500,200)

        pressed = get_input()
        if pressed[pygame.K_SPACE] and (pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]):
            if pokemonSelectCursor == 200:
                uncleRicky.pokemon.append(generate_pokemon(0))
                uncleRicky.selectedPokemon = uncleRicky.pokemon[0]
            if pokemonSelectCursor == 300:
                uncleRicky.pokemon.append(generate_pokemon(1))
                uncleRicky.selectedPokemon = uncleRicky.pokemon[0]
            if pokemonSelectCursor == 400:
                uncleRicky.pokemon.append(generate_pokemon(2))
                uncleRicky.selectedPokemon = uncleRicky.pokemon[0]
            
            displayPokemonSelect = False
            displayGame = True
            pygame.mixer.music.load(normalMusic)
            pygame.mixer.music.play(-1)

        pygame.display.update()

    #POKEMON BATTLE
    if displayBattleScreen:
        screen.fill(black)
        #draw pokemon
        uncleRicky.selectedPokemon.draw_self()
        uncleRicky.selectedNPC.selectedPokemon.draw_self()
        
        draw_rect(0,450,800,150,green)
        
        #draw pokemons health and name
        draw_text(str(uncleRicky.selectedPokemon.name),650,390,white,normalFont)
        draw_text("HP: " + str(int(uncleRicky.selectedPokemon.health)) + "/" + str(int(uncleRicky.selectedPokemon.maxHealth)),650,420,white,normalFont)
        draw_text(str(uncleRicky.selectedNPC.selectedPokemon.name),50,20,white,normalFont)
        draw_text("HP: " + str(int(uncleRicky.selectedNPC.selectedPokemon.health)) + "/" + str(int(uncleRicky.selectedNPC.selectedPokemon.maxHealth)),50,50,white,normalFont)
        
        if displayFightMenu:
            #draw selected pokemon's attacks
            if uncleRicky.selectedPokemon.type == 'fire':
                draw_text("Inferno",100,480,black,battleFont)
                draw_text("Self Immolate",100,530,black,battleFont)
                draw_text("Fire Boi",400,480,black,battleFont)
                draw_text("Stolen Ability",400,530,black,battleFont)
            
            if uncleRicky.selectedPokemon.type == 'water':
                draw_text("Drink Water",100,480,black,battleFont)
                draw_text("Squirt",100,530,black,battleFont)
                draw_text("Drown",400,480,black,battleFont)
                draw_text("Tsunami",400,530,black,battleFont)
            
            if uncleRicky.selectedPokemon.type == 'earth':
                draw_text("Overgrowth",100,480,black,battleFont)
                draw_text("Climate Change",100,530,black,battleFont)
                draw_text("Rock",400,480,black,battleFont)
                draw_text("Rock Pillar",400,530,black,battleFont)
            
            if uncleRicky.selectedPokemon.type == 'air':
                draw_text("Deep Breath",100,480,black,battleFont)
                draw_text("Blow",100,530,black,battleFont)
                draw_text("Fart",400,480,black,battleFont)
                draw_text("Stop Breathing",400,530,black,battleFont)
        
        elif displayFightPokemonMenu:
            for x in range(len(uncleRicky.pokemon)):
                if x == 1:
                    draw_text(str(uncleRicky.pokemon[1].name),100,480,black,battleFont)
                if x == 2:
                    draw_text(str(uncleRicky.pokemon[2].name),100,530,black,battleFont)
                if x == 3:
                    draw_text(str(uncleRicky.pokemon[3].name),350,480,black,battleFont)
                if x == 4:
                    draw_text(str(uncleRicky.pokemon[4].name),350,530,black,battleFont)
            
        elif displayFightBagMenu:
            draw_text("Pokeball (" + str(uncleRicky.pokeballCount) + ")",100,480,black,battleFont)
            draw_text("Health Potion (" + str(uncleRicky.healthPotCount) + ")",100,530,black,battleFont)
        
        else:
            #battle options
            draw_text("Fight",100,480,black,battleFont)
            draw_text("Pokemon",100,530,black,battleFont)
            draw_text("Bag",400,480,black,battleFont)
            draw_text("Run",400,530,black,battleFont)
        #draw cursor
        draw_rect(battleCursor[0],battleCursor[1],30,30,orange)
        
        #draw last action
        if uncleRicky.selectedNPC.selectedPokemon.lastUsed == None and uncleRicky.selectedPokemon.lastUsed != None:
            draw_text(str(uncleRicky.selectedPokemon.name) + " used " + uncleRicky.selectedPokemon.lastUsed,50,430,white,normalFont)
        if uncleRicky.selectedPokemon.lastUsed == None and uncleRicky.selectedNPC.selectedPokemon.lastUsed != None:
            draw_text(str(uncleRicky.selectedNPC.selectedPokemon.name) + " used " + uncleRicky.selectedNPC.selectedPokemon.lastUsed,50,430,white,normalFont)
            #do ai animation
            if battleAnimationSteps[0] == 0 and battleAnimationSteps[1] == 0:
                if aiBattleAnimationSteps[0] == 1 and aiBattleAnimationSteps[1] == 0:
                    move(uncleRicky.selectedNPC.selectedPokemon,20,280)
                if aiBattleAnimationSteps[1] == 1 and aiBattleAnimationSteps[0] == 0:
                    move(uncleRicky.selectedNPC.selectedPokemon,500,100)
                if uncleRicky.selectedNPC.selectedPokemon.x < 30 and uncleRicky.selectedNPC.selectedPokemon.y > 270:
                    aiBattleAnimationSteps[1] = 1
                    aiBattleAnimationSteps[0] = 0
                if uncleRicky.selectedNPC.selectedPokemon.x > 480 and uncleRicky.selectedNPC.selectedPokemon.y > 80 and aiBattleAnimationSteps[1] == 1:
                    aiBattleAnimationSteps[0], aiBattleAnimationSteps[1] = 0,0
        
        else:
            draw_text("",50,430,white,normalFont)

        #player won the fight
        if uncleRicky.selectedNPC.selectedPokemon.health <= 0:
            #gain xp + money
            uncleRicky.selectedPokemon.xp += (uncleRicky.selectedNPC.selectedPokemon.level * 10)
            uncleRicky.money += 1
            #check for level up
            if uncleRicky.selectedPokemon.xp >= uncleRicky.selectedPokemon.xpCap:
                uncleRicky.selectedPokemon.level += 1
                uncleRicky.selectedPokemon.xp = 0
                uncleRicky.selectedPokemon.xpCap = 100 + (uncleRicky.selectedPokemon.xpCap*.5)
                uncleRicky.selectedPokemon.update_stats()
            if uncleRicky.selectedNPC.name == 'world':
                worldTrainer.pokemon.remove(worldTrainer.selectedPokemon)
            if uncleRicky.selectedPokemon.type == 'fire':
                uncleRicky.selectedPokemon.fireBoi = False
            displayFightMenu = False
            displayBattleScreen = False
            displayGame = True
            pygame.mixer.music.load(normalMusic)
            pygame.mixer.music.play(-1)

        pressed = get_input()

        #player animation
        if battleAnimationSteps[0] == 1 and battleAnimationSteps[1] == 0:
            move(uncleRicky.selectedPokemon,450,80)
        if battleAnimationSteps[1] == 1 and battleAnimationSteps[0] == 0:
            move(uncleRicky.selectedPokemon,0,300)
        if uncleRicky.selectedPokemon.x > 440 and uncleRicky.selectedPokemon.y > 75:
            battleAnimationSteps[1] = 1
            battleAnimationSteps[0] = 0
        if uncleRicky.selectedPokemon.x < 10 and uncleRicky.selectedPokemon.y > 280 and battleAnimationSteps[1] == 1:
            battleAnimationSteps[0], battleAnimationSteps[1] = 0,0
        
        pygame.display.update()
    
    #DISPLAY GAME
    elif displayGame:
        if uncleRicky.selectedPokemon.width != 50:
            uncleRicky.selectedPokemon.width = 50
            uncleRicky.selectedPokemon.sprite = pygame.transform.scale(uncleRicky.selectedPokemon.sprite,(50,50))

        pressed = get_input()
        mousePos = get_mouse_position()
        mouse = get_mouse_input()
        if displayNPCInteraction == False and displayTrainerInteraction == False:
            if pressed[pygame.K_w]:
                for thing in npcList:
                    thing.y += SPEEDCONSTANT
                playerY -= SPEEDCONSTANT
                random_encounter(5000)
            if pressed[pygame.K_s]:
                for thing in npcList:
                    thing.y -= SPEEDCONSTANT
                playerY += SPEEDCONSTANT
                random_encounter(5000)
            if pressed[pygame.K_a]:
                for thing in npcList:
                    thing.x += SPEEDCONSTANT
                playerX -= SPEEDCONSTANT
                random_encounter(5000)
            if pressed[pygame.K_d]:
                for thing in npcList:
                    thing.x -= SPEEDCONSTANT
                playerX += SPEEDCONSTANT
                random_encounter(5000)

            if pressed[pygame.K_f] and pressed[pygame.K_LSHIFT]:
                random_encounter(0)

        screen.fill(black)
        #DRAW NPCS
        healerBoi.draw_self()
        shopBoi.draw_self()
        uncleRicky.draw_self()
        trainer1.draw_self()
        trainer2.draw_self()
        trainer3.draw_self()
        trainer4.draw_self()
        
        #NPC INTERACTION
        if displayTrainerInteraction:
            draw_rect(0,400,W_width,200,green)
            draw_text(str(uncleRicky.selectedNPC.name) + ":", 30,420,black,normalFont)
            draw_text(str(uncleRicky.selectedNPC.npcMessages[uncleRicky.selectedNPC.npcMessageNum]),30,450,black,normalFont)
            draw_text("Sure",30,480,black,normalFont)
            draw_text("No fuck off",30,510,black,normalFont)
            draw_rect(5,interactionCursor,20,20,orange)
        
        if displayNPCInteraction:
            draw_rect(0,400,W_width,200,green)
            draw_text(str(uncleRicky.selectedNPC.name) + ":", 30, 420, black, normalFont)
            draw_text(str(uncleRicky.selectedNPC.npcMessages[uncleRicky.selectedNPC.npcMessageNum]), 30, 450,black,normalFont)
            if uncleRicky.selectedNPC.name == "Daddy":
                if uncleRicky.selectedNPC.npcMessageNum == 1:
                    draw_text("<3",30,480,black,normalFont)
                    draw_text("ok",30,510,black,normalFont)
                else:
                    draw_text("Yes",30,480,black,normalFont)
                    draw_text("Ew no get away from me", 30, 510,black,normalFont)
            if uncleRicky.selectedNPC.name == "Baldy":
                if uncleRicky.selectedNPC.npcMessageNum == 0:
                    draw_text("Pokeball - $10",30,480,black,normalFont)
                    draw_text("Health Potion - $10",30,510,black,normalFont)

            draw_rect(5,interactionCursor,20,20,orange)

        #draw pokemon stats
        if displayPokemonStats:
            for x in range(len(uncleRicky.pokemon)):
                draw_text(str(uncleRicky.pokemon[x].name),100*x,10,white,normalFont)
                draw_text("HP: " + str(int(uncleRicky.pokemon[x].health)) + "/" + str(int(uncleRicky.pokemon[x].maxHealth)),100*x,30,white,normalFont)
                draw_text("Level: " + str(int(uncleRicky.pokemon[x].level)),100*x,50,white,normalFont)
                draw_text("XP: " + str(int(uncleRicky.pokemon[x].xp)) + "/" + str(int(uncleRicky.pokemon[x].xpCap)),100*x,70,white,normalFont)

        #draw inventory items
        if displayInventory:
            draw_text("$" + str(uncleRicky.money),600,10,white,normalFont)
            draw_text("Pokeballs: " + str(uncleRicky.pokeballCount), 600,30,white,normalFont)
            draw_text("Health Potions: " + str(uncleRicky.healthPotCount),600,50,white,normalFont)

        #draw player coordinates
        draw_text(str(playerX) + "," + str(playerY),700,580,white,normalFont)

        pygame.display.update()