from PIL import Image
import json
import numpy as np
# import preproc_beta
import os
import datetime
import sys
from flask import Flask
app = Flask(__name__)


##THIS ONE TAKES 2 ms


def dist(f, t):
    return int((abs(f[0] - t[0]) * 2 + abs(f[1] - t[1]) * 2 + abs(f[2] - t[2])) * 0.5)


def unimportant(rgb):
    return (rgb[0] <= 200 and rgb[1] <= 200 and rgb[2] <= 200) or (rgb[1] > 200 and rgb[2] > 200 and rgb[2] >= rgb[1])

cd = [0, 0]

def updateNPCoord():
    global cd
    if cd[1] < 12:
        cd = [cd[0], cd[1] + 1]
    else:
        cd = [cd[0] + 1, 0]




@app.route('/<path:myPath>')
def main(myPath):


    slot_state = np.zeros((14, 13))
    hops = []
    final_list = []

    tt = Image.open(myPath).rotate(180)
    # tt = Image.open(sys.argv[1]).rotate(180)
    # tt = Image.open("ttpxt.png")
    #tt = Image.open("ttpxt.png").rotate(180)

    # print(datetime.datetime.time(datetime.datetime.now()))

    dim = tt.size





    '''
    filled slot = (0,255,0)
    empty slot = (255,255,0)
    '''
    cols = [(0, 255, 0), (255, 255, 0)]

    start = []  ##coordinates of the starting point

    i = 0
    while i < dim[0]:
        j = 0
        while j < dim[1]:
            rgb = tt.getpixel((i, j))
            if unimportant(rgb) == False:
                start = [i, j]
                i = dim[0]  # breaking the outer loop
                break  # breaking the inner loop
            j = j + 1
        i = i + 1

    j = start[1]
    i = start[0]

    try:
        for b in range(14):

            for a in range(13):
                RGB = tt.getpixel((i, j))
                if unimportant(RGB) == False:
                    if dist((203, 254, 51), RGB) < dist((255, 255, 204), RGB):
                        slot_state[cd[0], cd[1]] = 1

                updateNPCoord()

                if a == 12:
                    break

                if b == 0:
                    h = 1
                    i = i + 1
                    while unimportant(tt.getpixel((i, j))) == False:
                        i = i + 1
                        h = h + 1
                    while unimportant(tt.getpixel((i, j))) == True:
                        i = i + 1
                        h = h + 1
                    hops.append(h)
                else:
                    i = i + hops[a]

            # printing
            # for x in range(13):
            #    print(int(slot_state[b][a]), end=' ')
            # print('\n')

            if b == 13:
                break

            i = start[0]
            j = j + 1
            while unimportant(tt.getpixel((i, j))) == False:
                j = j + 1
            while unimportant(tt.getpixel((i, j))) == True:
                j = j + 1

    except IndexError:
        if cd[0] < 10 or cd[1] != 0:
            return("BAD FILE: Please upload a proper time table image...")


    ##in case of a correctly cropped image, empty rows need be added to the top
    ##of the table, before rotation
    for x in range(14 - cd[0]):
        tr = np.zeros(13)
        i = 13
        while i >= 1:
            slot_state[i] = slot_state[i - 1]
            i = i - 1
        slot_state[0] = tr

    ##rotating the array
    slot_state = np.rot90(slot_state, 2, (0, 1))

    a = 0
    while a < 13:
        b = 0
        while b < 13:
            final_list.append(int(slot_state[a, b] + slot_state[a + 1, b]))
            b = b + 1
        a = a + 2

    f = []
    for i in range(0, 5):
        f.append([])
        for j in range(0, 22):
            f[i].append(0)
    k = 0
    for i in range(0, 10, 2):
        if slot_state[i][0] == 0 and slot_state[i + 1][0] == 0:
            f[k][0] = 1
        if slot_state[i][0] == 0 and slot_state[i + 1][0] == 0 and slot_state[i + 1][1] == 0:
            f[k][1] = 1
        if slot_state[i][1] == 0 and slot_state[i + 1][1] == 0:
            f[k][2] = 1
        if slot_state[i][1] == 0:
            f[k][3] = 1
        if slot_state[i][2] == 0 and slot_state[i + 1][2] == 0:
            f[k][4] = 1
        if slot_state[i][2] == 0 and slot_state[i + 1][2] == 0 and slot_state[i + 1][3] == 0:
            f[k][5] = 1
        if slot_state[i, 3] == 0 and slot_state[i + 1][3] == 0:
            f[k][6] = 1
        if slot_state[i][3] == 0 and slot_state[i + 1][4] == 0:
            f[k][7] = 1
        if slot_state[i][4] == 0 and slot_state[i + 1][4] == 0 and slot_state[i + 1][5] == 0:
            f[k][8] = 1
        if slot_state[i][4] == 0 and slot_state[i + 1][5] == 0:
            f[k][9] = 1
        if slot_state[i][6] == 0 and slot_state[i + 1][6] == 0:
            f[k][10] = 1
        if slot_state[i][6] == 0 and slot_state[i + 1][6] == 0 and slot_state[i + 1][7] == 0:
            f[k][11] = 1
        if slot_state[i][7] == 0 and slot_state[i + 1][7] == 0:
            f[k][12] = 1
        if slot_state[i][7] == 0:
            f[k][13] = 1
        if slot_state[i][8] == 0 and slot_state[i + 1][8] == 0:
            f[k][14] = 1
        if slot_state[i][8] == 0 and slot_state[i + 1][8] == 0 and slot_state[i + 1][9] == 0:
            f[k][15] = 1
        if slot_state[i][9] == 0 and slot_state[i + 1][9] == 0:
            f[k][16] = 1
        if slot_state[i][9] == 0 and slot_state[i + 1][10] == 0:
            f[k][17] = 1
        if slot_state[i][10] == 0 and slot_state[i + 1][10] == 0 and slot_state[i + 1][11] == 0:
            f[k][18] = 1
        if slot_state[i][10] == 0 and slot_state[i + 1][11] == 0:
            f[k][19] = 1
        if slot_state[i][12] == 0:
            f[k][20] = 1
        if slot_state[i][12] == 0:
            f[k][21] = 1
        k = k + 1

    # print(datetime.datetime.time(datetime.datetime.now()))
    # os.remove("ttpxt.png")
    # print(json.dumps(final_list))
    """l = []
    mor=0
    eve=0
    free_slot_dict = {}
    i = 0
    for y in final_list:
        if (i == 0):
            s = "Monday"
            # print("\n")
            # print(s)
        elif (i == 13):
            # print(l)
            s = "Tuesday"
            free_slot_dict["Monday"] = l
            l = []

            # print("\n")
            # print(s)
        elif (i == 26):
            # print(l)
            free_slot_dict["Tuesday"] = l
            l = []
            s = "Wednesday"
            # print("\n")
            # print(s)
        elif (i == 39):
            # print(l)
            free_slot_dict["Wednesday"] = l
            l = []
            s = "Thrusday"
            # print("\n")
            # print(s)
        elif (i == 52):
            # print(l)
            free_slot_dict["Thursday"] = l
            l = []
            s = "Friday"
            # print("\n")
            # print(s)

        if (y == 0):
            if (i % 13 == 0):
                # print("8:00-9:00 ")
                l.append("8:00-9:00")
                mor+=1
            if (i % 13 == 1):
                # print("9:00-10:00 ")
                l.append("9:00-10:00 ")
                mor+=1
            if (i % 13 == 2):
                # print("10:00-11:00 ")
                l.append("10:00-11:00 ")
                mor+=1
            if (i % 13 == 3):
                # print("11:00-12:00 ")
                l.append("11:00-12:00 ")
                mor+=1
            if (i % 13 == 4):
                # print("12:00-13:00 ")
                l.append("12:00-13:00 ")
                mor+=1
            if (i % 13 == 5):
                # print("13:00-14:00 ")
                l.append("13:00-14:00 ")
            if (i % 13 == 6):
                # print("14:00-15:00 ")
                l.append("14:00-15:00 ")
                eve+=1
            if (i % 13 == 7):
                # print("15:00-16:00 ")
                l.append("15:00-16:00 ")
                eve+=1
            if (i % 13 == 8):
                # print("16:00-17:00 ")
                l.append("16:00-17:00 ")
                eve+=1
            if (i % 13 == 9):
                # print("17:00-18:00 ")
                l.append("17:00-18:00 ")
                eve+=1
            if (i % 13 == 10):
                # print("18:00-18:50 ")
                l.append("18:00-18:50 ")
                eve+=1
            if (i % 13 == 11):
                # print("18:50-19:00 ")
                l.append("18:50-19:00 ")
            if (i % 13 == 12):
                # print("19:00-20:00 ")
                l.append("19:00-20:00 ")

        if (i == 64):
            # print(l)
            free_slot_dict["Friday"] = l
            break
        i = i + 1
    
    # print(final_list)
    # print(f)
    # print(free_slot_dict)
    #print(json.dumps(free_slot_dict))
    free_slot_dict["Free slots in"] = "morning" if mor>eve else "evening"
    """
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    free_s = {}
    l = []
    d = 0
    for i in f:
        if i[0] == 1 and i[1] == 1:
            l.append("8:00-9:00")
        if i[2] == 1 and i[3] == 1:
            l.append("9:00-10:00")
        if i[2] == 0 and i[3] == 1:
            l.append("9:30-10:00")
        if i[4] == 1 and i[5] == 1:
            l.append("10:00-11:00")
        if i[6] == 1 and i[7] == 1:
            l.append("11:00-12:00")
        if i[6] == 0 and i[6] == 1:
            l.append("11:30-12:00")
        if i[8] == 1 and i[9] == 1:
            l.append("12:00-13:00")
        if i[10] == 1 and i[11] == 1:
            l.append("14:00-15:00")
        if i[12] == 1 and i[13] == 1:
            l.append("15:00-16:00")
        if i[12] == 0 and i[13] == 1:
            l.append("15:30-16:00")
        if i[14] == 1 and i[15] == 1:
            l.append("16:00-17:00")
        if i[16] == 1 and i[17] == 1:
            l.append("17:00-18:00")
        if i[16] == 0 and i[17] == 1:
            l.append("17:30-18:00")
        if i[18] == 1 and i[19] == 1:
            l.append("18:00-19:00")
        if i[20] == 1 and i[21] == 1:
            l.append("19:00-20:00")
        free_s[days[d]] = l
        d += 1
        l = []

    #print(free_s)
    return(json.dumps(free_s))

@app.route('/')
def index():
    return '<h2>Please enter file path in the URL</h2>'

if __name__=="__main__":
    app.run(debug=True)

