import numpy as np

opTable = dict()
riTable = dict()
dataL = list()
poolTab = dict()
poolTab["Pool TAB"] = []
sT = dict()
sT["srN"] = []
sT["address"] = []
sT["symbol"] = []
lT = dict()
lT["srN"] = []
lT["address"] = []
lT["literal"] = []
pass2 = dict()
pass2["IS"] = []
pass2["RG"] = []
pass2["add"] = []
symbolError = []
InsLen3=['01','02','03','04','05','06','08']
InsLen2=['09','10']
sn = []
snl = []
ln = []
Equ, ltN = 0, 0
data = open("input.txt", "r")
dataNew = open("Pass2_output.txt", "w")
pass2Data = open("Pass1_output.txt", "w")
for line in data:
    dataL.append(line)


def opCode(word):  # mnemonic opcode table
    opTable = {'STOP': '00', 'ADD': '01', 'SUB': '02',
               'MULT': '03', 'MOVER': '04',
               'MOVEM': '05', 'COMP': '06', 'BC': '07',
               'DIV': '08', 'READ': '09', 'PRINT': '10'}

    for i in opTable:  # return opcode value of mnemonic
        if (word == i):
            return opTable[word]
            break
    else:
        return -1


def rTble(word):  # Register Table
    riTable = {'AREG': '1', 'BREG': '2',
               'CREG': '3', 'DREG': '4'}
    for i in riTable:
        if (word == i):
            return riTable[word]  # Return Resister code
            break
    else:
        return -1


def dTable(word):  #
    dcTable = {'DC': '01', 'DS': '02'}
    for i in dcTable:
        if word == i:
            return dcTable[word]
            break
    else:
        return -1


def cTable(word):
    csTable = {'LT': '1', 'LE': '2', 'EQ': '3', 'GT': '4', 'GE': '5', 'ANY': '6'}
    if word in csTable:
        return csTable[word]
    else:
        return -1


def lAssign():
    dataNew.write("(AD 04) ")
    dataNew.write("\n")


def sTable(sN, word, n=0, addr=0):  # allocate Symbol, sr number
    #print("sn", sN + 1)
    sT["srN"].append(sN + 1)  # +1 range 1 to n
    sT["symbol"].append(word)
    sT["address"].append(addr)


def allocateaddress(n, addr):  # allocate address
    #print(sT, n, addr)
    sT["address"][n] = addr
    # print(sT["address"],)
    return addr


def checkIndex(dC):  # return  index of symbol
    for i in range(len(sT["symbol"])):
        if dC == sT["symbol"][i]:
            return i


def lTable(word, lN, addr=0):  # creat literal table
    lT["srN"].append(lN + 1)
    lT["address"].append(addr)
    lT["literal"].append(word)


def allocateLaddress(addr, n):  # allocate address to literal
    i = 0
    poolTab["Pool TAB"].append(n + 1)  # Find pool tab number

    for i in range(n, len(lT["literal"]), 1):
        lT["address"][i] = addr
        dataNew.write("\n")
        dataNew.write(str(addr))
        dataNew.write("                ")

        dataNew.write("(")
        dataNew.write(" C , 00")
        dataNew.write(lT["literal"][i][2:-1])  # Updated
        dataNew.write(" )")
        addr = addr + 1
    dataNew.write("\n")
    return i + 1, addr


lC = 0


def checkS(word, word2):
    if word in sT["symbol"][::] and word2 == "DS":  # check copy present or not
        # sn.append(sT["symbol"].index(word))

        return 0
    elif word in sT["symbol"][::]:
        dataNew.write("(")
        dataNew.write("S")
        dataNew.write(",")
        dataNew.write(str(sT["symbol"].index(word) + 1))
        # sn.append(sT["symbol"].index(word) + 1)    # See this
        dataNew.write(")")
        dataNew.write("\n")

        return 0
    else:
        return 1


def CheckL(word, ln1):
    if word in lT["literal"][ln1::1]:  # Updated
        dataNew.write("(")
        dataNew.write(" l ")
        dataNew.write(" , ")
        dataNew.write(str(lT["literal"].index(word) + 1))
        dataNew.write(" )\n")

        return 0
    else:
        return 1


def adPtable(line, lC):  # increment address of lc by value
    if "+" in line:
        lineN = line.strip("\n")
        # print(lineN.split(" ")[1].split("+"))
        ind = sT["symbol"].index(lineN.split(" ")[1].split("+")[0])
        # print(lineN.split(" ")[1].split("+")[1][:2], "ind")
        ind1 = lineN.split(" ")[1].split("+")[1]
        # print(ind1,"ind1")
        # print(sT["address"][ind],"ind")
        dataNew.write("            C ")
        dataNew.write(str(int(sT["address"][ind] + int(ind1))))
        return int(sT["address"][ind] + int(ind1))
    elif line.split()[1].isdigit():
        return int(line.split()[1])
    else:

        ind = int(sT["address"][sT["symbol"].index(line.split()[1])])
        return ind


def poTable(word):  # AAd code value
    pot = {'LTORG': '05', 'ORIGIN': '03', 'EQU': '04'}
    if word in pot:
        return pot[word]
    else:
        return -1



def error(errorNumber):
    if errorNumber == 1:
        print("Syntax error :\"Register or operand is missing..\"")
    elif errorNumber == 2:
        print("Symbol declared again...")
    elif errorNumber == 3:
        print("COMP is missing before branch..")
    elif errorNumber == 4:
        print("START is missing ..")
    elif errorNumber == 5:
        print("END is missing ..")

def allocateAque(sN, word):
    sT["address"][sN] = sT["address"][sT["symbol"].index(word)]


def checkFun():
    lN, lC, sN, ltN1 = 0, 0, 0, 0
    dC, rC = "", ""
    ln1 = 0
    compVar = False
    if dataL[0].split()[0]!='START':
        error(4)
        exit(0)
    for line in dataL:
        for word in line.split():
            if ("START" == word):
                dataNew.write("00  ( AD, 01)")


            elif (opCode(word) != -1):  # Return Imperatve code value
                n = opCode(word)
                dataNew.write(str(lC))
                dataNew.write(" ( ")
                dataNew.write("IS ")
                dataNew.write(", ")
                dataNew.write(n)
                dataNew.write(" ) ")
                dataNew.write(" ")
                pass2["IS"].append(n)
                if n == '06':
                    compVar = True
                if n == '07' and compVar == False:
                    error(3)
                    compVar = False
                    exit(0)
                if n in InsLen3:
                    if len(line.split()[line.split().index(word):])<3:
                        error(1)
                        exit(0)
                    elif len(line.split()[line.split().index(word):])>3:
                        print("Syntax error :  Extra Symbol",line.split()[-1],"is present")
                        exit(0)
                if n in InsLen2:
                    if len(line.split()[line.split().index(word):])<2:
                        error(4)
                        exit(0)
                    elif len(line.split()[line.split().index(word):])>2:
                        print("Syntax error :  Extra Symbol",line.split()[-1],"is present")
                        exit(0)


                if int(n) == 00:
                    dataNew.write("\n")

                lC = lC + 1
            elif (rTble(word) != -1):  # Return register value
                n = rTble(word)
                dataNew.write("  ")
                dataNew.write("( R , ")
                dataNew.write(n)
                pass2["RG"].append(n)
                dataNew.write(" )")
            elif cTable(word) != -1:
                dataNew.write("   ")
                dataNew.write(cTable(word))
            elif (dTable(word) != -1):
                n = dTable(word)

                if (word == "DS"):
                    rC = "DS"
                else:
                    rC = "DC"

            # N DS 5
            elif (word.isdigit()):  # check constant
                if (rC == "DS"):
                    l = checkIndex(dC)  # Index of symbol
                    allocateaddress(l, lC)  # Allocate address to symbol

                    dataNew.write(str(lC))
                    dataNew.write(" (")
                    dataNew.write(" DL ")
                    dataNew.write(",")
                    dataNew.write(str(n))
                    dataNew.write(" )")
                    lC = lC + int(word)
                    if line.split()[0] in symbolError:
                        error(2)
                        exit(0)
                    else:
                        symbolError.append(line.split()[0])

                    rC = "NULL"
                elif rC == "DC":
                    l = checkIndex(dC)  # Index of symbol

                    # print(l,lC)
                    allocateaddress(l, lC)  # Allocate address to symbol

                    dataNew.write(str(lC))
                    dataNew.write(" (")
                    dataNew.write(" DL")
                    dataNew.write(",")
                    dataNew.write(str(n))
                    dataNew.write(" )")
                    allocateaddress(l, lC)  # Allocate address to symbol
                    lC = lC + int(word)
                    rC = "NULL"
                    if line.split()[0] in symbolError:
                        error(2)
                        exit(0)
                    else:
                        symbolError.append(line.split()[0])

                else:

                    if line.split(" ")[0] == "START":
                        lC = int(word)
                    else:
                        dataNew.write(str(lC))
                dataNew.write("       (")
                dataNew.write(" C , ")
                dataNew.write(word)
                dataNew.write(" )")

                dataNew.write("\n")
            elif poTable(word) != -1:
                n = poTable(word)
                dataNew.write("\n     ( ")
                dataNew.write("AD")
                dataNew.write(",")
                dataNew.write(str(n))
                dataNew.write(" )")

                if n == "03":
                    lC = adPtable(line, lC)  # increment address
                if n == "05":
                    ltA1 = np.array(lT["address"])
                    ln1 = lN
                    pass2["IS"].append("l")
                    ltN = np.count_nonzero(ltA1)

                    ltN1, lC = allocateLaddress(lC, ltN1)  # allocate address to literal

                    ltN = 0
                if n == "04":
                    allocateAque(sN - 1, line.split(" ")[2].strip("\n"))
                    # lAssign()
                    dataNew.write("      ")  # updated
            elif word[0] == "=":
                if (CheckL(word, ln1)):
                    dataNew.write("(")
                    dataNew.write(" l ")
                    dataNew.write(", ")
                    lTable(word, lN)
                    snl.append("l")
                    dataNew.write(str(lN + 1))
                    dataNew.write(" )")
                    dataNew.write("\n")
                    lN = lN + 1


                ltN = 1
            elif word == "END":
                dataNew.write("    ( ")
                dataNew.write("AD")
                dataNew.write(",")
                dataNew.write("02")
                dataNew.write(" )\n")
                ltA2 = np.array(lT["address"])
                ltN = (np.size(ltA2)) - np.count_nonzero(ltA2)  # literal with without address
                if ltN:
                    allocateLaddress(lC, ltN1)  # allocate address to literal
                break





            else:
                if (checkS(word, line.split(" ")[1])):  # Check similar copies of symbol
                    if line.split(' ', 1)[0] == word and line.split(" ")[1] != "DS":  # Assign address to label
                        # dataNew.write("S ")
                        # dataNew.write(str(sN))
                        sTable(sN, word)
                        # print(sT["address"])

                        allocateaddress(sN, lC)
                        # sn.append(sN)
                        sN = sN + 1



                    elif line.split(' ', 1)[0] == "ORIGIN":
                        pass
                    else:

                        dataNew.write("(")
                        dataNew.write(" S ")
                        dataNew.write(", ")
                        dataNew.write(str(sN + 1))  # symbol number 1 to n
                        dataNew.write(" )")
                        sTable(sN, word)
                        # if line.split()[1] != "EQU":
                        #     sn.append(sN + 1)
                        #     snl.append("s")
                        dataNew.write("\n")
                        dC = word

                        sN = sN + 1
                else:
                    dC = word
    return  word

word=checkFun()
if word!='END':
    error(5)
    exit(0)
for i in sn:
    for j in sT["srN"]:
        if i == j:
            pass2["add"].append(sT["address"][i - 1])
# print(lC)
# print(sT)
# print(lT)

dataNew.write("\n")
dataNew.write("\n")
import pandas as pd

# ps = pd.DataFrame(pass2)
# ps = ps.to_string(index=False)
# pass2Data.write(str(ps))

dataNew.write("Symbol Table\n\n")  # Print symbol table
st = pd.DataFrame(sT)
st = st.to_string(index=False)
dataNew.write(str(st))
dataNew.write("\n")
dataNew.write("\n")

dataNew.write("Literal Table\n\n")  # Print Literal Table
lt = pd.DataFrame(lT)
lt = lt.to_string(index=False)
# print(lt)
dataNew.write(str(lt))
dataNew.write("\n")
dataNew.write("\n")

dataNew.write("Pool TAB\n\n")  # Print Literal Table
pt = pd.DataFrame(poolTab)
pt = pt.to_string(index=False)
# print(lt)
dataNew.write(str(pt))
dataNew.close()
############################
data = open("Pass2_output.txt", "r")
data = data.read()
flag = ""
flag1 = ""
flag2 = ""
flag3 = ""
flag4 = ""
flag5 = ""
c = ""
check = "F"
for i in data.split():
    if i == "IS":
        pass2Data.write("\n")
        flag = i
    if flag == "IS" and i.isdigit():
        pass2Data.write(i)
        pass2Data.write("  ")
        flag = "null"
    if i == "R":
        flag1 = i
    if flag1 == "R" and i.isdigit():
        pass2Data.write(i)
        pass2Data.write("  ")
        flag1 = "null"
    if i == "S":
        flag2 = "S"
    if flag2 == "S" and i.isdigit():
        pass2Data.write(str(sT["address"][int(i) - 1]))
        pass2Data.write("  ")
        flag2 = "Null"
    if i == "l":
        flag3 = "l"
    if flag3 == "l" and i.isdigit():
        pass2Data.write(str(lT["address"][int(i) - 1]))
        pass2Data.write("  ")
        l = int(i)
        n = l
        flag3 = "null"
    if i == "AD,05":
        flag4 = "05"
        check = "T"
    if i == "C" and check == "T":
        c = i

    if flag4 == "05" and i.isdigit() and c == "C":
        pass2Data.write("\n       ")
        pass2Data.write(i)
        c = "null"
    if i == "AD,02":
        check = "T"
        flag5 = "02"

    if flag5 == "02" and i.isdigit() and c == "C":
        pass2Data.write("\n       ")
        pass2Data.write(i)
        c = "null"
    if i == "IS" or i == "AD" or i == "DL":
        flag4 = "null"
        flag5 = "null"
        c = "null"
        check = "F"
########
pass2Data.write("\n\n")

pass2Data.write("Symbol Table\n\n")  # Print symbol table
st = pd.DataFrame(sT)
st = st.to_string(index=False)
pass2Data.write(str(st))
pass2Data.write("\n")
pass2Data.write("\n")

pass2Data.write("Literal Table\n\n")  # Print Literal Table
lt = pd.DataFrame(lT)
lt = lt.to_string(index=False)
# print(lt)
pass2Data.write(str(lt))
pass2Data.write("\n")
pass2Data.write("\n")

pass2Data.write("Pool TAB\n\n")  # Print Literal Table
pt = pd.DataFrame(poolTab)
pt = pt.to_string(index=False)
# print(lt)
pass2Data.write(str(pt))
