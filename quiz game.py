questions = ("Who won the 2025 FIA formula one world championship?:",
             "How many wins does Lewis Hamilton have as of august 2026?:",
             "How many wins did Max Verstappen get during his dominant 2023 season?:",
             "Who has the record for the lowest pole-to-win conversion rate (among current drivers)?:",
             "Who was the winner of the 2008 british gp?:")

answers = ("A", "B", "C", "B", "D")
options = (('A: Lando Norris', 'B: Max Verstappen', 'C: Charles Leclerc', 'D: Lewis Hamilton'),
           ('A: 91', 'B: 106', 'C: 105', 'D: 110'),
           ('A: 13', 'B: 18', 'C: 19', 'D: 17'),
           ('A: Valtteri Bottas', 'B: Charles Leclerc', 'C: Sergio Perez', 'D: Nico Hulkenberg'),
           ('A: Felipe Massa', 'B: Mark Webber', 'C: Kimi Raikkonen', 'D: Lewis Hamilton'))
score = 0
question_no = 0

for question in questions:
    print("===========================================================================================================")
    print(question)
    for option in options[question_no]:
        print (option)
    question_no += 1
    ans = input("enter your answer(A/B/C/D):").upper()
    if ans in answers:
        print("you got that right!")
        score += 1
    else:
        print()
        print("youre wrong!")

print ("your score is:", score,"/ 5")
print ("the correct answers for these questions are:", answers)


