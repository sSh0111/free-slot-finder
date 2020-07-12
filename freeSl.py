dict_lab = {}
for i in range(1, 61):
    dict_lab[i] = 0


'''Initial LAB Dictionary, display re-arranged for simplified explanation

{      1: 0,  2: 0,  3: 0,  4: 0,  5: 0,  6: 0,               31: 0, 32: 0, 33: 0, 34: 0, 35: 0, 36: 0,
       7: 0,  8: 0,  9: 0, 10: 0, 11: 0, 12: 0,               37: 0, 38: 0, 39: 0, 40: 0, 41: 0, 42: 0,
      13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0,               43: 0, 44: 0, 45: 0, 46: 0, 47: 0, 48: 0,
      19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0,               49: 0, 50: 0, 51: 0, 52: 0, 53: 0, 54: 0,
      25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0,               55: 0, 56: 0, 57: 0, 58: 0, 59: 0, 60: 0
}'''


# Test case

dict_lab =       { 1: 1,  2: 0,  3: 1,  4: 1,  5: 1,  6: 1,               31: 1, 32: 1, 33: 1, 34: 0, 35: 0, 36: 1,
                   7: 0,  8: 0,  9: 1, 10: 1, 11: 1, 12: 1,               37: 1, 38: 0, 39: 1, 40: 1, 41: 1, 42: 0,
                  13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0,               43: 1, 44: 1, 45: 1, 46: 1, 47: 0, 48: 0,
                  19: 1, 20: 1, 21: 0, 22: 0, 23: 0, 24: 0,               49: 1, 50: 1, 51: 0, 52: 1, 53: 0, 54: 0,
                  25: 0, 26: 0, 27: 1, 28: 1, 29: 1, 30: 1,               55: 1, 56: 1, 57: 1, 58: 1, 59: 0, 60: 0
}



# Function for ALL POSSIBLE GAPS

all_gaps_list = []

def all_gaps_counter(dict_lab):

    gaps = 0
    for i in range(1, 61):
        if dict_lab[i] == 0:
            gaps += 1
            all_gaps_list.append(i)
    return gaps

print()
print('Number of all free slots: ' + str(all_gaps_counter(dict_lab)))           #Calling the function
print(all_gaps_list)
print()