ie = 'ie'
cie = 'cie'
ei = 'ei'
cei = 'cei'


# while True:
#     print("What word would you like to check? Enter \'q\' to quit.")
#     checkWord = input()
#     if checkWord == 'q':
#         break

def check(checkWord):        
    if ie in checkWord:
        if cie in checkWord:
            print(checkWord + ' fails the rule.')
        else:
            print(checkWord + ' passes the rule.')
    elif ei in checkWord:
        if cei in checkWord:
            print(checkWord + ' passes the rule.')
        else:
            print(checkWord + ' fails the rule.')
    else:
        print(checkWord + ' passes the rule.')

check("a")
check("zombie")
check("transceiver")
check("veil")
check("icier")
