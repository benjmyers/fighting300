import os
import re
import difflib
from operator import itemgetter

def similar(seq1, seq2):
    return difflib.SequenceMatcher(a=seq1.lower(), b=seq2.lower()).ratio()

artillery = re.compile(r"ar{1}.*y{1}")
cavalry = re.compile(r"ca{1}.*y{1}")
infantry = re.compile(r"inf{1}.*y{1}")
reserves = re.compile(r"re{1}.*s{1}")
sharpshooters = re.compile(r"sh{1}.*s{1}")

def getBranch(s):
    si = infantry.search(s)
    sc = cavalry.search(s)
    sa = artillery.search(s)
    sr = reserves.search(s)
    ss = sharpshooters.search(s)
    if si:
        return ["Infantry", si.start()]
    elif sc:
        return ["Cavalry", sc.start()]
    elif sa:
        return ["Artillery", sa.start()]
    elif sr:
        return ["Reserves", sr.start()]
    elif ss:
        return ["Sharpshooters", ss.start()]
    else:
        return ["Unknown"]

states = ["Alaska", "Alabama", "Arkansas", "Arizona", "California", "Connecticut", "Delaware", "Florida", "Georgia", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "North Carolina", "New Hampshire", "New Jersey", "New York", "Ohio", "Oklahoma", "Pennsylvania", "Rhode Island", "South Carolina", "Tennessee", "Texas", "Virginia", "Vermont", "Wisconsin", "West Virginia"]
def getState(s):
    scores = []
    for state in states:
        scores.append((state,similar(s, state.lower())))
    return max(scores,key=itemgetter(1))[0]

def text2int(s):
    
    numbers = {
        'first': 1,
        'second': 2,
        'third': 3, 
        'fourth': 4,
        'fifth': 5,
        'sixth': 6,
        'seventh': 7,
        'eighth': 8,
        'ninth': 9,
        'tenth': 10,
        'eleventh': 11,
        'twelfth': 12,
        'thirteenth': 13,
        'fourteenth': 14,
        'fifteenth': 15,
        'sixteenth': 16,
        'seventeenth': 17,
        'eighteenth': 18,
        'nineteenth': 19,
        'twenty': 20,
        'twentieth': 20,
        'thirty': 30,
        'thirtieth': 30,
        'forty': 40,
        'fortieth': 40,
        'fifty': 50,
        'fiftieth': 50,
        'sixty': 60,
        'sixtieth': 60,
        'seventy': 70,
        'seventieth': 70,
        'eighty': 80,
        'eightith': 80,
        'ninety': 90,
        'ninetieth': 90,
        'onehundredand': 100
    }

    starts = []
    ends = []
    groups = []

    for key in numbers.keys():
        r = re.compile(key)
        match = r.search(s)
        if match:
            starts.append(match.start())
            ends.append(match.end())
            groups.append(match.group(0))

    result = [x for (y,x) in sorted(zip(starts, groups))]#[]
    
    # if len(starts) == 0:
    #     print(s)
    #     manual = input("Enter the number separated by ,s -> ")
    #     if manual != '':
    #         result = manual.split(",")
    # else:
    #     result = [x for (y,x) in sorted(zip(starts, groups))]
    
    
    regt = 0
    for no in result:
        regt += numbers[no]

    return [regt, ''.join(result), max(ends) if len(ends) else None]

def getRegiments():

    filepath = './pages/txt/'

    reg = re.compile(r"A{1}.*Y{1}") # This will capture INFANTRY, CAVALRY, and ARTILLERY

    for filename in os.listdir(filepath):
        if '.DS_Store' in filename:
            continue

        f = open(filepath + filename, 'r', errors='ignore')
        contents = f.read().strip().split("\n")

        if len(contents) > 2:

            ## Generally, the header information is within the top 10 lines of the stripped file
            header = list(filter(lambda x: x!= '' and x!=' ', contents[0:10]))
            
            # Find the line containing the regiment's name
            regimentRaw = list(filter(lambda x: reg.search(x) or 'RESERVES' in x or 'SHARP' in x, header))[0].lower()

            # Strip out noise from OCR
            clean = re.sub(r'([^\w]|_)+', '', regimentRaw)
            
            # Parse regiment number. Returns number, string, and end index within clean
            regNo = text2int(clean)
            startIndex = 0
            endIndex = 0
            if (regNo[0]):
                startIndex = regNo[2]

            # Get branch. Returns the branch and its start index within clean
            branch = getBranch(clean)
            if len(branch) == 2:
                endIndex = branch[1]
           
            # Using the start and end index from above to isolate the state, go get the state
            state = getState(clean[startIndex:endIndex])

            print(clean, regNo[0], state, branch[0])
            # print(" ")
        else:
            print(filename)


def main():
    getRegiments()    

if __name__ == '__main__':
    main()