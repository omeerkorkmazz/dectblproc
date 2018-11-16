from satispy import Variable, CnfFromString
from satispy.solver import Minisat
from tabulate import tabulate
import itertools
import math as math
import sys


# it takes all seperated data and just previews how they are seen.
def PreviewTable(conditions, conditionExpressions, conditionValues, outputs, outputValues):
    for i in range(0, len(conditions)):
        print(conditions[i], " ", conditionExpressions[i])

    for i in range(0, len(conditions)):
        print(conditions[i], " ", conditionValues[i])

    for i in range(0, len(outputs)):
        print(outputs[i], " ", outputValues[i])


# Prepares the our data for seperation. fileName is dt0 as a default.
# It takes the document name and opens document and starts to read lines respectively.
# Then, creates a list of lines and returns the list
def PrepareToSeperateData(fileName):
    isExcept = False
    try:
        pathInput = fileName.split("\\")
    except:
        isExcept = True

    with open(r"" + fileName, 'r') as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    if(isExcept):
        return content, fileName
    else:
        return content, pathInput[len(pathInput) - 1]


#It takes content which is returned by PrepareToSeperateData()
#It seperates document as Conditions, ConditionExpressions, ConditionVaues,Outputs and OutputValues
def SeperateData(content):
    conditions = []
    conditionExpressions = []
    conditionValues = []
    outputs = []
    outputValues = []

    seperateIndex = content.index("##")

    for i in range(0, seperateIndex):
        text = content[i]
        if (text.startswith("c")):
            condition, expression = text.split(":")
            conditions.append(condition)
            conditionExpressions.append(expression)

    for i in range(seperateIndex, len(content)):
        text = content[i]
        if (text.startswith("c")):
            condition, conditionValue = text.split(" ")
            conditionValues.append(list(conditionValue))
        elif (text.startswith("a")):
            output, outputValue = text.split(" ")
            outputs.append(output)
            outputValues.append(list(outputValue))

    return conditions, conditionExpressions, conditionValues, outputs, outputValues


def FindPairs(conditions, conditionExpressions, conditionValues, outputs, outputValues):
    length = len(conditionValues[0])
    InconsistentPairs = []
    RedundantPairs = []

    for i in range(0, length - 1):
        state = True

        # check condiitons whether if they are equal or not.
        # if state is true, it will check actions for redundant and inconsistent situations.
        # if state is false, it means there is no redundancy or inconsistency.
        for k in range(i + 1, length):
            for j in range(0, len(conditions)):
                if (conditionValues[j][i] == "-" or conditionValues[j][k] == "-"):
                    state = True
                elif (conditionValues[j][i] == conditionValues[j][k]):
                    state = True
                elif (conditionValues[j][i] != conditionValues[j][k]):
                    state = False
                    break

            # check actions whether if they are same or not. It clarifies inconsistent and redundant rules.
            if (state == True):
                outState = True
                for m in range(0, len(outputs)):
                    if (outputValues[m][i] != outputValues[m][k]):
                        outState = False
                        break
                    else:
                        outState = True

                if (outState == False):
                    # print("Inconsistent pair rule ",i+1, "and rule ",k+1)
                    InconsistentPairs.append((i, k, "r" + str(i + 1), "r" + str(k + 1)))
                else:
                    # print("Redundant pair rule ",i+1, "and rule ",k+1)
                    RedundantPairs.append((i, k, "r" + str(i + 1), "r" + str(k + 1)))

    return InconsistentPairs, RedundantPairs


# This method calculates the total number of unique rules
def CalculateRuleCounts(InConsistentPairs, RedundantPairs):
    combineList = InconsistentPairs + RedundantPairs
    deletedList = []
    uniqueList = []

    for i in range(0, len(combineList)):

        firstIndex = combineList[i][0]
        secondIndex = combineList[i][1]
        firstRuleCount = 0
        secondruleCount = 0

        # find the total rule numbers of each pair
        for c in range(0, len(conditions)):
            if (conditionValues[c][firstIndex] == "-"):
                firstRuleCount += 1
            if (conditionValues[c][secondIndex] == "-"):
                secondruleCount += 1

        # if # of rules of first pair is greater than second pair or they are equal
        if (firstRuleCount > secondruleCount or firstRuleCount == secondruleCount):
            isSeconPairUnique = secondIndex in uniqueList
            isSecondPairDeleted = secondIndex in deletedList
            # if second pair is presence in uniqueList before, delete it from uniqueList and add it to deletedList.
            if (isSeconPairUnique == True):
                uniqueList.remove(secondIndex)
            elif (isSecondPairDeleted == False):
                deletedList.append(secondIndex)

                # first pair is added into uniqueList, if it is not presence in the list before and it is not in deletedList.
            isFirstPairDeleted = firstIndex in deletedList
            isFirstPairUnique = firstIndex in uniqueList

            if (isFirstPairDeleted == False):
                if (isFirstPairUnique == False):
                    uniqueList.append(firstIndex)

        # if # of rules of second pair is greater than first pair
        if (secondruleCount > firstRuleCount):
            isFirstPairUnique = firstIndex in uniqueList
            isFirstPairDeleted = firstIndex in deletedList
            # if first pair is presence in uniqueList before, delete it from uniqueList and add it to deletedList
            if (isFirstPairUnique == True):
                uniqueList.remove(firstIndex)
                if (isFirstPairDeleted == False):
                    deletedList.append(firstIndex)
            elif (isFirstPairDeleted == False):
                deletedList.append(firstIndex)

                # second pair is added into uniqueList, if it is not presence in the list before and it is not in deletedList.
            IsSecondPairUnique = secondIndex in uniqueList
            IsSecondPairDeleted = secondIndex in deletedList
            if (IsSecondPairDeleted == False):
                if (IsSecondPairUnique == False):
                    uniqueList.append(secondIndex)

            elif (isFirstPairDeleted == False):
                deletedList.append(firstIndex)

    # finds the other unique rules except inconsistent and redundant pairs
    for r in range(0, len(conditionValues[0])):
        isExistInUnique = r in uniqueList
        isExistInDeleted = r in deletedList
        if (isExistInDeleted == False and isExistInUnique == False):
            uniqueList.append(r)

    # finds the total rule count by checking unique rules
    rCounts = []
    for m in range(0, len(uniqueList)):
        ruleCount = 0
        for c in range(0, len(conditions)):
            if (conditionValues[c][uniqueList[m]] == "-"):
                ruleCount += 1
        rCounts.append(math.pow(2, ruleCount))

    return sum(rCounts)


# This method prints the expected outputs to the user
def PrintResults(fileName, InconsistentPairs, RedundantPairs, conditionValues):
    isRedundant = False
    isInConsistent = False
    totalRuleNumbers = math.pow(2, len(conditionValues))
    completeTablePercent = 100

    if (len(InconsistentPairs) > 0):
        isInConsistent = True

    if (len(RedundantPairs) > 0):
        isRedundant = True

    totalRuleCount = CalculateRuleCounts(InconsistentPairs, RedundantPairs)

    # if there is any redundant or inconsistent pairs, calculates the percentage of table complete
    # if not, it means the table is %100 complete, as I defined it initally as 100
    if (isRedundant or isInConsistent):
        completeTablePercent = (totalRuleCount / totalRuleNumbers) * 100

    redundantAnswer = "No"
    inconsistentAnswer = "No"
    if (isRedundant):
        redundantAnswer = "Yes"
    if (isInConsistent):
        inconsistentAnswer = "Yes"

    rPairs = []
    rtext = ""
    for r in range(0, len(RedundantPairs)):
        rPairs.append((RedundantPairs[r][2], RedundantPairs[r][3]))
        if (r == len(RedundantPairs) - 1):
            rtext = rtext + "(r" + str(RedundantPairs[r][0] + 1) + ", r" + str(RedundantPairs[r][1] + 1) + ")"
        else:
            rtext = rtext + "(r" + str(RedundantPairs[r][0] + 1) + ", r" + str(RedundantPairs[r][1] + 1) + "), "

    itext = ""
    for r in range(0, len(InconsistentPairs)):
        rPairs.append((InconsistentPairs[r][2], InconsistentPairs[r][3]))
        if (r == (len(InconsistentPairs) - 1)):
            itext = itext + "(r" + str(InconsistentPairs[r][0] + 1) + ", r" + str(InconsistentPairs[r][1] + 1) + ")"
        else:
            itext = itext + "(r" + str(InconsistentPairs[r][0] + 1) + ", r" + str(InconsistentPairs[r][1] + 1) + "), "

    # print output process
    print("Processing File: %s" % fileName)
    print("Is table complete? " + str(int(completeTablePercent)) + "% complete")
    print("Is table redundant? " + redundantAnswer)
    if (isRedundant):
        print("    Redundant pairs of rules: ", rtext)
    print("Is table inconsistent? " + inconsistentAnswer)
    if (isInConsistent):
        print("    Inconsistent pairs of rules: ", itext)



def WriteTestCases(conditionValues, conditions):
    generalOutput = ""
    dontCareIndexes = []
    testCaseExpressions = []
    dontCareConditionsIndexes = []
    for t in range(0, len(conditionValues[0])):
        isDontCare = False
        dontCaresCount = 0
        for i in range(0, len(conditions)):
            conditionText = ""
            # we need to check each condition as true
            # if condition value is false, we can use negation(-) for that rule to be able to get true result from sat solver
            if (conditionValues[i][t] == "T"):
                conditionText = "(" + conditionExpressions[i] + ")"

            elif (conditionValues[i][t] == "F"):
                conditionText = "-(" + conditionExpressions[i] + ")"

            # if the value of condition of tth rule is dont care, check for both false and true.
            # if one of them says not satisfiable, we should approve that one value.
            elif (conditionValues[i][t] == "-"):
                dontCaresCount+=1
                isDontCare = True
                dontCareConditionsIndexes.append((i, t))
            # combines the conditions
            if (i == 0):
                generalOutput = conditionText
            else:
                generalOutput = generalOutput + " & " + conditionText

        if (isDontCare != True):
            testCaseExpressions.append((str(t), generalOutput))
        else:
            dontCareIndexes.append((t, dontCaresCount))

    return testCaseExpressions, dontCareIndexes, dontCareConditionsIndexes


def WriteTestCasesForDontCares(conditionValues, dontCareIndexes, dontCareConditionIndexes, conditionExpressions):
    dontCareSuites=[]
    for r in range(0, len(dontCareIndexes)):
        dCount = dontCareIndexes[r][1]
        dIndex = dontCareIndexes[r][0]
        possibleSamples = list(itertools.product([True, False], repeat=dCount))
        conditionText = ""
        globalText = ""
        for p in range(0, len(possibleSamples)):
            dCare = 0
            IsDontCare = False
            for c in range(0, len(conditions)):
                if (conditionValues[c][dIndex] == "T"):
                    conditionText = "(" + conditionExpressions[c] + ")"

                elif (conditionValues[c][dIndex] == "F"):
                    conditionText = "-(" + conditionExpressions[c] + ")"

                elif (conditionValues[c][dIndex] == "-"):
                    IsDontCare = True
                    if (possibleSamples[p][dCare] == True):
                        conditionText = "(" + conditionExpressions[c] + ")"
                    elif (possibleSamples[p][dCare] == False):
                        conditionText = "-(" + conditionExpressions[c] + ")"

                if (c == 0):
                    globalText = conditionText
                else:
                    globalText = globalText + " & " + conditionText

                if(IsDontCare):
                    dCare+=1
                    IsDontCare = False

            dontCareSuites.append((dIndex, globalText))

    return dontCareSuites


def PrintTestCaseTable(parametersValues, conditionValues):
    headers = []
    rules = []
    testCases = []
    table = []

    for t in range(0, len(parametersValues)):
        parametersValues[t] = sorted(parametersValues[t])

    if (len(parametersValues) != 0):
        for c in range(0, len(parametersValues[0])):
            headers.append(parametersValues[0][c][0])

    for b in range(0, len(parametersValues)):
        if (len(parametersValues[b]) != 0):
            for s in range(0, len(parametersValues[0])):
                rules.append(parametersValues[b][s][1])
            testCases.append(("r" + str(parametersValues[b][0][2]), rules))
            rules = []

    for z in range(0, len(conditionValues[0])):
        ruleInput = "r" + str(z + 1)
        for k in range(0, len(testCases)):
            if (ruleInput == testCases[k][0]):
                table.append(testCases[k])

    tempTable = []
    testSuitesTable = []
    for u in range(0, len(table)):
        tempTable.append(table[u][0])
        for n in range(0, len(table[u][1])):
            tempTable.append(table[u][1][n])

        testSuitesTable.append(tempTable)
        tempTable = []

    print("Testsuite")
    print("=========")
    print(tabulate(testSuitesTable, headers, tablefmt="grid"))


def SATSolver(dontCareSuites, testCaseExpressions):
    FoundedIndex = -1
    parameters = []
    parametersValues = []

    for i in range(0, len(dontCareSuites)):
        tempValues = []
        if (FoundedIndex != dontCareSuites[i][0]):
            # print(int(dontCareSuites[i][0]) + 1, " rule expression ----->", dontCareSuites[i][1])
            # finds the satisfiable rules and writes test suite for them by using CnfFromString method
            exp, symbols = CnfFromString.create(dontCareSuites[i][1])
            solver = Minisat()
            solution = solver.solve(exp)
            if solution.success:
                FoundedIndex = dontCareSuites[i][0]
                # print("Rule :", int(dontCareSuites[i][0]) + 1)

                for symbol_name in symbols.keys():
                    # print("%s is %s" % (symbol_name, solution[symbols[symbol_name]]))
                    parameters.append((symbol_name, solution[symbols[symbol_name]], (int(dontCareSuites[i][0]) + 1)))
            else:
                # print("The expression cannot be satisfied")
                FoundedIndex = dontCareSuites[i][0]

            parametersValues.append(parameters)
            parameters = []

    for i in range(0, len(testCaseExpressions)):
        tempValues = []
        # print("Rule ", (int(testCaseExpressions[i][0])+1))
        # finds the satisfiable rules and writes test suite for them by using CnfFromString method
        exp, symbols = CnfFromString.create(testCaseExpressions[i][1])
        solver = Minisat()
        solution = solver.solve(exp)
        if solution.success:

            for symbol_name in symbols.keys():
                # print("%s is %s" % (symbol_name, solution[symbols[symbol_name]]))
                parameters.append((symbol_name, solution[symbols[symbol_name]], (int(testCaseExpressions[i][0]) + 1)))

        parametersValues.append(parameters)
        parameters = []

    ##----------suitable test order operation ---------##
    for m in range(0, len(parametersValues)):
        parametersValues[m] = sorted(parametersValues[m])

    return parametersValues



# ------------------- MAIN PART ----------------------------


#get the path of file from user (arg)
pathInput = str(sys.argv[1])

#prepares file for seperating data (read lines respectively)
content, fileName = PrepareToSeperateData("C:\\Users\Omer\Desktop\cs539\dt2")

conditions, conditionExpressions, conditionValues, outputs, outputValues = SeperateData(content)
InconsistentPairs, RedundantPairs = FindPairs(conditions, conditionExpressions, conditionValues, outputs, outputValues)
testCaseExpressions, dontCareIndexes, dontCareConditionsIndexes = WriteTestCases(conditionValues, conditions)
dontCareSuites = WriteTestCasesForDontCares(conditionValues, dontCareIndexes, dontCareConditionsIndexes, conditionExpressions)
parametersValues = SATSolver(dontCareSuites, testCaseExpressions)


PrintResults(fileName, InconsistentPairs, RedundantPairs, conditionValues)
PrintTestCaseTable(parametersValues, conditionValues)
