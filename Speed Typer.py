import time #used to calculate time taken to enter the string/phrase, and also to create pauses when going between windows 
import os #used to clear the cmd screen
import string #used to get letters to generate the string of letters
import random #used to randomly selected words or letters
import threading #used in multithreading the server (other file), used to create spinner whilst computer completes phrase
import itertools #used for spinner
import sys #used to flush the line on spinner for smooth animation
import pickle #used in file serialisation
import socket #used in multiplayer

#the Menu class stores a range of menus that are called throughout the program. This was a good way to keep them organised and make it easier when programming
class Menu():

    #this is used when you go into a game and it is starting to play; this is printed before the phrase/string is printed
    def launching():
        print("Test starts in 3")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        time.sleep(1)
    
    #Instructions for Time Trial mode
    def instrTimeTrial():
        print("Instructions")
        print("************\n")
        print("There are 3 modes, easy, medium and hard. Each mode has a random word (real or not) that you have to copy in the faster time possible\n")
        print("The corresponding lengths are 5,10 and 15 characters of upper and lowercase letters.\n")
        input("\nPress any button")
        os.system('cls')

    #Instructions for Climb The Ranks mode
    def instrCTR():
        print("Instructions")
        print("************\n")
        print("In this mode you will face the computer to see who can complete the phrase in the shortest time")
        print("You have currency that you can bet whilst playing, earn as much as you can!")
        print("Because of how kind I am I'll give you $10 to start with. Make the most of it!!")
        print("You can bet the currency, if you win you earn a multiplier on what bet, if you lose you lose what you bet.")
        input("\nPress any button")
        os.system('cls')

    #main menu
    def menu():
        print("Select mode: \n\
        1. Time Trial \n\
        2. Climb the Ranks! \n\
        3. Multiplayer \n\
        4. Exit")

    #main menu for Time Trial mode
    def menuTT():
        print("Select difficulty: \n\
        1. Easy \n\
        2. Medium \n\
        3. Hard\n\
        \n\
        9. Display Highscores \n\
        0. Back")

    #main menu for Climb The Ranks mode
    def menuCTR():
        print("Actions: \n\
        1. Race! \n\
        2. View Stats \n\
        3. Upgrades! \n\
        \n\
        0. Save and Go Back")

    #menu for Climb The Ranks upgrades
    def menuCTR_upgrades():
        print("Upgrades: \n\
        1. Prestige \n\
        2. Ultimate Prestige \n\
        3. Investment \n\
        \n\
        0. Go back")

    #main menu for multiplayer
    def Multiplayer():
        print("Multiplayer: \n\
        1. Create Lobby \n\
        2. Join Lobby \n\
        \n\
        3. Exit")

#the Functions class stores processes that happen within the main program within the Gameplay class
class Functions():

    #this is a list of bot names that are randomly selected during the Climb The Ranks mode
    bot_names = ["Armstrong","Bandit","Beast","Boomer","Casper","Centrice","Fury","Gerwin","Hollywood","Khan","Maverick","Rex",\
             "Sabertooth","Saltie","Yuri"]

    #singular nouns used in generating a phrase
    s_nouns = ["A dude", "My mom", "The king", "Some guy",\
               "A cat with rabies", "A sloth", "Your homie", "Superman"]

    #singular verbs used in generating a phrase
    s_verbs = ["eats", "kicks", "gives", "treats",\
               "meets with", "creates", "hacks", "configures",\
               "spies on", "retards", "meows on", "flees from", "tries to automate", "explodes"]

    #function the returns a string of letters of x+1 length
    def getWord(x):
        word = random.choice(string.ascii_letters) #randomly gets a letter and sets 'word' to it
        for loop in range(x):
            letter = random.choice(string.ascii_letters) #letter is given a random letter from string.ascii_letters
            word = word + letter #appends randomly generated letter to the word
        return word #returns the word to the main program

    #function for updating the highscores in highscores.txt in the directory for Time Trial mode
    def infoUpdateTT(mode,timeTaken):
        file = open("highscores.txt","r") #opens highscore.txt as file in read-mode
        lines = file.readlines() #reads the lines of the file
        for loop in range(3):
            data = lines[loop].split(",") #splits the information on the given line into the data variable 
            if data[0] == mode: #checks the mode in highscores.txt to the mode that the user played
                s = loop #sets 's' to the line the mode is on
                break
        file.close() #closes the file
        if timeTaken < float(data[3]): #if timeTaken is less than the current score, it updates
            print("Congratulations!! You beat the current best!")
            name = input("Enter your name: ") #enter name
            lines[s] = (mode + "," + name + "," + time.strftime("%d/%m/%Y") + "," + str(timeTaken) + "\n") #change the correct line in the file to the new highscore
            file = open("highscores.txt","w") #opens the highscores.txt in write-mode as file
            for loop in range(3):
                file.write(lines[loop]) #rewrites the entire file with changes
            file.close()
            print("Score updated")
        else: #otherwise it says you didn't beat the highscore
            print("It didn't beat the quickest time which is",data[3][:-1],"seconds")
        time.sleep(2)

    #getPhrase generates a random phrase using the variables set at the beginning
    def getPhrase():
        phrase = random.choice(Functions.s_nouns) + " " + random.choice(Functions.s_verbs) + " " + random.choice(Functions.s_nouns).lower() #append the randomly selected variables to phrase to generate a sentence
        return phrase #return phrase

    #CTRcompute generates the phrase using a bit of code i got online as i couldn't create a more efficient way to do so
    def CTRcompute(phrase):
        possibleCharacters = string.ascii_lowercase + string.ascii_uppercase + ' .,!?;:' #a list of possible characters that can be used in the phrase
        target = phrase #sets the target so the program knows when to stop as it 
        attemptThis = ''.join(random.choice(possibleCharacters) for i in range(len(target))) #sets a bunch of random letters to correct length of the target
        attemptNext = '' 
        completed = False
        bot_start = time.time() #starts bot time
        while completed == False: #while the the attempt is not the same as the target
            attemptNext = ''
            completed = True
            for i in range(len(target)):
                if attemptThis[i] != target[i]: #if attempt of current position, is not the same as the target of current position
                    completed = False
                    attemptNext += random.choice(possibleCharacters) #attemptNext is set to another random choice
                else:
                    attemptNext += target[i] #the attemptNext has the current letter appended if it is correct
            attemptThis = attemptNext
            time.sleep(0.035215) #pause for a small amount of time
        bot_end = time.time() #end bot time
        bot_time = round(bot_end - bot_start,3) #calculate precise bot time to 3 d.p
        return bot_time #returns bot time taken to program

    #a spinning animation that is shown when the computer is calculating the phrase
    def waiting():
        for spin in itertools.cycle(["|","/","-","\\"]):
            if Gameplay.bot_complete:
                break
            sys.stdout.write("\rWaiting for bot to finish " + spin)
            sys.stdout.flush()
            time.sleep(0.1)

    #load the save for Climb The Ranks for continuation.
    def CTRLoadSave():
        if os.path.isfile('CTRStats'):
            file = open("CTRstats","rb")
            Gameplay.CTR_stats = pickle.load(file)
            file.close()

    #update the save for Climb the Ranks when you leave the program
    def infoUpdateCTR():
        file = open("CTRstats","wb")
        pickle.dump(Gameplay.CTR_stats,file)
        file.close()


#the Gameplay class stores the modes which is then called in the main program 
class Gameplay():

    #these are variables that are used throughout the program. They are stored as local variables as they aren't need through everything, just the Gameplay class
    readInstr_TT = False
    readInstr_CTR = False
    bot_complete = False
    CTR_stats = {"Currency" : 10,"Wins" : 0,"Loses" : 0, "Lifetime_Total" : 0, "Prestiges" : 0}
    CTR_lost = False
    CTR_increase = 2
    CTR_required_prestige = 100
    CTR_loan_days = 1
    CTR_loan_payoff = False
    CTR_invest_instr = False
    CTR_invest_days = 0
    CTR_invest_run = False
    CTR_invest_streak = False

    #the code for the Time Trial code is in the TimeTrial function
    def TimeTrial():
        while True: #this while loop runs the program whilst the user doesn't change it to a different mode
            os.system('cls') #clears the cmd screen where the program is run
            if Gameplay.readInstr_TT == False: #prints instructions if the user hasn't loaded into the mode before
                Menu.instrTimeTrial() #calls instrTimeTrial from the Menu class
                Gameplay.readInstr_TT = True
            os.system('cls')
            Menu.menuTT() #prints the TimeTiral menu from the Menu class
            action = int(input("Enter a action number: ")) #asks for in input. This 'action' is used to navigate through the text menus
            if action == 1 or action == 2 or action == 3: #if a difficulty is selected
                if action == 1:
                    mode = "Easy"
                    word = Functions.getWord(4) #uses getWord from the Functions class
                elif action == 2:
                    mode = "Medium"
                    word = Functions.getWord(9)
                elif action == 3:
                    mode = "Hard"
                    word = Functions.getWord(14)
                os.system('cls')
                Menu.launching() #prints the launching sequence from the Menu class
                print(word)
                start = time.time() #start time for user
                attempt = input() #input attempt
                end = time.time() #end time for user
                timeTaken = round(end - start,3) #calculate time taken to 3 d.p.
                if attempt == word: #if they got it correct
                    print("You copied the word in",timeTaken,"seconds")
                    Functions.infoUpdateTT(mode,timeTaken) #uses infoUpdateTT in Functions to compare the current highscore and the users scores to see who was faster
                else: #if the attempt doesn't match the target
                    print("It took you",timeTaken,"seconds to get it wrong")
                time.sleep(3) #pause so the user has time to read the screen before going back to the previous menu
            elif action == 9: #action selected for 'Display Highscores'
                os.system('cls')
                print("Current Highscores")
                print("*********************")
                file = open("highscores.txt","r") #opens highscores.txt in read-mode
                lines = file.readlines() #reads the file lines
                for loop in range(3): #for each line
                    data = lines[loop].split(",") #split data
                    data[3] = data[3][:-1]
                    print(data[0],":",data[3],"seconds. Held by",data[1],"-",data[2]) #prints the highscores for the line in a given format
                input("Press enter to go back")
            elif action == 0: #if the user wants to exit Time Trial and go back to the main menu
                os.system('cls') #clear screen
                print("Returning to Main Menu")
                time.sleep(1) #sleep for a second before changing menu
                break
            else: #if the user doesn't enter a valid number, the program requests for another input
                print("Enter valid action number")
                print("\n")
                Menu.menuTT()

    #the code for the Climb The Ranks mode, stored in the ClimbTheRanks function
    def ClimbTheRanks():
        Functions.CTRLoadSave() #uses the CTRLoadSave function within the Functions class to see if there is a previous save and load it if their is
        os.system('cls')
        if Gameplay.readInstr_CTR == False: #checks if the user has loaded into the gamemode in this instance of the program already, if they haven't it prints the instructions. If they have, it doesn't display them
            Menu.instrCTR() #print the Climb The Ranks menu
            Gameplay.readInstr_CTR = True
        while True: #runs whilst the user doesn't exit the mode
            try: #uses a try except function to ensure that the input is an integer
                os.system('cls')
                Menu.menuCTR() #prints menu for CTR
                action = int(input("Enter action number: ")) #asks for action number
            except ValueError: #if the input isn't an integer
                print("Enter a number")
            else: #if the input is an integer
                if action == 1: #if the user selects 'Race'
                    if Gameplay.CTR_lost == False: #checks if the user has lost all their money, if they have they can't race
                        os.system('cls')
                        phrase = Functions.getPhrase() #uses the getPhrase function from Functions to generate a random phrase
                        while True: #while loop for try except evaluation for integers as commented on before
                            try:
                                print("Bank Total: $" + str(Gameplay.CTR_stats["Currency"])) #prints total in bank that the user is able to bet
                                bet_money = int(input("Enter how much you are willing to bet: ")) #bet that the user is willing to place
                            except ValueError:
                                print("Enter valid amount")
                                time.sleep(1)
                                os.system('cls')
                            else:
                                if bet_money > Gameplay.CTR_stats["Currency"]: #if the user has tried to bet more than they have
                                    print("You don't have that much to bet!!")
                                    time.sleep(1)
                                    os.system('cls')
                                elif bet_money < 0: #if the user tries to bet a negative amount of money
                                    print("You can't bet negative money!")
                                    time.sleep(1)
                                    os.system('cls')
                                else: #if the user has bet a amount that is >= 0 and <= total in bank, the program breaks out of the while loop
                                    break
                        Gameplay.CTR_stats["Currency"] -= bet_money #the bet money is removed from the player
                        Menu.launching() #prints lanuching sequence from Menu class
                        print(phrase) #prints phrase
                        start = time.time() #start of users time
                        user_attempt = input() #users attempt
                        end = time.time() #end of users time
                        user_TimeTaken = round(end - start,3) #calculate users time to 3 d.p.
                        print("It took you",user_TimeTaken,"seconds to fill the phrase") #display how long it took the usere
                        waiting_thread = threading.Thread(target=Functions.waiting) #create a thread that displays the spinner whilst the bot is computing the phrase
                        waiting_thread.start() #start the thread
                        bot_time = Functions.CTRcompute(phrase) #waits for computer to complete the phrase then recieves the time it took for the bot to complete
                        Gameplay.bot_complete = True #sets bot_complete to True. This is used so the for loop in the waiting function in Functions class to stop the spinner and break. Stopping the thread.
                        time.sleep(0.2) #pause for a small amount of time so the spinner stops
                        Gameplay.bot_complete = False #sets bot_complete to false so the spinner is able to be active again, otherwise it will break before the bot is complete
                        print("\nIt took",random.choice(Functions.bot_names),bot_time,"seconds to fill the phrase") #randomy choose a bot name, then print how long it took it to complete
                        if user_attempt != phrase: #if user didn't get the phrase correct
                            print("You didn't get the phrase right! \nYou lose all your bet")
                            bet_money = 0 #resets bet_money
                            Gameplay.CTR_stats["Loses"] += 1 #adds a lose to the profile
                            if Gameplay.CTR_invest_run: #if the user has invested money, if removes the investment as they didn't meet the requirements
                                    print("You failed to get the streak")
                                    time.sleep(1)
                                    Gameplay.CTR_invest_run = False #removes the investment if the user had one running
                        elif user_TimeTaken < bot_time: #if the user beat the bot
                            print("You beat the bot!!!")
                            print(str(Gameplay.CTR_increase) +"x bet returned") 
                            Gameplay.CTR_stats["Currency"] += round(bet_money*Gameplay.CTR_increase,0) #returns the bet with the multiplier applied
                            Gameplay.CTR_stats["Lifetime_Total"] += (round(bet_money*Gameplay.CTR_increase,0)-bet_money) #adds money to the total earnt in the lifetime of the game
                            Gameplay.CTR_stats["Wins"] += 1 #adds a win to the profile
                            if Gameplay.CTR_invest_run: #if they are running an investment
                                Gameplay.CTR_invest_days += 1 #adds a day to the win streak
                                if Gameplay.CTR_invest_days >= invest_streak_goal and Gameplay.CTR_invest_streak: #if the have reached the goal days
                                        print("You achieved you goal!")
                                        print("Money added!")
                                        Gameplay.CTR_stats["Currency"] += (round(invest_money * invest_multiplier,0)) #adds the money with a multiplier to your bank balance
                                        Gameplay.CTR_stats["Lifetime_Total"] += (round(invest_money*invest_multiplier,0)-invest_money) #adds the money to Lifetime total earnt
                                        time.sleep(2)
                                        Gameplay.CTR_invest_days = 0 #resets CTR_invest_days
                                        Gameplay.CTR_invest_run = False #resets CTR_invest_run
                                        Gameplay.CTR_invest_streak = False #resets CTR_invest_streak
                        elif user_TimeTaken == bot_time: #if you and the bot get the same time
                            print("You drew. Money returned")
                            Gameplay.CTR_stats["Currency"] += bet_money #returns your bet money
                        else:
                            print("The bot beat you. Bet money lost")
                            bet_money = 0 #resets bet_money
                            Gameplay.CTR_stats["Loses"] += 1 #adds a lose to your profile
                            Gameplay.CTR_invest_streak = False #resets CTR_invest_streak
                            if Gameplay.CTR_invest_run: 
                                    print("You failed to get the streak")
                                    time.sleep(1)
                                    Gameplay.CTR_invest_run = False
                        if Gameplay.CTR_loan_payoff: #if you are paying off a loan
                            if Gameplay.CTR_loan_days < 3: #it checks if you have met the three day repayment time
                                Gameplay.CTR_loan_days += 1 #if you haven't, adds another day to CTR_loan_days
                            else: #when you have reached 3 days for paying off the loan
                                Gameplay.CTR_loan_days = 1  #loan days reset
                                Gameplay.CTR_stats["Currency"] -= loan #remove loan amount taken 
                                loan = 0 #reset loan amount
                                Gameplay.CTR_loan_payoff = False #reset CTR_loan_payoff
                                print("Loan has been paided off")
                        if Gameplay.CTR_stats["Currency"] <= 0: #if the Currency is less than 0
                            print("You have lost all your money and cannot proceed any further")
                            print("You are able to view your stats in the menu but not race")
                            time.sleep(3)
                            Gameplay.CTR_lost = True #stops them from playing the game
                        input("Press enter to return to menu")
                    else:
                            print("You are unable to do that")
                            time.sleep(1)
                elif action == 2: #if the user chooses to enter the 'View stats' menu
                    os.system('cls')
                    print("Total in Bank: $" + str(Gameplay.CTR_stats["Currency"])) #prints total in bank
                    print("Lifetime Earnings: $" + str(Gameplay.CTR_stats["Lifetime_Total"])) #prints lifetime earnings
                    print("Wins: " + str(Gameplay.CTR_stats["Wins"])) #prints wins
                    print("Loses: " + str(Gameplay.CTR_stats["Loses"])) #prints loses
                    print("Prestiges: " + str(Gameplay.CTR_stats["Prestiges"])) #prints times prestiged
                    back = input("\nPress Enter to go back")
                    if back.upper() == "LOAN" and Gameplay.CTR_lost == True and Gameplay.CTR_loan_payoff == False: #hidden loan featured
                        os.system('cls')
                        print("Loan!!!")
                        print("You have the ablilty to get a loan when you have no money left")
                        try: #try except for making sure the loan entered is an integer
                            loan = int(input("Please enter loan amount: "))
                        except ValueError:
                            print("Enter valid amount")
                        else:
                            if loan > 100:
                                print("Loan too high, maximum loan is £100")
                            elif loan < 0:
                                print("You can't have negative money!")
                            else:
                                print("After 3 games this money will taken from your account to play back")
                                print("Use the money wisely")
                                input("Press enter to go back")
                                Gameplay.CTR_stats["Currency"] += loan #add the loan to the bank balance
                                Gameplay.CTR_lost = False #reset CTR_lost so that the user can play again
                                Gameplay.CTR_loan_payoff = True  #set CTR_loan_payoff so the user has to pay off the loan
                elif action == 3: #if the user chooses the enter the 'Upgrades' menu, this will be ran
                    while True:
                        try: #try except to ensure the 'action' is an integer
                            os.system('cls')
                            Menu.menuCTR_upgrades() #print menuCTR_upgrades from the Menu class
                            action = int(input("Enter action number: ")) #asks for action number
                        except ValueError: #if the entered value creates an ValueError
                            print("Enter a number")
                        else:
                            if action == 1: #if the user wishes to prestige to increase their multiplier
                                if Gameplay.CTR_stats["Currency"] > Gameplay.CTR_required_prestige: #if bank balance is greater than what is required to prestige
                                    if Gameplay.CTR_stats["Prestiges"] == 0: #if they haven't prestiged before, this explains what happens when the user prestiges
                                        os.system('cls')
                                        print("Prestige!!!")
                                        print("This means you can earn more money by winning, by 0.5 increase per prestige")
                                        print("You also sacrifice money (which increases) the more you prestige")
                                        print("You can prestige countless times")
                                        print("Ultimate Prestige works in a way where the game will presitge as many times as you \
                                        can, so you aren't spending time doing it singulary. It's a bulk prestige basically.")
                                        input("Press enter to continue")
                                        os.system('cls')
                                    Gameplay.CTR_increase += 0.5 #increases the multiplier that is used when you win by 0.5
                                    print("You have prestiged! Multiplier increased to " + str(Gameplay.CTR_increase) + "x")
                                    Gameplay.CTR_stats["Prestiges"] += 1 #adds a prestige to the user profile
                                    Gameplay.CTR_stats["Currency"] -= Gameplay.CTR_required_prestige #removes the money that is spent on the prestige
                                    Gameplay.CTR_required_prestige += 50 #adds 50 to go to the next prestige
                                    time.sleep(2)
                                elif Gameplay.CTR_stats["Currency"] == Gameplay.CTR_required_prestige: #if the currency the user left is equal to how much is needed for the next prestige
                                    print("It's not recommended to prestige currently, since you would have no money left")
                                    print("Come back when you have more that the required amount")
                                    time.sleep(2)
                                else: #if the user doesn't have enough money to prestige
                                    print("You can't do that at this time")
                                    print("Try again when you have more than $" + str(Gameplay.CTR_required_prestige) + " in your bank")
                                    time.sleep(2)
                            elif action == 2: #if the user wishes to 'Ultimate Prestige' or Bulk Prestige
                                old_prestige = Gameplay.CTR_stats["Prestiges"] #stores the current prestige of the user
                                while True: #runs whilst it is possible
                                    if Gameplay.CTR_stats["Currency"] > Gameplay.CTR_required_prestige: #if the user has enough to prestige 
                                        if Gameplay.CTR_stats["Prestiges"] == 0: #inform the user on what prestiges do if they haven't prestiged before
                                            os.system('cls')
                                            print("Ultimate Prestige!!!")
                                            print("This means you can earn more money by winning, by 0.5 increase per prestige")
                                            print("You also sacrifice money (which increases) the more you prestige")
                                            print("You can prestige countless times")
                                            print("Ultimate Prestige works in a way where the game will presitge as many times as you \
                                            can, so you aren't spending time doing it singulary. It's a bulk prestige basically.")
                                            input("Press enter to continue")
                                            os.system('cls')
                                        Gameplay.CTR_increase += 0.5
                                        Gameplay.CTR_stats["Prestiges"] += 1
                                        Gameplay.CTR_stats["Currency"] -= Gameplay.CTR_required_prestige
                                        Gameplay.CTR_required_prestige += 50
                                    else: #when the user can not prestige any further
                                        print("Multiplier increased to " + str(Gameplay.CTR_increase) + "x")
                                        print("You have prestiged " + str(Gameplay.CTR_stats["Prestiges"] - old_prestige) + " times")
                                        time.sleep(3)
                                        break
                            elif action == 3: #if the user chooses to invest money
                                if Gameplay.CTR_invest_instr == False: #if they haven't invested before, it prints instructions.
                                    os.system('cls')
                                    print("Investments!!!!")
                                    print("With these you place money to one side that then has an increased multiplier")
                                    print("However in order to get this increased multiplier you need a 'win streak'")
                                    print("which is determined by you at the start. The lower the streak goal the lower the multiplier")
                                    input("Press enter to continue")
                                    Gameplay.CTR_invest_instr = True #sets CTR_invest_instr to True so the program can register a investment is being run
                                if not Gameplay.CTR_invest_run and Gameplay.CTR_stats["Currency"] > 0: #if a investment isn't already running and there is enough currency to place an investment
                                    while True:
                                        try: #try except to check investment input
                                            os.system('cls')
                                            print("Bank Total: $" + str(Gameplay.CTR_stats["Currency"]))
                                            invest_money = int(input("Enter how much you want to invest: ")) #ask for investment amount
                                        except ValueError: #if the entered value isn't a integer
                                            print("Enter valid amount")
                                            time.sleep(1)
                                        else:
                                            if invest_money > Gameplay.CTR_stats["Currency"]: #if the money they want to invest is greater than the money they have total
                                                print("You don't have that much to invest!!")
                                                time.sleep(1)
                                            elif invest_money < 0: #if they try to invest negative money
                                                print("You can't invest negative money!")
                                                time.sleep(1)
                                            elif (Gameplay.CTR_stats["Currency"] - invest_money) == 0: #if they invest all their money
                                                print("Invalid amount since you would have no money left")
                                                time.sleep(1)
                                            else: #if they invest a valid amount of money
                                                break
                                    invest_multiplier = (invest_money / Gameplay.CTR_stats["Currency"]) * 10 #calculates a investment multiplier based on what percent of money you invest
                                    Gameplay.CTR_stats["Currency"] -= invest_money #remove the money invested from your bank account
                                    while True:
                                        try: #try except to check that what you enter is a integer
                                            os.system('cls')
                                            invest_streak_goal = int(input("Enter Streak Goal (min 5): "))
                                        except ValueError:
                                            print("Enter valid amount")
                                            time.sleep(1)
                                        else:
                                            if invest_streak_goal < 5:
                                                print("You have to have a higher streak!!")
                                                time.sleep(1)
                                            else:
                                                break
                                    invest_multiplier = (invest_multiplier * invest_streak_goal * Gameplay.CTR_increase) + 1 #calculate investment mutiplier further depending on what streak length you set
                                    print("You have",invest_streak_goal,"day streak goal.")
                                    print("Achieve it and get a " + str(invest_multiplier) + "x multiplier on $" + str(invest_money))
                                    input("Press enter to go back")
                                    Gameplay.CTR_invest_streak = True #set CTR_invest_streak to True, this register is the streak has been reached or not
                                    Gameplay.CTR_invest_run = True #set CTR_invest_run to True, so it is known that a investment is running
                                else:
                                    if not Gameplay.CTR_invest_streak: #if the user fails to get the streak for the investment
                                        print("You failed to get the streak")
                                        time.sleep(2)
                                        Gameplay.CTR_invest_run = False #reset CTR_invest_run to False
                            elif action == 0: #exit to the CTR menu
                                os.system('cls')
                                print("Returning to Climb The Ranks menu")
                                time.sleep(1)
                                break
                elif action == 0: #if the user leaves the CTR menu to go back to the main menu this runs
                    Functions.infoUpdateCTR() #infoUpdateCTR function runs from the Functions class. This will update the update the CTRstats file in the directory
                    os.system('cls')
                    print("Returning to Main Menu")
                    time.sleep(1)
                    break #break to main menu
                else: #if they don't enter a valid number for the action, this will run
                    print("Enter valid action number")
                    time.sleep(0.5)
            

#the Multiplayer class stores the code for the client. It also runs the server file "ST-server.py" to host the server
class Multiplayer:

    #this is the code for the menu for multiplayer. This handles actions and calling other functions.
    def menu():
        while True: #while loop that runs the multiplayer, it breaks out to go to main program
            try: #try except loop for validation
                os.system('cls')
                Menu.Multiplayer() #prints the multiplayer menu from the Menu class
                action = int(input("Enter action number: ")) #enter action number from the Menu
            except ValueError:
                print("Enter a valid input")
                time.sleep(0.5)
            else: #if the menu option is valid
                if action == 1: #if they want to host the server
                    Multiplayer.Server() #start server from the class
                elif action == 2: #if they want to join a lobby that already exists
                    Multiplayer.Client() #start client
                elif action == 3: #if they wish to go back to main menu
                    print("Returning to Main Menu")
                    time.sleep(1)
                    break #break out of the loop
                else: #if they enter a number that doesn't have an action associated with it
                    print("Enter a valid number")
                    time.sleep(0.5)
                

    #server function, starts the server then loads into the client
    def Server():
        os.system('cls')
        print("Server launching...")
        os.startfile("ST-server.py") #start the "ST-server.py" file in directory. This starts the server
        time.sleep(1)
        os.system('cls')
        print("Server live. Client starting..")
        time.sleep(2)
        Multiplayer.Client() #loads into the client

        

    #client function, create the client within the main program.
    def Client():
        os.system('cls')
        host = socket.gethostbyname(socket.gethostname()) #get host ip
        port = int(input("Input port: ")) #user enters a port that they wish to use to connect

        #create a client socket, this will allow a connection 
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        client_socket.connect((host, port)) #connect the socket to the designated host and port

        msg = client_socket.recv(1024).decode() #recieves a "Connected" message to the client
        lobby_size = client_socket.recv(1024).decode() #recieve lobby size
        lobby_size = int(lobby_size) #sets the lobby_size to an integer
        print(msg) #print "Connected"
        time.sleep(3)
        os.system('cls')

        print("Please enter your name:")
        name = input() #enter your name
        client_socket.send(name.encode()) #sends the name to the server
        os.system('cls')

        #lobby

        print("Waiting for players..") #idle message to the user while it waits to recieve the lobby
        lobby = client_socket.recv(4096) #lobby list of names is recieved
        os.system('cls')
        names = pickle.loads(lobby) #unpickle lobby

        print("Currently in lobby: ")
        for item in names: #for name in names. item is used as name is already used
            print(item)
                
        #input to halt the program
        input("Press enter to continue")

        client_socket.send("True".encode()) #send True to continue the server to send the phrase
      
            
        

        
        phrase = client_socket.recv(1024).decode() #recieve phrase
        os.system('cls')
        Menu.launching() #launching menu
        print(phrase) #print phrase
        t_start = time.time() #start time
        attempt = input() #attempt
        t_end = time.time() #end time
        timeTaken = round(t_end - t_start,3) #calculate time taken to 3 d.p.
        timeTaken = str(timeTaken) #timeTaken converted to string so it sends through the socket
        if attempt == phrase: #if the attempt is correct
            client_socket.send(timeTaken.encode()) #send time
        else: #if they get the phrase wrong
            print("You didn't get it correct")
            client_socket.send("False".encode()) #send False if they got it wrong

        #recieve the winner from the server and decode
        winner = client_socket.recv(1024).decode()
        time.sleep(0.2)
        os.system('cls')

        #if the user logged into the client is the winner
        if name == winner:
            print("Congratulations!! You won!")
        else: #if they aren't the winner
            print("Better luck next time. Winner was",winner)
        time.sleep(5)



#main program runs in while loop
while True:
    try: #try except for input on main menu
        os.system('cls')
        Menu.menu() #print menu
        action = int(input("Enter action number: ")) #enter action number for menu navigation
    except ValueError: #if the number entered isn't an integer
        print("Enter a number")
    else: #if number entered is valid
        if action == 1: #if they want to enter time trial mode
            Gameplay.TimeTrial() #start time trial mode
        elif action == 2: #if they want to enter Climb The Ranks mode
            Gameplay.ClimbTheRanks() #start Climb The Ranks mode
        elif action == 3: #if the user wants to enter multiplayer
            Multiplayer.menu() #start multiplayer
        elif action == 4: #if the user wants to exit the program
            quit() #end the program
        else: #if the action entered is an integer but has nothing associated to it
            print("Enter valid action number")
            time.sleep(0.5)

