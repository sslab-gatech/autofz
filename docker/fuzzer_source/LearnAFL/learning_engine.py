#!/usr/bin/env python2
import os
import sys
import math
import time
from _weakrefset import WeakSet

MAXCACULATE = 250000000
HardCode = {}
Relation = []
NewFault = []
LengthCount = {}
Process = []
Finding = []
Paths = []
Matrix = []
current_time = time.time()
time_out = 0

#Defining data struct to store data nodes.
class PathInformation:
    minLength = 0
    nums = 0
    cksum = 0

    def __init__(self, tcse, cks):
        self.cksum = cks
        if tcse != '':
            self.testcases = [tcse]
            self.nums = 1
            self.totalExec = 1
        else:
            self.testcases = []
            self.nums = 0
            self.totalExec = 0
        self.minLength = len(tcse)
        self.maxLength = len(tcse)
        self.fixedLength = -1
        self.relation = []
        self.fault = 0
        self.reg = []
        self.pos = []
        self.useModel = 0
        self.isSeed = 0
        self.diff = 0


    def update(self, node):
        self.testcases.append(node['Testcase'])
        self.nums += 1
        self.totalExec += 1
        tempLength = len(node['Testcase'])
        if self.minLength == 0:
            self.minLength = tempLength
        if tempLength < self.minLength:
            self.minLength = tempLength
        if tempLength > self.maxLength:
            self.maxLength = tempLength
        if node['Fault case'] != '0':
            self.fault = int(node['Fault case'])

    def delete(self, node):
        self.testcases.remove(node['Testcase'])
        self.nums -= 1
        self.totalExec -= 1
        if self.nums == 0:
            self.minLength = 0
        else:
            if len(node['Testcase']) == self.minLength:
                self.minLength = len(self.testcases[0])
                for i in range(0, self.nums):
                    if len(self.testcases[i]) < self.minLength:
                        self.minLength = len(self.testcases[i])

    def add_node(self, node):
        if node['Cksum'] != self.cksum:
            return 0
        else:
            self.update(node)


    def analysis_feature(self):
        #Trying to find hardcode and relation
        if self.maxLength == self.minLength:
            self.fixedLength = self.maxLength
        else:
            self.fixedLength = -1

        if self.nums == 0:
            return 0
        else:
            tempReg = []
            tempPos = []
            lastReg = self.reg
            lastPos = self.pos
            print "[*] Getting format."
            if self.nums * self.maxLength * self.maxLength > MAXCACULATE:
                tempNum = MAXCACULATE / (self.maxLength * self.maxLength)
                tempReg, tempPos = get_format(self.testcases[0:tempNum])
            else:
                tempReg, tempPos = get_format(self.testcases)
            if self.reg != []:
                self.reg, self.pos = generate_new_reg_from_two_regs(self.reg, self.pos, tempReg, tempPos)
                if self.reg != lastReg or self.pos != lastPos:
                    self.useModel = 1
                else:
                    self.useModel = 2
            else:
                self.useModel = 1
                self.reg = tempReg
                self.pos = tempPos

            if self.reg == []:
                self.useModel = 0



def get_hardcode(testcases):
    minLength = len(testcases[0])
    for tcse in testcases:
        if len(tcse) < minLength:
            minLength = len(tcse)
    tempHardcode = []
    for i in range(0, minLength):
        tempHardcode.append(testcases[0][i])
    for tcse in testcases:
        for i in range(0,minLength):
            if tcse[i] != tempHardcode[i]:
                tempHardcode[i] = ''

    hardcode = {}
    i = 0
    while i < len(tempHardcode):
        if tempHardcode[i] != '':
            j = i
            hardcode[j] = ''
            while i < len(tempHardcode) and tempHardcode[i] != '':
                hardcode[j] += tempHardcode[i]
                i += 1
        i += 1

    return hardcode

def splice_testcases(testcases, hardcode):
    order1 = hardcode.keys()
    order1.sort()
    order2 = []
    for i in order1:
        order2.append(i+len(hardcode[i]))
    if 0 not in order1:
        order2.insert(0,0)
    else:
        order1.pop(0)
    splice = []
    for tc in testcases:
        spliceOfTc = []
        for i in range(len(order1)):
            spliceOfTc.append(tc[order2[i]:order1[i]])
        spliceOfTc.append(tc[order2[-1]:])
        splice.append(spliceOfTc)
    result = []
    for i in range(0,len(splice[0])):
        tempSplice = []
        for j in range(0,len(splice)):
            tempSplice.append(splice[j][i])
        result.append(tempSplice)
    return result

def splice_testscase_by_regular(testcase, reg, pos, num):
    ind = [0]
    for i in range(0,len(reg)):
        if pos[i] == -2:
            ind.append(testcase[ind[-1]:].index(reg[i]))
        elif pos[i] != -1:
            ind.append(pos[i])
        else:
            ind.append(len(testcase)-len(reg[i])-1)



def get_dictionary(strings):
    dic = list(set(strings[0]))
    j = 0
    while j < len(dic):
        for s in strings:
            if dic[j] not in s:
                dic.remove(dic[j])
                j -= 1
                break
        j += 1
    return  dic

def get_subString(s1, s2, dic):
    i = 0
    subString = []
    while i < len(s1):
        flag = False
        j = 0
        maxLength = 0
        maxString = ''
        while j < len(s2):
            tempString = ''
            k = 0
            while (i + k < len(s1) and j + k < len(s2) and s1[i+k] == s2[j + k] and s1[i + k] in dic):
                flag = True
                tempString += s1[i + k]
                k += 1
            if k > maxLength:
                maxLength = k
                maxString = tempString
            if k == 0:
                j += 1
            else:
                j += k

        if flag == False:
            i += 1
        else:
            subString.append(maxString)
            i += maxLength
    return subString


def find_min_string(strings):
    min_sub = strings[0]
    minLength = 0
    for sub in min_sub:
        minLength += len(sub)

    for s in strings:
        length = 0
        for sub in s:
            length += len(sub)

        if length < minLength:
            minLength = length
            min_sub = s

    return min_sub

def get_position(testcases, minString):
    regular = minString
    lengthOfLast = len(regular[-1])
    end = False
    position = [-2] * len(regular)

    for tscs in testcases:
        if tscs[-lengthOfLast:] != regular[-1]:
            end = True

    if position[-1] == -2:
        if end == False:
            position[-1] = -1
    return regular, position


def generate_regular(testcases, time_limit):
    dictionary  = get_dictionary(testcases)
    reg = []
    pos = []
    subString = []
    c_time = time.time()
    if dictionary == []:
        return [],[]
    num = len(testcases)
    for i in range(0, len(testcases)):
        if time.time() - c_time > time_limit:
            time_out = 1
            num = i
            break
        subString.append(get_subString(testcases[i], testcases[(i+1)%len(testcases)], dictionary))
    minString = find_min_string(subString)

    if minString != []:
        for i in range(0, num):
            for r in minString:
                if r not in testcases[i]:
                    minString.remove(r)
    if minString != []:
        reg, pos = get_position(testcases[0:num], minString)
    if reg != []:
        for tc in testcases[0:num]:
            i = 0
            j = 0
            while i < len(reg):
                if pos[i] == -2:
                    if reg[i] in tc[j:]:
                        j = j + tc[j:].index(reg[i]) + len(reg[i])
                        i += 1
                    else:
                        reg.pop(i)
                        pos.pop(i)
                        continue
                elif pos[i] == -1:
                    if tc[-len(reg[i]):] == reg[i]:
                        i += 1
                    else:
                        reg.pop(i)
                        pos.pop(i)
                        continue
                else:
                    j = pos[i] + len(reg[i])
                    i += 1

    return reg, pos

def get_regular(testcases, hardcode):
    splice = splice_testcases(testcases,hardcode)
    tempReg = []
    tempPos = []
    tempKey = hardcode.keys()
    tempKey.sort()
    if len(splice) > 0:
        time_limit = 15.0 / len(splice)
    for i in range(0,len(splice)):
        r, p = generate_regular(splice[i], time_limit)
        tempReg.append(r)
        tempPos.append(p)
    reg = []
    pos = []
    if 0 in hardcode.keys():
        for i in range(0,len(tempReg)):
            reg.append(hardcode[tempKey[i]])
            pos.append(tempKey[i])
            for j in range(0,len(tempReg[i])):
                reg.append(tempReg[i][j])
                pos.append(tempPos[i][j])
    else:
        for i in range(0,len(tempReg)-1):
            for j in range(0,len(tempReg[i])):
                reg.append(tempReg[i][j])
                pos.append(tempPos[i][j])
            reg.append(hardcode[tempKey[i]])
            pos.append(tempKey[i])
        for j in range(0, len(tempReg[-1])):
            reg.append(tempReg[-1][j])
            pos.append(tempPos[-1][j])
    return reg,pos

def get_format(testcases):
    if len(testcases) == 0:
        return [],[]
    hardcode = get_hardcode(testcases)
    reg,pos = get_regular(testcases,hardcode)

    return reg,pos

def get_public_hardcode(reg1,pos1,reg2,pos2):
    hardcode1 = {}
    hardcode2 = {}
    length1 = len(pos1)
    length2 = len(pos2)
    for i in range(0,max(length1, length2)):
        if i < length1:
            if pos1[i] != -2 and pos1[i] != -1:
                for j in range(0,len(reg1[i])):
                    hardcode1[pos1[i]+j] = reg1[i][j]
        if i < length2:
            if pos2[i] != -2 and pos2[i] != -1:
                for j in range(0,len(reg2[i])):
                    hardcode2[pos2[i]+j] = reg2[i][j]
    if hardcode1 == {} or hardcode2 == {}:
        return {}
    tempHardcode = []
    for i in range(0,max(max(hardcode1.keys()),max(hardcode2.keys()))+1):
        if i in hardcode1.keys() and i in hardcode2.keys():
            if hardcode1[i] == hardcode2[i]:
                tempHardcode.append(hardcode1[i])
            else:
                tempHardcode.append('')
        else:
            tempHardcode.append('')
    hardcode = {}
    lengthOfHardcode = len(tempHardcode)
    i = 0
    while i < lengthOfHardcode:
        if tempHardcode[i] != '':
            j = i
            hardcode[j] = ''
            while i < lengthOfHardcode:
                if tempHardcode[i] != '':
                    hardcode[j] += tempHardcode[i]
                    i += 1
                else:
                    break
        i += 1

    return hardcode

def transfer_reg(reg,pos,hardcode):
    newReg = []
    newPos = []
    for i in range(0,len(reg)):
        if pos[i] != -2 and pos[i] != -1:
            lastJ = 0
            for j in range(0,len(reg[i])):
                if pos[i]+j in hardcode.keys():
                    if j != lastJ:
                        newReg.append(reg[i][lastJ:j])
                        newPos.append(-2)
                    newReg.append(hardcode[pos[i]+j])
                    newPos.append(pos[i]+j)
                    lastJ = j+len(hardcode[pos[i]+j])
            if lastJ < len(reg[i]):
                newReg.append(reg[i][lastJ:])
                newPos.append(-2)
        else:
            newReg.append(reg[i])
            newPos.append(pos[i])

    return newReg, newPos

def get_max_substring(s1, s2):
    i = 0
    subString = []
    lastJ = 0
    while i < len(s1):
        flag = False
        j = lastJ
        maxLength = 0
        maxString = ''
        while j < len(s2):
            tempString = ''
            k = 0
            while (i + k < len(s1) and j + k < len(s2) and s1[i+k] == s2[j+k]):
                flag = True
                tempString += s1[i + k]
                k += 1
            if k > maxLength:
                maxLength = k
                maxString = tempString
            if k == 0:
                j += 1
            else:
                lastJ = lastJ+k
                j += k

        if flag == False:
            i += 1
        else:
            subString.append(maxString)
            i += maxLength
    return subString

def generate_sub_regular(reg1,reg2):
    if reg1 == [] or reg2 == []:
        return [],[]
    reg = []
    pos = []
    s1 = ''
    s2 = ''
    i1 = []
    i2 = []
    lastIndex1 = 0
    lastIndex2 = 0
    for i in range(0,len(reg1)):
        s1 += reg1[i]
        i1.append(lastIndex1)
        lastIndex1 += len(reg1[i])
    i1.append(lastIndex1)
    for i in range(0,len(reg2)):
        s2 += reg2[i]
        i2.append(lastIndex2)
        lastIndex2 += len(reg2[i])
    i2.append(lastIndex2)
    maxLength = 0
    maxS = []
    for i in range(0,len(s1)):
        s = get_max_substring(s1[i:],s2)
        tempLength = 0
        for j in s:
            tempLength += len(j)
        if tempLength > maxLength:
            maxLength = tempLength
            maxS = s
    lastIndex1 = 0
    lastIndex2 = 0
    for s in maxS:
        index1 = lastIndex1+s1[lastIndex1:].index(s)
        index2 = lastIndex2+s2[lastIndex2:].index(s)
        lastI = 0
        for i in range(0,len(s)):
            if i+index1 not in i1 and i+index2 not in i2:
                continue
            else:
                if i+index1 in i1:
                    if lastI == i:
                        continue
                    else:
                        reg.append(s[lastI:i])
                        pos.append(-2)
                        lastI = i
                elif i+index2 in i2:
                    if lastI == i:
                        continue
                    else:
                        reg.append(s[lastI:i])
                        pos.append(-2)
                        lastI = i
        if lastI <= len(s):
            reg.append(s[lastI:lastI+len(s)])
            pos.append(-2)
            lastIndex1 = lastIndex1+len(s)
            lastIndex2 = lastIndex2+len(s)


    return reg, pos

def generate_new_reg_from_two_regs(reg1,pos1,reg2,pos2):
    reg = []
    pos = []
    hardcode = get_public_hardcode(reg1,pos1,reg2,pos2)
    newReg1,newPos1 = transfer_reg(reg1,pos1,hardcode)
    newReg2,newPos2 = transfer_reg(reg2,pos2,hardcode)
    numsOfSplice = len(hardcode.keys())
    lastindex1 = 0
    lastindex2 = 0
    tempKey = hardcode.keys()
    tempKey.sort()
    for i in range(0,numsOfSplice):
        index1 = newPos1.index(tempKey[i])
        index2 = newPos2.index(tempKey[i])
        if lastindex1 != index1 and lastindex2 != index2:
            r,p = generate_sub_regular(newReg1[lastindex1:index1], newReg2[lastindex2:index2])
            for j in range(0,len(r)):
                reg.append(r[j])
                pos.append(p[j])
            reg.append(hardcode[tempKey[i]])
            pos.append(tempKey[i])
            lastindex1 = index1 + 1
            lastindex2 = index2 + 1
        else:
            reg.append(hardcode[tempKey[i]])
            pos.append(tempKey[i])
            lastindex1 = index1 + 1
            lastindex2 = index2 + 1
    if lastindex1 == len(newPos1) or lastindex2 == len(newPos2):
        return reg, pos
    else:
        r,p = generate_sub_regular(newReg1[lastindex1:],newReg2[lastindex2:])
        if newPos1[-1] == -1 and newPos2[-1] == -1:
            if r[-1] in newReg1[-1] and r[-1] in newReg2[-1]:
                p[-1] = -1
        for i in range(0, len(r)):
            reg.append(r[i])
            pos.append(p[i])
        return reg, pos


#Printing error message and shuting down programs
def sys_error(message):
    print message
    exit(1)

#Creating file to store information
def create_information_file(path):
    path_abs = os.path.abspath(path).split('/')
    if len(path_abs) >= 4:
        path_file = ''
        for i in range(0,len(path_abs[:-2])):
            path_file = path_file + path_abs[i] +'/'
        path_file += "fuzzing_transfer"
        return path_file
    else:
        sys_error("The path of output dictionary is too short")

#Reading information from information file
def read_information_file(information_file):
    if os.path.exists(information_file):
        try:
            fl = open(information_file, 'r')
        except IOError:
            sys_error("Can't open information file!")
            for line in fl.readlines():
                cksum, trans = line.split(':')[0]
                if cksum not in Paths:
                    Paths.append(cksum)
                tempList = []
                t = trans.split(' ')
                for i in range(0, len(t)):
                    if t[i] != ' ' and t[i] != '\n':
                        tempList.append(int(t[i]))
                Matrix.append(tempList)



#Creating file to store models
def write_model_to_file(filename, path):
    if os.path.exists(filename):
        os.remove(filename)
    try:
        fl = open(filename, 'w')
    except IOError:
        sys_error("IOError: create file failed!")
    else:
        fl.write('Cksum:{cksum}\n'
                 'TotalExec:{totalExec}\n'
                 'FaultCase:{fault}\n'
                 'MinLength:{minLength}\n'
                 'MaxLength:{maxLength}\n'
                 'UseModel:{useModel}\n'
                 'Diff:{diff}\n'.format(cksum=path.cksum,
                                 totalExec=path.totalExec,
                                 fault=path.fault,
                                 minLength=path.minLength,
                                 maxLength=path.maxLength,
                                 useModel=path.useModel,
                                 diff=path.diff))
        fl.write('PositionLength:{positionLength}\n'.format(positionLength=len(path.pos)))
        for i in range(0, len(path.reg)):
            fl.write('Position:{position}\nLength:{length}\nRegular:{regular}\n'.format(position=path.pos[i],length=len(path.reg[i]),regular=path.reg[i]))

        print "[*] Writing model to model file."

#Opening files
def open_file(filename):
    try:
        fl = open(filename, 'r')
    except IOError:
        sys_error("IOError: open file failed! Couldn't find file or Permission denied")
    else:
        return fl

#Deleting files.
def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        sys_error("File not exist!")


#Reading and handling last model file
def read_and_handle_last_model(file):
    recordRegular = False
    for line in file.readlines():
        if line.startswith("Cksum:"):
            newPath = PathInformation('', line[6:-1])
        elif line.startswith("TotalExec:"):
            newPath.totalExec = int(line[10:-1])
        elif line.startswith("FaultCase:"):
            newPath.fault = int(line[10:-1])
        elif line.startswith("MinLength:"):
            newPath.minLength = int(line[10:-1])
        elif line.startswith("MaxLength:"):
            newPath.maxLength = int(line[10:-1])
        elif line.startswith("UseModel:"):
            newPath.useModel = int(line[9:-1])
        elif line.startswith("Diff:"):
            newPath.diff = int(line[5:-1])
        elif line.startswith("PositionLength:"):
            newPath.reg = [''] * int(line[15:-1])
            newPath.pos = [0] * int(line[15:-1])
            k = -1
        elif line.startswith("Position:"):
            if recordRegular == True:
                recordRegular = False
                newPath.reg[k] = newPath.reg[k][:-1]
            k += 1
            newPath.pos[k] = int(line[9:-1])
        elif line.startswith("Regular:"):
            recordRegular = True
            newPath.reg[k] = line[8:]
        elif recordRegular == True:
            newPath.reg[k] += line
    if recordRegular == True:
        newPath.reg[-1] = newPath.reg[-1][:-1]

    return newPath

#Handling knowledge files, generating seednodes and process.
def generate_pathnodes_and_process(knowledgeFile,lastModelFileName):
    recordSeed = False
    recordTestcase = False
    startRecording = True
    node = {}
    lastNode = {}
    if os.path.exists(lastModelFileName):
        lastModelFile = open_file(lastModelFileName)
        path = read_and_handle_last_model(lastModelFile)
    else:
        path = PathInformation('', '')
    for line in knowledgeFile.readlines():
        if line.startswith("Seed:"):
            startRecording = True
            recordSeed = True
            node = {}
            node['Seed'] = ""
            node['Seed'] = line[5:]

        elif line.startswith("Stage cksum:"):
            recordSeed = False
            node['Seed'] = node['Seed'][:-1]
            node['Stage cksum'] = line[12:-1]
            path.testcases.append(node['Seed'])
            path.cksum = node['Stage cksum']

        elif line.startswith("Stage name:"):
            tempSeed = node['Seed']
            tempStageCksum = node['Stage cksum']
            node = {}
            startRecording = True
            node['Seed'] = tempSeed
            node['Stage cksum'] = tempStageCksum
            node['Stage name'] = line[11:-1]
            if node['Stage name'].startswith("splice"):
               node['Seed'] = lastNode['Seed']

        elif line.startswith("Testcase:"):
            recordTestcase = True
            node['Testcase'] = line[9:]

        elif line.startswith("Fault case:"):
            recordTestcase = False
            node['Testcase'] = node['Testcase'][:-1]
            node['Fault case'] = line[11:-1]

        elif line.startswith("Finding:"):
            node['Finding'] = line[8:-1]

        elif line.startswith("Cksum:"):
            startRecording = False
            node['Cksum'] = line[6:-1]

            if node['Cksum'] not in Paths:
                Paths.append(node['Cksum'])

        else:
            if recordSeed:
                node['Seed'] += line

            elif recordTestcase:
                node['Testcase'] += line

        if startRecording == False:
            if node['Fault case'] != '0':
                NewFault.append(node)

            if node['Finding'] != '0':
                Finding.append(node)

            path.add_node(node)
            lastNode = node

    return path


#Handling knowledge files.
def handle_knowledge_file(knowledgeFileName, modelFileName):
    knowledgeFile = open_file(knowledgeFileName)  #Opening knowledge files
    print "[*] Handling knowledge file."
    path = generate_pathnodes_and_process(knowledgeFile, modelFileName)

    print "[*] Generating model."
    path.analysis_feature()

    return path
#Writing time information to files
def write_to_time_file(timeFile, lastTime):
    if os.path.exists(timeFile):
        try:
            fl = open(timeFile, 'a')
        except IOError:
            sys_error("Can't open information file!")
        fl.write(str(lastTime)+"\n")

def main(argv):
    if len(argv) == 3:
        knowledgeFile = argv[0]
        modelFile = argv[1]
        timeFile = argv[2]
    else:
        sys_error("")
    print "[*] Starting python script."
    current_time = time.time()
    #information_file = create_information_file(modelFile)
    path = handle_knowledge_file(knowledgeFile,  modelFile)
    write_model_to_file(modelFile, path)
    delete_file(knowledgeFile)
    last_time = time.time() - current_time
    write_to_time_file(timeFile,last_time)


if __name__ == "__main__":
    main(sys.argv[1:])
    #main(['./bug/2019-7-10-9-6-52-8034-knowledge.txt','./bug/1705'])
