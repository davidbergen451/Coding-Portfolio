#########################################################################################################################################################################################################
"""Importing  stuff"""
import os 
import random 
import sys 
import time 


class RestartChoice(Exception):
    pass


class RestartStory(Exception):
    pass


class QuitGame(Exception):
    pass


fastspeed = 0.25
section_checkpoint = None


def game_sleep(seconds):
    """Sleep for the requested delay; Ctrl+C can still stop the game."""
    time.sleep(max(0, seconds))


def ask_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please enter y or n.")


def iamspeed():
    """Let the player choose the text speed."""
    global fastspeed
    while True:
        choice = input("Text speed: [1] Fast  [2] Normal  [3] Slow : ").strip()
        if choice in {"", "1"}:
            fastspeed = 0.05
            return
        if choice == "2":
            fastspeed = 0.25
            return
        if choice == "3":
            fastspeed = 0.5
            return
        print("Please choose 1, 2, or 3.")


def save_section_checkpoint(section_name):
    """Save the mutable state at the start of a story section."""
    global section_checkpoint
    state_names = [
        "randomhp", "health", "cash", "vardebbugger", "police", "safe",
        "wep", "run", "apple", "free_escape_ticket", "bag_of_chips",
        "super_heal", "medkit", "coke", "cookie", "turtle", "impostercall",
        "evasiveness", "newfriends", "sewers", "secretending", "explosives",
        "baseballbat"
    ]
    section_checkpoint = {name: globals().get(name) for name in state_names}


def restore_game_state(state):
    """Restore a previously saved section state."""
    if state:
        globals().update(state)


# --- Shop prices (used in part5store) ---
cookie_cost = 15
coke_cost = 30
medkit_cost = 50
super_heal_cost = 70
bag_of_chips_cost = 60
free_escape_ticket_cost = 20


def game_input(prompt):
    """Read input and provide restart/quit commands at any choice."""
    answer = input(prompt).strip()
    command = answer.lower()
    if command in {"r", "restart"}:
        raise RestartChoice()
    if command in {"q", "quit"}:
        raise QuitGame()
    return answer


def reset_game_state():
    """Reset all mutable game state so a new run starts cleanly."""
    global randomhp, health, cash, vardebbugger, police, safe, wep, run, apple
    global free_escape_ticket, bag_of_chips, super_heal, medkit, coke, cookie
    global turtle, impostercall, evasiveness, newfriends, sewers, secretending
    global explosives, baseballbat

    randomhp = random.randint(60, 85)
    health = randomhp
    cash = 0
    vardebbugger = 0
    police = 0
    safe = 0
    wep = 0
    run = 0
    apple = 0
    free_escape_ticket = 0
    bag_of_chips = 0
    super_heal = 0
    medkit = 0
    coke = 0
    cookie = 0
    turtle = 0
    impostercall = 0
    evasiveness = 0
    newfriends = 0
    sewers = 0
    secretending = 0
    explosives = 0
    baseballbat = 0


def game_over(reason="You died."):
    """Offer a restart of the current section, a full story restart, or quit."""
    print(f"\n{reason}")
    while True:
        choice = input(
            "[1] Restart choice/section  [2] Restart story  [3] Quit\n> "
        ).strip().lower()

        if choice in {"1", "c", "choice", "r", "restart"}:
            raise RestartChoice()
        if choice in {"2", "s", "story"}:
            raise RestartStory()
        if choice in {"3", "q", "quit"}:
            raise QuitGame()
        print("Please choose 1, 2, or 3.")


def settings():
    # Startup confirmation was intentionally removed.
    print("proceeding...\n")
    iamspeed()

#########################################################################################################################################################################################################
"""For later processing"""

def use_de_items():
    """Use one available healing item when health reaches zero."""
    global health, apple, bag_of_chips, super_heal, medkit, coke, cookie, evasiveness
    items = [
        ("super heal", "super_heal", 75), ("medkit", "medkit", 51),
        ("bag of chips", "bag_of_chips", None), ("apple", "apple", 15),
        ("coke", "coke", 15), ("cookie", "cookie", 15)
    ]
    for label, attr, amount in items:
        if globals().get(attr, 0) > 0:
            globals()[attr] -= 1
            print(f"You used a {label} to avoid dying of low health.")
            if attr == "bag_of_chips":
                for _ in range(random.randint(16, 21)):
                    health += random.randint(1, 5)
            else:
                health += amount
            if attr == "coke":
                evasiveness += 1
            print("Your health is now:", health)
            return True
    return False


def healthcheck():
    """Handle critical health once, without recursively consuming all inventory."""
    if health > 0:
        return True
    if use_de_items() and health > 0:
        return True
    game_over("You died of low health.")


################################################################################

def startup():
    """Simple startup screen with no jokes or external media."""
    print("\nStarting David's Adventure...")
    game_sleep(0.25)
    print("Loading...")
    game_sleep(0.25)
    print("Let's begin.\n")


def part1():
    global cash, health, apple, baseballbat, newfriends
    print("You have just moved to a new house in a new neighborhood.")
    game_sleep(fastspeed)

    random_num = random.randint(9, 21)
    cash += random_num
    print("You just checked your wallet and found you have:", cash, "cash to start with")
    print("You are tired from the move and have:", health, "health")

    lets_go = game_input("Do you want to explore the house (1) or look around outside? (2) ")
    baseballbat = 0
    newfriends = 0

    if lets_go == "1":
        random_number = random.randint(1, 10)
        if random_number < 3:
            print("You didn't find anything in the house; the previous owners cleaned up well.")
        elif random_number == 4 or random_number == 9:
            print("You found an apple!")
            apple += 1
        else:
            print("You found a baseball bat (old)")
            baseballbat = 1
    else:
        go_ahead_take_the_bait = game_input("You go outside and see your neighbor's house. It looks old, dusty, and deserted. Check it out? (y/n) ")
        if "y" in go_ahead_take_the_bait:
            print("You go inside and find an old, grey-haired man sleeping on the couch.")
            die = game_input("Wake him up? (y/n) ")
            if "y" in die:
                print("He is mad and starts yelling at you.")
                game_sleep(1)
                print("You turn around to leave.")
                game_sleep(0.5)
                print("The man says, 'WAIT!'")
                game_sleep(1)
                print("You stop and decide to talk with him for a while.")
                game_sleep(1)
                print("You end up being good friends after a quick chat and discover that you are related.")
                game_sleep(1)
                newfriends = 1
            else:
                print("That was a close call.")
        else:
            print("You just avoided death.")
    starve = game_input("It's lunch time, go to the fridge to look for food? (y/n)")
    if "n" in starve:
        print("you died of extreme hunger...")
        game_over()
    else:
        print("there is no food...")
        print("however...")
        print("you find a magnet on the fridge with a number on it")
        ded = game_input("call the number? (y/n)")
        if "y" in ded:
            print("a voice says, 'hello, and welcome to Little Nero's, pizza is free today, how may I help you?'")
            order_poison = game_input("order free pizza? (y/n)")
            if "y" in order_poison:
                print("you ordered free pizza and it should come soon...")
                game_sleep(5)
                print("you heard an angry grunt and a bang")
                answer_to_robber = game_input("the doorbell rung, answer it? (y/n)")
                if"y" in answer_to_robber:
                    print("...")
                    game_sleep(1)
                    print("It's the pizza delivery man!")
                    eat_poison = game_input("eat the pizza? (y/n)")
                    if "y" in eat_poison:
                        random_numeral = random.randint(3,33)
                        health += random_numeral
                        print("you ate the pizza and you are satisfied and full.")
                        print("you regained your strength from food, your health is now : ", health)
                    else:
                        print("you died of extreme hunger...")
                        game_over()
                else:
                    print("you died of extreme hunger...")
                    game_over()
            else:
                print("you died of extreme hunger...")
                game_over()
        else:
            print("you died of extreme hunger...")
            game_over()
            game_sleep(1)


def part2sleep():
    global health, cash, baseballbat, police
    game_sleep(1)
    print("The lights suddenly went out...")
    game_sleep(1)
    print("I wonder what happened...")
    game_sleep(1)
    print("You feel very tired from moving.")
    game_sleep(0.5)

    die_in_your_sleep = game_input("Go to sleep? (y/n) ")
    if "y" in die_in_your_sleep:
        print("You went upstairs to sleep.")
        game_sleep(0.5)
        print("Goodnight...")
        game_sleep(0.5)

        sleepfx = 1
        while sleepfx < 10:
            random_number = random.randint(1, 3)
            print("z")
            game_sleep(0.05)
            print(" z")
            game_sleep(0.025)
            print("  z")
            game_sleep(0.05)
            health += random_number
            print("You regained your strength while sleeping; your health is now:", health)
            print("z")
            game_sleep(0.025)
            print(" z")
            game_sleep(0.05)
            print("  z")
            game_sleep(0.025)
            sleepfx += 1
        
        print("   *")
        game_sleep(0.1)
        print("BANG!")
        print("CRASH!")
        print("You heard glass shatter...")
        game_sleep(0.5)
        print("Someone with a crowbar came into your room and attacked you!")

        if baseballbat == 1:
            game_sleep(0.5)
            print("You instinctively defended yourself with the baseball bat.")
            cash += 10
            health -= 5
            healthcheck()
            print("He retreated, dropping 10 bucks on his way out.")
        else:
            die_in_vain = game_input("Call the police? (y/n) ")
            if "y" in die_in_vain:
                game_sleep(0.5)
                print("The person was beating you up until they heard the police, then retreated.")
                random_number = random.randint(15, 35)
                health -= random_number
                healthcheck()
                print("You significantly lost health from the attack; your health is:", health)
                police = 1
            else:
                print("You got beaten to a pulp; he wiped the living daylight out of you...")
                print("Murdered mercilessly...")
                game_over()
    else:
        random_number = random.randint(10, 30)
        health -= random_number
        healthcheck()
        print("You significantly lost health from not sleeping; your health is:", health)
        print("You are very tired; why didn't you go to sleep?")
        game_sleep(0.5)
        print("You look on your phone, and the news says there have been 29 break-ins in your neighborhood recently...")


def part3breakinnight1():
    global health, cash, baseballbat 
    print("I think it is a good idea to put up some defenses.")
    game_sleep(0.25)
    print("The guy at the store is providing material free because of so many break-ins.")
    game_sleep(0.25)

    die_in_vain2 = game_input("Recommendation: Board up the house? (y/n) ")
    if "y" in die_in_vain2:
        destiny = game_input("Choose a number in the range 1-10: ")
        
        if destiny in ["1", "3", "7", "9"]:
            random_number = random.randint(1, 3)
            print("You did a great job protecting the house.")
            print("You went upstairs to sleep.")
            game_sleep(0.5)
            print("Goodnight...")
            game_sleep(0.5)
            sleepfx = 1
            while sleepfx < 10:
                random_number = random.randint(1, 3)
                print("z")
                game_sleep(0.05)
                print(" z")
                game_sleep(0.025)
                print("  z")
                game_sleep(0.05)
                health += random_number
                print("You regained your strength while sleeping; your health is now:", health)
                print("z")
                game_sleep(0.025)
                print(" z")
                game_sleep(0.05)
                print("  z")
                game_sleep(0.025)
                sleepfx += 1
            print("   *")
            if random_number == 1:
                print("You heard a loud clink, a smash, and an angry grunt...")
                game_sleep(0.5)
                print("Your boards held them back...")
            else:
                print("Two men with crowbars broke into your room and attacked you!")
                game_sleep(0.5)
                if baseballbat == 1:
                    print("You instinctively defended yourself with the baseball bat.")
                    cash += 20
                    health -= 10
                    healthcheck()
                    game_sleep(0.25)
                    print("They retreated, dropping 20 bucks on their way out.")
                else:
                    die_in_vain3 = game_input("Call the police? (y/n) ")
                    if "y" in die_in_vain3:
                        print("They were beating you up until they heard the police, then retreated.")
                        random_number = random.randint(15, 40)
                        health -= random_number
                        healthcheck()
                        print("You significantly lost health from the attack; your health is:", health)
                        police = 1
                    else:
                        print("You got beaten to a pulp; they wiped the living daylight out of you...")
                        print("Murdered mercilessly...")
                        game_over()
        
        elif destiny in ["2", "5", "8", "10"]:
            random_number = random.randint(1, 5)
            print("You did an okay job protecting the house.")
            if random_number == 1:
                print("You heard a loud clink, a smash, and an angry grunt...")
                game_sleep(0.5)
                print("Your boards held them back...")
            else:
                print("Two men with crowbars broke into your room and attacked you!")
                game_sleep(0.5)
                if baseballbat == 1:
                    print("You instinctively defended yourself with the baseball bat.")
                    cash += 15
                    health -= 15
                    healthcheck()
                    game_sleep(0.25)
                    print("They retreated, dropping 15 bucks on their way out.")
                else:
                    die_in_vain4 = game_input("Call the police? (y/n) ")
                    if "y" in die_in_vain4:
                        print("They were beating you up until they heard the police, then retreated.")
                        random_number = random.randint(20, 50)
                        health -= random_number
                        healthcheck()
                        print("You significantly lost health from the attack; your health is:", health)
                        police = 1
                    else:
                        print("You got beaten to a pulp; they wiped the living daylight out of you...")
                        print("Murdered mercilessly...")
                        game_over()
        
        elif destiny in ["4", "6"]:
            random_number = random.randint(1, 2)
            print("You did a perfect job protecting the house.")
            print("You went upstairs to sleep.")
            game_sleep(0.5)
            print("Goodnight...")
            game_sleep(0.5)
            sleepfx = 1
            while sleepfx < 10:
                random_number = random.randint(1, 3)
                print("z")
                game_sleep(0.05)
                print(" z")
                game_sleep(0.025)
                print("  z")
                game_sleep(0.05)
                health += random_number
                print("You regained your strength while sleeping; your health is now:", health)
                print("z")
                game_sleep(0.025)
                print(" z")
                game_sleep(0.05)
                print("  z")
                game_sleep(0.025)
                sleepfx += 1
            print("   *")
            if random_number == 1:
                print("You heard a loud clink, a smash, and an angry grunt...")
                game_sleep(0.5)
                print("Your boards held them back...")
            else:
                print("A man with a crowbar broke into your room and attacked you!")
                game_sleep(0.5)
                if baseballbat == 1:
                    print("You instinctively defended yourself with the baseball bat.")
                    cash += 25
                    health -= 5
                    healthcheck()
                    game_sleep(0.25)
                    print("He retreated, dropping 25 bucks on his way out.")
                else:
                    die_in_vain5 = game_input("Call the police? (y/n) ")
                    if "y" in die_in_vain5:
                        print("He was beating you up until they heard the police, then retreated.")
                        random_number = random.randint(10, 20)
                        health -= random_number
                        healthcheck()
                        print("You significantly lost health from the attack; your health is:", health)
                        police = 1
                    else:
                        print("You got beaten to a pulp; he wiped the living daylight out of you...")
                        print("Murdered mercilessly...")
                        game_over()
    else:
        print("Okayyyy....")
        game_sleep(1)
        print("Wow, it got late fast.")
        print("I guess we can just go to sleep then...")
        game_sleep(2.5)
        print("BbBaAAaaaAaAANnnNnGGggGgggG!")
        game_sleep(1)
        print("Someone shot you because your house was not boarded up...")
        game_sleep(0.5)
        print("You died.")
        game_over()


def part4basementventure():
    global health, cash, cookie, coke, medkit, super_heal, bag_of_chips, apple, evasiveness, weaponthingy, impostercall, code

    
    print("There are bad guys all over the place nowadays...")
    game_sleep(0.1)
    print("The boards can't hold all of them back, we need to do something about it.")
    game_sleep(0.1)
    print("Option [1]: Hide in the basement.")
    game_sleep(0.1)
    print("Option [2]: Look around the house more for any other bad guys.")
    game_sleep(0.1)
    print("Option [3]: Hide in the basement, lock the door, and look around.")
    game_sleep(0.1)

    death_death_or_death = game_input("What do you choose? ([1],[2],[3]): ")

    police = 0
    if "1" in death_death_or_death:
        print("You hid in the basement, but you didn't lock the door...")
        game_sleep(2)
        print("They found you and you were stabbed to death.")
        game_over()

    elif "2" in death_death_or_death:
        print("You found a bad guy!")
        print("Before you could do anything, he shot you, not so lucky this time...")
        game_over()

    else:
        print("You hid in the basement, locked the door so they can't get in, and found food, weapons, and a little change to spare.")
        game_sleep(0.1)
        print("You ate the food because you were hungry.")
        random_number = random.randint(15, 25)
        health += random_number
        print("Your health is:", health)
        game_sleep(0.1)
        print("Your cash is:", cash)
        game_sleep(0.1)

        if baseballbat == 1:
            print("You don't need a weapon because you already have one.")
            wep = 5
            weaponthingy = "baseball bat"
        else:
            randomnumber2 = random.randint(0, 3)
            weaponthing = ["pitchfork", "crowbar", "hammer", "wrench"]
            weaponthingy = weaponthing[randomnumber2]
            print("You found a", weaponthingy)
            wep = 5

    random_number = random.randint(1, 5)
    if random_number < 4:
        game_sleep(0.1)
        print("You found a hidden code!")
        code = random.randint(1234, 7654)
        game_sleep(0.1)
        print(f"{code}!")
        game_sleep(0.1)
        print("They broke through the locked door even though it was locked...")
        game_sleep(0.1)
        print("You are fighting.")
        health -= 5
        healthcheck()
        game_sleep(1)
        print("You are still fighting.")
        health -= 10
        healthcheck()
        game_sleep(1)
        print("A crook dropped a padlock.")
        game_sleep(0.1)

        fight_to_your_death = game_input("Keep fighting [1] or use the extra padlock [2]? ([1]/[2]): ")

        if "1" in fight_to_your_death:
            print("You managed to fight 'em all off.")
            game_sleep(0.1)
            print("You lost a lot of health; however, on the bright side, they dropped some spare cash.")
            random_number = random.randint(12, 34)
            cash += random_number
            health -= random_number
            healthcheck()
            print(f"Your health is now: {health} and you have: {cash} cash.")
            safe = 1
        else:
            print("That should hold 'em off for the night, whewf...")
            safe = 1
    else:
        print("They couldn't break through the locked door, whewf...")




def part5store():
    global health, cash, code, safe, turtle, run, newfriends, free_escape_ticket, cookie_cost, cookie, coke_cost, coke, medkit_cost, medkit, super_heal, super_heal_cost, bag_of_chips_cost, bag_of_chips, free_escape_ticket_cost
    
    game_sleep(1)
    print("you are finally safe now")
    game_sleep(1)
    print("you fell asleep in the basement...")
    game_sleep(3)
    
    sleepfx = 1
    while sleepfx < 10:
        random_number = random.randint(1, 3)
        print("z")
        game_sleep(0.05)
        print(" z")
        game_sleep(0.025)
        print("  z")
        game_sleep(0.05)
        health += random_number
        print("you regained your strength sleep, your health is now : ", health)
        print("z")
        game_sleep(0.025)
        print(" z")
        game_sleep(0.05)
        print("  z")
        game_sleep(0.025)
        sleepfx += 1

    print("I think it is time to head out for some supplies, we are running low")
    game_sleep(0.1)
    
    die_die = game_input("get supplies [1] or hide in the basement [2]?")
    if "1" in die_die:
        print("okay, lets get some supplies")
        game_sleep(0.1)
        if safe == 1:
            print("you knocked over a painting by accident")
            game_sleep(0.1)
            print("there is a hidden safe!")
            game_sleep(0.1)
            deathcode = game_input("use the code? (y/n)")
            if "y" in deathcode:
                print("you used ", code, " and it opened!")
                if cash > health:
                    print("there is a medkit!")
                    print("you used the medkit")
                    health += 25
                    print("your health is now : ", health)
                else:
                    print("there's some cash!")
                    cash += 25
                    print("your cash is now : ", cash)
            else:
                print("you just left it there...")
        else:
            print("")

        random_number = random.randint(1, 2)
        if random_number == 1:
            print("you slipped on ice on the road and hurt yourself")
            health -= 15
            healthcheck()
            print("your health is now : ", health)
        else:
            print("you arrived at the store")
    else:
        print("you stayed in the basement")
        turtle = 1

    if turtle == 0:
        def print_message():
            print('I\'m sorry, I did not understand your selection. Please enter the corresponding number for your response.')
        
        def print_message2():
            print('I\'m sorry, but you need more money to buy that...')

        drinks = []

        def coffee_bot():
            print('Welcome to the store!')
            order_drink = 'y'
            while order_drink == 'y':
                drink_type = get_drink_type()
                if drink_type == 'oof':
                    drink = '{}'.format(drink_type)
                    print('{}!'.format(drink))
                    break
                else:
                    drink = '{}'.format(drink_type)
                    print('Alright, that\'s a {}!'.format(drink))
                    drinks.append(drink)
                    while True:
                        order_drink = game_input('Would you like anything else? (y/n) \n> ')
                        if order_drink == 'n':
                            vardebbugger = 1
                        else:
                            vardebbugger = 0
                        if order_drink in ['y', 'n']:
                            break
                
                if drink_type == 'oof':
                    print("you ran out of the store...")
                else:
                    if vardebbugger == 1:
                        print('Okay, so I have:')
                        for drink in drinks:
                            print('-', drink)
                        name = game_input('Can I get your name please? \n> ')
                        print('Thanks, {}! Come again soon!'.format(name))
                    else:
                        game_sleep(1)

        def get_drink_type():
            global health, cash, code, safe, turtle, run, newfriends, free_escape_ticket, cookie_cost, cookie, coke_cost, coke, medkit_cost, medkit, super_heal, super_heal_cost, bag_of_chips_cost, bag_of_chips, free_escape_ticket_cost
            while True:
                print("you have : ", cash, " cash")
                if newfriends == 0:
                    res = game_input('What would you like to buy? \n[1] Cookie $15 \n[2] Coca Cola $30 \n[3] Medkit $50 \n[4] Super Heal $70 \n[5] Bag Of Chips $60 \n[0] Just leave and get outta here \n> ')
                else:
                    res = game_input('What would you like to buy? \n[1] Cookie $15 \n[2] Coca Cola $30 \n[3] Medkit $50 \n[4] Super Heal $70 \n[5] Bag Of Chips $60 \n[6] Something for your neighbor $20 \n[0] Just leave and get outta here \n> ')

                if res == '1':
                    if cash >= cookie_cost:
                        cash -= cookie_cost
                        cookie += 1
                        return 'Cookie'
                    else:
                        print_message2()

                elif res == '2':
                    if cash >= coke_cost:
                        cash -= coke_cost
                        coke += 1
                        return 'Coca Cola'
                    else:
                        print_message2()

                elif res == '3':
                    if cash >= medkit_cost:
                        cash -= medkit_cost
                        medkit += 1
                        return 'Medkit'
                    else:
                        print_message2()

                elif res == '4':
                    if cash >= super_heal_cost:
                        cash -= super_heal_cost
                        super_heal += 1
                        return 'Super Heal'
                    else:
                        print_message2()

                elif res == '5':
                    if cash >= bag_of_chips_cost:
                        cash -= bag_of_chips_cost
                        bag_of_chips += 1
                        return 'Bag of Chips'
                    else:
                        print_message2()

                elif res == '6':
                    if newfriends == 1:
                        if cash >= free_escape_ticket_cost:
                            cash -= free_escape_ticket_cost
                            free_escape_ticket = 1
                            return 'Something for your neighbor'
                        else:
                            print_message2()
                    else:
                        print('*deep sigh*')

                elif res == '0':
                    return 'oof'
                else:
                    print_message()

        coffee_bot()
    
    if run == 0:
        if turtle == 1:
            print("...")
        else:
            print("it is late and the shop closed")
    else:
        game_sleep(0.1)
        print("you ran back home")

    if free_escape_ticket == 1:
        print("you gave something to your neighbor")
        print("He was happy and promised to do something for you in return")
    else:
        game_sleep(0.1)


def part6deathpizza():
    global health, cash, cookie, coke, medkit, super_heal, bag_of_chips, apple, evasiveness, weaponthingy, impostercall

    print("It's getting late, you feel hungry.")
    death_pizza = game_input("Order pizza? (y/n): ")

    if "y" in death_pizza:
        print("You phoned the pizza place.")
        game_sleep(0.5)
        print("The voice is cutting out a little...")
        game_sleep(0.5)
        print("A muffled voice says, '#ello, #nd welc#### to #r# Pizza's, th#re #s a f#ee #i#za give#way , ho# m#y # #elp y#u?'")
        game_sleep(0.5)
        print("Free pizza giveaway?")
        game_sleep(0.5)
        print("Ye# th#r# is # fr## piz## give#way.")
        game_sleep(0.5)
        print("I would like a pizza...")
        game_sleep(0.5)
        print("Thank you for your order, the pizza should come soon.")
        impostercall = 1
    else:
        cursed_items = game_input("Use your items instead? (y/n): ")

        if "y" in cursed_items:
            def use_items():
                global cookie, coke, medkit, super_heal, health, apple, bag_of_chips, evasiveness
                if apple > 0:
                    apple -= 1
                    print("You used an apple.")
                    health += 15
                    print("Your health is now:", health)
                if bag_of_chips > 0:
                    print("You used a bag of chips.")
                    bag_of_chips -= 1
                    random_chip = random.randint(16, 21)
                    for _ in range(random_chip):
                        chip_hp = random.randint(1, 5)
                        health += chip_hp
                        print("Your health is now:", health)
                if super_heal > 0:
                    super_heal -= 1
                    print("You used a super heal.")
                    health += 75
                    print("Your health is now:", health)
                if medkit > 0:
                    medkit -= 1
                    print("You used a medkit.")
                    health += 51
                    print("Your health is now:", health)
                if coke > 0:
                    coke -= 1
                    print("You used a coke.")
                    health += 15
                    evasiveness += 1
                    print("Your health is now:", health)
                if cookie > 0:
                    cookie -= 1
                    print("You used a cookie.")
                    health += 15
                    print("Your health is now:", health)

            for _ in range(10):
                use_items()
        else:
            print("You didn't use your items...")

    if impostercall == 0:
        game_sleep(3)
        print("It's getting very late.")
        die_in_your_sleep = game_input("Go to sleep? (y/n): ")

        if "y" in die_in_your_sleep:
            print("You went upstairs to sleep.")
            game_sleep(0.5)
            print("Goodnight...")
            game_sleep(0.5)

            sleepfx = 1
            while sleepfx < 10:
                random_number = random.randint(1, 3)
                print("z")
                game_sleep(0.05)
                print(" z")
                game_sleep(0.025)
                print("  z")
                game_sleep(0.05)
                health += random_number
                print("You regained your strength during sleep, your health is now:", health)
                print("z")
                game_sleep(0.025)
                print(" z")
                game_sleep(0.05)
                print("  z")
                game_sleep(0.025)
                sleepfx += 1
        else:
            random_number = random.randint(10, 30)
            health -= random_number
            healthcheck()
            print("You significantly lost health from not sleeping, your health is:", health)
            print("You are very tired, why didn't you go to sleep?")
            game_sleep(0.5)

    else:
        game_sleep(0.25)
        print("You ordered free pizza and it should come soon...")
        game_sleep(3)
        print("You heard a muffled grunt and a bang.")
        answer_to_robber = game_input("The doorbell rang, answer it? (y/n): ")

        if "y" in answer_to_robber:
            print("...")
            game_sleep(1)
            print("It's the pizza delivery man!")
            game_sleep(2)
            print("Wait a minute... why does he have a weird mask on?")
            game_sleep(1)
            print("IT'S AN IMPOSTER!")
            
            randomdmg = random.randint(1, 3)
            randomdmg2 = random.randint(9, 27)

            for _ in range(randomdmg2):
                health -= randomdmg
                healthcheck()
                print("You significantly lost health from the imposter, your health is:", health)
                randomdmg = random.randint(1, 3)

            game_sleep(0.5)
            print(f"You managed to beat him back using your {weaponthingy}.")
        else:
            print("You heard a loud smash.")
            game_sleep(1)
            print("The door broke down.")
            game_sleep(2)
            print("...")
            game_sleep(1)
            print("Uh oh...")

            randomdmg = random.randint(1, 2)
            randomdmg2 = random.randint(7, 21)

            print("AN IMPOSTER!")
            for _ in range(randomdmg2):
                health -= randomdmg
                healthcheck()
                print("You significantly lost health from the imposter, your health is:", health)
                randomdmg = random.randint(1, 3)

            game_sleep(0.5)
            print(f"You managed to beat him back using your {weaponthingy}.")

        game_sleep(3)
        print("It's getting very late.")
        die_in_your_sleep = game_input("Go to sleep? (y/n): ")

        if "y" in die_in_your_sleep:
            print("You went upstairs to sleep.")
            game_sleep(0.5)
            print("Goodnight...")
            game_sleep(0.5)

            sleepfx = 1
            while sleepfx < 10:
                random_number = random.randint(1, 3)
                print("z")
                game_sleep(0.05)
                print(" z")
                game_sleep(0.025)
                print("  z")
                game_sleep(0.05)
                health += random_number
                print("You regained your strength during sleep, your health is now:", health)
                print("z")
                game_sleep(0.025)
                print(" z")
                game_sleep(0.05)
                print("  z")
                game_sleep(0.025)
                sleepfx += 1
        else:
            random_number = random.randint(10, 30)
            health -= random_number
            healthcheck()
            print("You significantly lost health from not sleeping, your health is:", health)
            print("You are very tired, why didn't you go to sleep?")
            game_sleep(0.5)

    print("   *")


def cutscene():

    game_sleep(2)
    print("...")

    game_sleep(1)

    print("Its the alarm for the store!")

    game_sleep(2)


    print("oh no!")

    game_sleep(1)

    print("THE MAFIA BOSS IS ROBBING THE STORE!")

    game_sleep(1)

    print("QUICK! ")
    print("WE NEED TO ESCAPE! ")

    game_sleep(1)


def escape():
    global sewers, health
    global secretending
    if free_escape_ticket == 1:
        print("your neighbor offered to drive you away from danger")
        while True:
            escape_tactic = game_input("what is your plan? \n[1] Hide at the house \n[2] Hide in the sewers\n[3] Ride in your neighbor's truck to escape (SECRET ENDING) \n>")
            if escape_tactic == "1":
                print("The Mafia Boss saw you!")
                print("He threw a grenade and blew up your house!")
                print("you died")
                game_sleep(1)
                game_over("You were caught while trying to hide.")
                continue
            elif escape_tactic == "2":
                sewers = 1
                break
            elif escape_tactic == "3":
                secretending = 1
                break
            else:
                print("huh?")
                game_sleep(1)
    else:
        while True:
            escape_tactic = game_input("what is your plan? \n[1] Hide at the house \n[2] Hide in the sewers \n>")
            if escape_tactic == "1":
                print("The Mafia Boss saw you!")
                print("He threw a grenade and blew up your house!")
                print("you died")
                game_sleep(1)
                game_over("You were caught while trying to hide.")
                continue
            elif escape_tactic == "2":
                sewers = 1
                break
            else:
                print("huh?")
                game_sleep(1)
        

    if sewers == 1:
        game_sleep(2)
        print("you escaped to the sewers")
        game_sleep(0.5)
        music_player = False
        random_drown = random.randint(1,5)
        if random_drown == 3:
            print("you fell into the sewage and got hurt")
            health -= random_drown*3
            healthcheck()
        else:
            game_sleep(0.001)
        game_sleep(1)
        print("3RR0R")
        print("Pl4y3rScr1pts.D14l0gu3S3rv1c3:48 ")
        print("I... ")
        print("ERR0R... ")
        print("Rebo0ting...")
        print("RebOot fa1led. ")
        print("Uns4nct10n3d m4nu4l 0verr1d3 r3qu3st3d. ")
        print("F1r3w4ll byp4ss3d, ov3rr1de 1n1t14t3d. ")
        game_sleep(0.75)
        print("Error er r r or ERror Error Error Error Error Error Error Error Error Error Error Error Error Error ")
        game_sleep(0.5)
        print("Mafia Boss speaking, And up until now, you have been playing easy mode. ")
        game_sleep(1)
        print("Luckily for you, that's about to change.")
        game_sleep(1)
        print("time to die")
        game_sleep(1)
        random_boss = random.randint(11,25)
        random_boss_amount = random.randint(1,3)
        print("*The mafia boss took out his gun and shot you*")
        for x in range(random_boss_amount):
            print("*POW*")
            health -= random_boss
            healthcheck()
            game_sleep(random_boss_amount-0.5)
            print("health = ", health)
            random_boss = random.randint(11,25)
        print("*Click*")
        game_sleep(1)
        print("*cliCk*")
        game_sleep(0.9)
        print("*cLick*")
        game_sleep(0.8)
        print("*cLIck*")
        game_sleep(0.7)
        print("*cLicK*")
        game_sleep(0.6)
        print("*ClICK*")
        game_sleep(0.5)
        print("*cLick*")
        game_sleep(0.4)
        print("*cLick*")
        game_sleep(0.3)
        print("...")
        game_sleep(0.2)
        print("shoot!")
        game_sleep(0.1)
        print("I musta ran outa bullets there")
        game_sleep(0.1)
        print("I guess its just me and you, crowbar versus ", weaponthingy)
        game_sleep(2.5)
        print("ClinK")
        game_sleep(1)
        health -= random.randint(5,10)
        healthcheck()
        print("cLang")
        health -= random.randint(3,7)
        healthcheck()
        game_sleep(1)
        print("cRaSh")
        health -= random.randint(5,10)
        healthcheck()
        game_sleep(1)
        print("BaNG")
        health -= random.randint(7,9)
        healthcheck()
        game_sleep(1)
        print("SLaaM")
        health -= random.randint(7,9)
        healthcheck()
        game_sleep(1)
        print("you beat him and you are at : ", health, " health")
        game_sleep(3)
        print("You...")
        game_sleep(2)
        print("you did it.")
        game_sleep(1)
        print("The Mafia Boss has been defeated.")
        game_sleep(0.5)
        print("you heard police sirens in the distance")
        game_sleep(0.25)
        print("Someone lowered a ladder, it looks safe to climb...")
        game_sleep(0.5)
        print("Outside, the remaining Villains have been arrested by the police")
        game_sleep(1)
        print("the Neighborhood has been restored.")
        game_sleep(1)
        print("The Story ends here.")
        game_sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("")
        print("Congratulations.")
        game_sleep(3)
        print("")
        print("Thank you for playing!")
        sys.exit()
    elif secretending == 1:
        game_sleep(0.5)
        print("you are in the truck")
        game_sleep(2)
        music_player = False 
        print("wait a second... What's that?")
        print("you saw a sign saying : DA MAFIA BOSS’S HOUSE, DO NOT ENTER!")
        def de4th():
            global health
            global explosives
            while True:
                deat2w4ys = game_input("go to the house [1] or just keep driving [2]")
                if deat2w4ys in ("1", "2"):
                    break
                print("huh?")
            if deat2w4ys == "1":
                print("there are guards at the entrance")
                wut = game_input("Break in and try getting past the guards [1] or sneak in using stealth [2]")
                if wut == "1":
                    ooflmao = random.randint(1,3)
                    ooflols = random.randint(3,5)
                    print(ooflols, " guards attacked you!")
                    for x in range(ooflmao):
                        health -= ooflmao*ooflols
                        healthcheck()
                        print("your health is : ", health)
                        print("")
                        game_sleep(0.5)
                    game_sleep(1)
                    print("you managed to get rid of the guards")
                    print("")
                    explosives = 1
                elif wut == "2":
                    ooflol = random.randint(1,5)
                    if ooflol == 4:
                        print("some guards saw you and attacked you but you managed to escape them")
                        health -= ooflol*3
                        healthcheck()
                        print("health : ", health)
                        print("")
                    else:
                        explosives = 1
                    print("you snuck into his house undetected")
                    game_sleep(1)
                    print("Like a Boss")
                    print("")
                    explosives = 1
                else:
                    print("wut?")
                    print("you died of mass errors and not cooperating with the system")
                    game_sleep(1)
                    game_over()
            elif deat2w4ys == "2":
                print("*CRACK*")
                game_sleep(1)
                print("GUNSHOT SOUND")
                game_sleep(1)
                print("you were killed")
                game_over()
        de4th()
    else:
        print("this is impossible, you shouldn't be reading this...")
        game_sleep(10)
        nonunicode = "\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff\u0100\u0101\u0102\u0103\u0104\u0105\u0106\u0107\u0108\u0109\u010a\u010b\u010c\u010d\u010e\u010f\u0110\u0111\u0112\u0113\u0114\u0115\u0116\u0117\u0118\u0119\u011a\u011b\u011c\u011d\u011e\u011f\u0120\u0121\u0122\u0123\u0124\u0125\u0126\u0127\u0128\u0129\u012a\u012b\u012c\u012d\u012e\u012f\u0130\u0131\u0132\u0133\u0134\u0135\u0136\u0137\u0138\u0139\u013a\u013b\u013c\u013d\u013e\u013f\u0140\u0141\u0142\u0143\u0144\u0145\u0146\u0147\u0148\u0149\u014a\u014b\u014c\u014d\u014e\u014f\u0150\u0151\u0152\u0153\u0154\u0155\u0156\u0157\u0158\u0159\u015a\u015b\u015c\u015d\u015e\u015f\u0160\u0161\u0162\u0163\u0164\u0165\u0166\u0167\u0168\u0169\u016a\u016b\u016c\u016d\u016e\u016f\u0170\u0171\u0172\u0173\u0174\u0175\u0176\u0177\u0178\u0179\u017a\u017b\u017c\u017d\u017e"
        n = 1000 #Change to make text longer

        #version 1, prints all out at once
        def glitchtext(length):
            output = ""
            for x in range(length):
                output += random.choice(nonunicode)
            return output
        for x in range(100):
          print (glitchtext(n))
          game_sleep(0.001)
        game_sleep(3)
        for x in range(1000):
            print(" th1s 1s th3 gl1tch 3nd1ng...")
            print("")
  
    if explosives == 1:
        print("The Mafia Boss has a lot of explosives ...")
        game_sleep(1)
        last_important_desicion = game_input("Light up the explosives [1] or get outa there [2]")
        if last_important_desicion == "1":
            print("You put a 3 minute timer on the explosion, ran out and...")
            print("...")
            sleeptime = 0.1
            while sleeptime < 1:
                print("Boom!")
                game_sleep(sleeptime)
                sleeptime += 0.1
            game_sleep(3)
            healthcheck()
            print("You...")
            game_sleep(2)
            print("you did it.")
            game_sleep(1)
            print("The Mafia Boss has been defeated.")
            game_sleep(0.5)
            print("Turns out, that he was in the house and there wasn't just guards there")
            game_sleep(0.5)
            print("you heard police sirens")
            game_sleep(0.5)
            print("Outside, the remaining Villains have been arrested by the police")
            game_sleep(1)
            print("the Neighborhood has been restored.")
            game_sleep(1)
            print("The Story ends here.")
            game_sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')
            print("")
            print("Congratulations, more endings will be coming if you enjoyed this game.")
            game_sleep(3)
            print("")
            print("Thank you for playing, this is version 2.0")
            sys.exit()
        else:
            print("A guard found you and shot you, you died")
            game_sleep(1)
            game_over()
    else:
        print("this is impossible, you shouldn't be reading this...")
        game_sleep(10)
        nonunicode = "\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff\u0100\u0101\u0102\u0103\u0104\u0105\u0106\u0107\u0108\u0109\u010a\u010b\u010c\u010d\u010e\u010f\u0110\u0111\u0112\u0113\u0114\u0115\u0116\u0117\u0118\u0119\u011a\u011b\u011c\u011d\u011e\u011f\u0120\u0121\u0122\u0123\u0124\u0125\u0126\u0127\u0128\u0129\u012a\u012b\u012c\u012d\u012e\u012f\u0130\u0131\u0132\u0133\u0134\u0135\u0136\u0137\u0138\u0139\u013a\u013b\u013c\u013d\u013e\u013f\u0140\u0141\u0142\u0143\u0144\u0145\u0146\u0147\u0148\u0149\u014a\u014b\u014c\u014d\u014e\u014f\u0150\u0151\u0152\u0153\u0154\u0155\u0156\u0157\u0158\u0159\u015a\u015b\u015c\u015d\u015e\u015f\u0160\u0161\u0162\u0163\u0164\u0165\u0166\u0167\u0168\u0169\u016a\u016b\u016c\u016d\u016e\u016f\u0170\u0171\u0172\u0173\u0174\u0175\u0176\u0177\u0178\u0179\u017a\u017b\u017c\u017d\u017e"
        n = 1000 #Change to make text longer

        #version 2, prints all out at once
        def glitchtext(length):
            output = ""
            for x in range(length):
                output += random.choice(nonunicode)
            return output
        for x in range(100):
          print (glitchtext(n))
          game_sleep(0.001)
        game_sleep(3)
        for x in range(1000):
            print(" th1s 1s th3 gl1tch 3nd1ng...")
            print("")


def run_story():
    """Run the adventure while allowing section or full-story restarts."""
    sections = [
        ("Part 1", part1),
        ("Part 2", part2sleep),
        ("Part 3", part3breakinnight1),
        ("Part 4", part4basementventure),
        ("Part 5", part5store),
        ("Part 6", part6deathpizza),
        ("Cutscene", cutscene),
        ("Escape", escape),
    ]

    reset_game_state()
    settings()

    index = 0
    while index < len(sections):
        section_name, section_function = sections[index]
        save_section_checkpoint(section_name)

        try:
            section_function()
            index += 1
        except RestartChoice:
            # Return to the beginning of the current major story section.
            restore_game_state(section_checkpoint)
            print(f"\nRestarting {section_name}...\n")
            continue


if __name__ == "__main__":
    while True:
        try:
            run_story()
            print("\nThanks for playing David's Adventure!")
            break
        except RestartStory:
            print("\nRestarting the adventure from the beginning...\n")
            continue
        except QuitGame:
            print("\nThanks for playing. Goodbye!")
            break
        except KeyboardInterrupt:
            # Player pressed Ctrl+C - exit cleanly
            print("\n\nInterrupted. Thanks for playing. Goodbye!")
            break
        except EOFError:
            # Input stream closed unexpectedly (e.g. piped input ran out).
            print("\n\nNo more input received. Thanks for playing. Goodbye!")
            break
