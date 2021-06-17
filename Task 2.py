import csv
import random
import operator

players = []


class Player():

    # Player class used for holding the point values of each player

    def __init__(self):
        self.score = 0
        self.name = ""

    def rollDice(self):
        """

        Roll two dice and adds the total to the players score

        """
        roll = random.randint(1, 6)
        self.score += roll
        roll2 = random.randint(1, 6)
        self.score += roll2
        return "\n" + self.name + " rolled a " + str(roll) + " and a " + str(roll2) + "\n" + str(
            self.calculateAddOnScore(roll, roll2)) + "\n"

    def calculateAddOnScore(self, roll, roll2):
        """
`
        Calculates the additional score to be added after the user has rolled
    

        """
        total = roll + roll2
        if roll == roll2:
            extraRoll = random.randint(1, 6)
            self.score += extraRoll
            return self.name + " rolled a double: EXTRA ROLL\nYour extra roll gave you " + str(extraRoll) + "points"
        elif total % 2 == 0:
            self.score += 10
            return self.name + " rolled an even total: Extra 10 points"
        else:
            if self.score - 5 < 0:
                self.score = 0
                return self.name + " rolled an odd total: Minus 5 points"
            else:
                self.score -= 5
                return self.name + " rolled an odd total: Minus 5 points"


def showLeaderboard():
    # fucntion that displays the top 5 leaderboard in descending order
    with open("winners.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        print("\n")
        leaderboard = []
        for row in reader:
            leaderboard.append(row)
        csvfile.close()
    sortedLeaderboard = sorted(leaderboard, key=lambda k: k["Score"])
    top5 = sortedLeaderboard[-5:]
    return top5[::-1]


def saveToCsv(account, password):
    # procedure saving usernames and paswords to a csv file
    with open("users.csv", "a") as csvfile:
        fieldnames = ["username", "password"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({"username": account, "password": password})
        csvfile.close()


def saveWinnerToCsv(winner, points):
    # procedure to save winner of the game to a csv file
    with open("winners.csv", "a") as csvfile:
        fieldnames = ["Name", "Score"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({"Name": winner, "Score": str(points)})
        csvfile.close()


def login():
    # function for authenticating users
    userAuthenticated = False
    while not userAuthenticated:
        user = input("Username:")
        passw = input("Password:")
        with open("users.csv") as csvFile:
            readLines = csv.DictReader(csvFile)
            for row in readLines:
                if (row["username"] == user) and (row["password"] == passw):
                    print("Login Succesful")
                    if len(players) == 0:
                        global player1

                        player1 = Player()
                        player1.name = user
                    elif len(players) == 1:
                        ###This check to see if the first player object exists
                        global player2
                        player2 = Player()
                        player2.name = user  ###If it does not exist then player1 object is craeted
                        ###If player1 exists then player2 is created

                    players.append(row["username"])
                    userAuthenticated = True
                    if len(players) == 1:
                        print("One player authentictated, Please login with another account")
                    return True

            print("Invalid credentials")
            print("If you do not have an account please regsiter")
            return False


def userNameIsAvailable(username):
    # function checking if a username has been taken
    # returns True if username does exist
    with open("users.csv") as csvFile:
        readLines = csv.DictReader(csvFile)
        for row in readLines:
            if username == row["username"]:
                return False
    return True


def register():
    # function to register users
    print("Register for dice roll game")
    while True:
        regName = input("Username:\n>>>")
        if not userNameIsAvailable(regName):
            # calls function to check if name is available
            print("Username has already been chosen, try a different one!")
        else:
            print("Username is available!")
            regPass = input("Password\n>>>")
            saveToCsv(regName, regPass)
            print("Account Created\nYour Username is: " + regName + "\nYour Password is: " + regPass)
            break


def printGameOverScreen():
    # procedure to display the game over text
    print("""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                        Game Over                          +
+                        {}'s points: {}                  +
+                        {}'s points: {}                   +
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++""".format(player1.name, player1.score, player2.name,
                                                                       player2.score))


def displayRound(roundNumber):
    # procedure to display text reffering to the current
    """
    print("========================Round "+str(roundNumber)+"==========================")
    print("====================={}'s Points: {} =========================".format(player1.name, player1.score))
    print("====================={}'s Points: {} =========================".format(player2.name, player2.score))
"""

    print("""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                        Round {}                           +
+                        {}'s points: {}                  +
+                        {}'s points: {}                   +
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++""".format(str(roundNumber), player1.name, player1.score,
                                                                       player2.name, player2.score))


def mainGame():
    # Intro to the game
    print("====================Dice Rolling Game====================")
    for x in range(1, 6):
        # for loop that will loop 5 times because in a normal game there will be 5 rounds
        displayRound(x)
        input(players[0] + "'s turn to roll\nPress Enter to roll")
        print(player1.rollDice())
        input(players[1] + "'s turn to roll\nPress Enter to roll")
        print(player2.rollDice())
    while player1.score == player2.score:
        # this trigger if the scores are the same after the 5 rounds. If they are not it goes to a tiebreaker round to determine the winner.
        y = 6
        displayRound(y)
        input(players[0] + "'s turn to roll\nPress Enter to roll")
        print(player1.rollDice())
        input(players[1] + "'s turn to roll\nPress Enter to roll")
        print(player2.rollDice())
        y += 1
    # This dertimens if player 1 wins and produces a victory message
    if player1.score > player2.score:
        printGameOverScreen()

        print("=================WINNER " + player1.name + "=================")
        print("==============SCORED: " + str(player1.score) + "==============")
        saveWinnerToCsv(player1.name, player1.score)
    if player1.score < player2.score:
        printGameOverScreen()
        print("=================WINNER " + player2.name + "=================")
        print("==============SCORED: " + str(player2.score) + "==============")
        saveWinnerToCsv(player2.name, player2.score)


while True:
    if len(players) == 2:
        print("Welcome " + player1.name + " and " + player2.name)
        mainGame()
        break
    option = input("Sign Up - S\nLog in - L\nView Leaderboard - V\n>>>").lower()
    if option.lower() == "l":
        login()
    elif option.lower() == "s":
        register()
    elif option.lower() == "v":
        print(showLeaderboard())
    else:
        print("!!!!\nIncorrect option\n!!!!")
