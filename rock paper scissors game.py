import random

rps = ["rock", "paper", "scissors"]
player = None
computer = random.choice(rps)

choice = input("what do you pick (rock, paper, or scissors)?: ")
print (f"your choice was: {choice}")
print (f"the computer picked: {computer}")
beats = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper"
}
if choice == computer:
    print ("wow we picked the same choice!")
elif beats.get(choice) == computer:
    print ("you win")
else:
    print ("you lose")

