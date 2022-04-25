#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, getopt

"""
https://en.wikipedia.org/w/index.php?title=New_York_State_Identification_and_Intelligence_System&oldid=814240898

Translate first characters of name: MAC → MCC; KN → NN; K → C; PH, PF → FF; SCH → SSS
Translate last characters of name: EE, IE → Y; DT, RT, RD, NT, ND → D
First character of key = first character of name.
Translate remaining characters by following rules, incrementing by one character each time:
    EV → AF else A, E, I, O, U → A
    Q → G; Z → S; M → N
    KN → N else K → C
    SCH → SSS; PH → FF
    H → If previous or next is non-vowel, previous.
    W → If previous is vowel, A.
    Add current to key if current is not same as the last key character.
If last character is S, remove it.
If last characters are AY, replace with Y.
If last character is A, remove it.
Append translated key to value from step 3 (removed first character)
If longer than 6 characters, truncate to first 6 characters. (only needed for true NYSIIS, some versions use the full key)
"""
def NYSIIS(name, trueNYSIIS=False):
    translated = name.upper()
    
    # Translate first characters of name: MAC → MCC; KN → NN; K → C; PH, PF → FF; SCH → SSS
    if translated[0:3] == 'MAC':
        translated = "MCC" + translated[3:]
    elif translated[0:2] == 'KN':
        translated = "NN" + translated[2:]
    elif translated[0:1] == 'K':
        translated = "C" + translated[-1]
    elif translated[0:2] == 'PH':
        translated = "PF" + translated[2:]
    elif translated[0:3] == 'SCH':
        translated = "SSS" + translated[3:]
    
    # Translate last characters of name: EE, IE → Y; DT, RT, RD, NT, ND → D
    if translated[-2:] in ['EE', 'IE']:
        translated = translated[0:-2] + "Y"
    elif translated[-2:] in ['DT', 'RT', 'RD', 'NT', 'ND']:
        translated = translated[0:-2] + "D"
    
    lastCharacter = translated[0:1]
    
    # First character of key = first character of name.
    key = lastCharacter
    
    translated = translated[1:]
    currentCharacter = ""
    nextAppend = ""
    vowels = ["A","E","I","O","U"]
    
    # Translate remaining characters by following rules, incrementing by one character each time:
    while len(translated) > 0:
        
        nextAppend = ""
        currentCharacter = translated[0:1]
        
        if translated[0:2] == "EV": # EV → AF
            nextAppend = "AF"
        elif currentCharacter in vowels: # else A, E, I, O, U → A
            nextAppend = "A"
        elif currentCharacter == "Q": # Q → G
            nextAppend = "G"
        elif currentCharacter == "Z": # Z → S
            nextAppend = "S"
        elif currentCharacter == "M": # M → N
            nextAppend = "N"
        elif translated[0:2] == "KN": # KN → N
            nextAppend = "N"
        elif currentCharacter == "K": # K → C
            nextAppend = "C"
        elif translated[0:3] == "SCH": # SCH → SSS
            nextAppend = "SSS"
        elif translated[0:2] == "PH": # PH → FF
            nextAppend = "FF"
        elif currentCharacter == "H" and (lastCharacter not in vowels or translated[1:2] not in vowels): # H → If previous or next is non-vowel, previous.
            nextAppend = lastCharacter
        elif currentCharacter == "W" and lastCharacter in vowels: # W → If previous is vowel, A.
            nextAppend = "A"
        elif currentCharacter != lastCharacter:
            nextAppend = currentCharacter
        
        lastCharacter = currentCharacter
        
        if nextAppend == "":
            translated = translated[1:]
            lastCharacter = key[-1:]
        else:
            if nextAppend != key[-1:]: # Add current to key if current is not same as the last key character.
                key += nextAppend
            translated = translated[len(nextAppend):]
        
    #end while
    
    if key[-1:] in ['S', 'A']: # If last character is S, remove it. If last character is A, remove it.
        key = key[0:-1]
    elif key[-2:] == "AY": # If last characters are AY, replace with Y.
        key = key[0:-2] + "Y"
    
    # If longer than 6 characters, truncate to first 6 characters. (only needed for true NYSIIS, some versions use the full key)
    if trueNYSIIS:
        return key[0:6]
    else:
        return key



def main(argv):
    name = ''
    
    try:
        opts, args = getopt.getopt(argv,"hn:",["name="])
    except getopt.GetoptError:
        print('nysiis.py -n <name>')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print('nysiis.py -n <name>')
            sys.exit()
        elif opt in ("-n", "--name"):
            name = arg
    
    print(NYSIIS(name))

if __name__ == "__main__":
    main(sys.argv[1:])