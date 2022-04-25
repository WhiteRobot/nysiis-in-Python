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
def NYSIIS(name, true_NYSIIS = False):
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
    
    # First character of key = first character of name.
    key = translated[0:1]
    translated = translated[1:]
    
    last_character = key
    current_character = ""
    next_append = ""
    vowels = ["A","E","I","O","U"]
    
    # Translate remaining characters by following rules, incrementing by one character each time:
    while len(translated) > 0:
        
        next_append = ""
        current_character = translated[0:1]
        
        if translated[0:2] == "EV": # EV → AF
            next_append = "AF"
        elif current_character in vowels: # else A, E, I, O, U → A
            next_append = "A"
        elif current_character == "Q": # Q → G
            next_append = "G"
        elif current_character == "Z": # Z → S
            next_append = "S"
        elif current_character == "M": # M → N
            next_append = "N"
        elif translated[0:2] == "KN": # KN → N
            next_append = "N"
        elif current_character == "K": # K → C
            next_append = "C"
        elif translated[0:3] == "SCH": # SCH → SSS
            next_append = "SSS"
        elif translated[0:2] == "PH": # PH → FF
            next_append = "FF"
        elif current_character == "H" and (last_character not in vowels or translated[1:2] not in vowels): # H → If previous or next is non-vowel, previous.
            next_append = last_character
        elif current_character == "W" and last_character in vowels: # W → If previous is vowel, A.
            next_append = "A"
        elif current_character != last_character:
            next_append = current_character
        
        if next_append != key[-1:]: # Add current to key if current is not same as the last key character.
            key += next_append
        
        last_character = current_character
        translated = translated[max(len(next_append),1):]
        
    #end while
    
    if key[-1:] in ['S', 'A']: # If last character is S, remove it. If last character is A, remove it.
        key = key[0:-1]
    elif key[-2:] == "AY": # If last characters are AY, replace with Y.
        key = key[0:-2] + "Y"
    
    # If longer than 6 characters, truncate to first 6 characters. (only needed for true NYSIIS, some versions use the full key)
    if true_NYSIIS:
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