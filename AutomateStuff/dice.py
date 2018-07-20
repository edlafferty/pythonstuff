from random import randint

keepRolling = True
while keepRolling:
    print('What are you rolling? Enter \'q\' to quit')
    rollinput = input()
    if rollinput == 'q':
        keepRolling = False
        break
    rolls = rollinput.split("d")
    print(rolls)
    for x in range(int(rolls[0])):
        print('Result ' + str(x + 1) + ': ' + str(randint(1,int(rolls[1]))))