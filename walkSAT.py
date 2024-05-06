import random
import os
import time

def getBestVariable(clauses, clause, assignment):
    #Init Vars
    bestVariable = None
    mostSatisfied = 0

    #Looks at each variable in a clause
    for each in clause:
        var = abs(each)

        #Assigns a T or F to test the effect
        assignment[var-1] = not assignment[var-1]

        #Determins the number of clauses that are satisfied after the change
        numSats = sum(1 for subclause in clauses if isClauseSat(subclause, assignment))

        #return variable to original value, flips back
        assignment[var-1] = not assignment[var-1]

        #Determines which variable makes the most clauses satisfied and returns it
        if numSats > mostSatisfied:
            mostSatisfied = numSats
            bestVariable = var
    return bestVariable

#Returns max of the two ints passed to it
def returnMax(x, y):
    return max(x, y)

#Returns the number of subclauses that are satisfied by given assignments
def genNumSatClauses(clauses,assignment):
    return sum(1 for subclause in clauses if isClauseSat(subclause, assignment))

#Returns true if a clause has an assigned true, else it returns false
def isClauseSat(clause, assignment):
    for literal in clause:
        if literal > 0 and assignment[abs(literal)-1] or literal < 0 and not assignment[abs(literal)-1]:
            return True
    return False

#Runs isClauseSat on all clauses with given assignments
def allClausesSatisfied(clauses, assignment):
    return all(isClauseSat(subclause, assignment) for subclause in clauses)

def WalkSAT(clauses, numVariables):
    #Generate random assignments for all vars
    randomAssignment = [random.choice([True, False]) for _ in range(numVariables)]
    xSatisfied = 0

    #Set timeout conditions if ever stuck in local minima ARBITRAY
    maxFlips = numVariables * 3
    maxRetries = 100

    #The for loop is another timeout condition, representing max number of retries
    for _ in range(maxRetries):

        #Gen random assignmet for numVars
        currentAssignment = [random.choice([True, False]) for _ in range(numVariables)]
        currentSatCount = genNumSatClauses(clauses, currentAssignment)

        for i in range(numVariables):
            randomAssignment[i] = random.choice([True, False])

        for _ in range(maxFlips):
            #Exit condition for satisfiable
            if allClausesSatisfied(clauses, randomAssignment):
                return True, xSatisfied, randomAssignment
            
            #If not satisfied, assign a probability
            p = random.randint(0, 99)

            #Randomly grab a clause in which a var will be flipped
            randomClause = random.choice(clauses)

            #If the random assignment is satisfied, new random clause
            while isClauseSat(randomClause, randomAssignment):
                randomClause = random.choice(clauses)

            #Enter with 65% probability, flip best var
            if p < 65:
                #Grab best var, in the random clause, flip it
                flip = getBestVariable(clauses, randomClause, randomAssignment)
                
                #If the value was true, its now false, and if it was false, it is now true
                randomAssignment[flip - 1] = not randomAssignment[flip - 1]

                #Calculate how many clauses are satisfied with random assignment, store it in most satisfied
                numSatisfied = genNumSatClauses(clauses, randomAssignment)
                xSatisfied = returnMax(numSatisfied, xSatisfied)

            #35% probability will enter, flip random var
            else:
                flip = random.choice(randomClause)
                varIndex = abs(flip) - 1
                currentAssignment[varIndex] = not currentAssignment[varIndex]
                currentSatCount = genNumSatClauses(clauses, currentAssignment)
    return False, xSatisfied


#directoryPath = r"PA3_Benchmarks\CNF Formulas"
directoryPath = r"PA3_Benchmarks\HARD CNF Formulas"

for filename in os.listdir(directoryPath):
    if filename.endswith(".cnf"):  # Process only files with the .cnf extension
        filePath = os.path.join(directoryPath, filename)

        # Initialize variables to store data for each file
        numVars = None
        numClauses = None
        clauses = []
        simplifications = 0

        with open(filePath, 'r') as file:
            lines = file.readlines()
            
            for line in lines:
                line = line.strip()
                
                if not line:
                    continue
                
                if line.startswith('p cnf'):
                    numVars, numClauses = line.split()[2:]
                    numVars = int(numVars)
                    numClauses = int(numClauses)
                elif line.startswith('%'):
                    break
                elif not line.startswith('c'):
                    line_data = line.split()[:3]
                    row = [int(num) for num in line_data]
                    clauses.append(row)

        # Now you have extracted data for the current file, and you can handle it as needed
        #print("Number of Variables:", numVars)
        #print("Number of Clauses:", numClauses)
        for i in range(10):
            timeStart = time.time()
            result = WalkSAT(clauses, numVars)
            simplifications = int(simplifications)
            simplifications = numClauses - simplifications
            simplifications = str(simplifications)
            timeEnd = time.time()

            runTime = timeEnd-timeStart
            runTime = str(runTime)
            #print("Runtime:", timeEnd-timeStart)
            if result[0]:
                f = open("WALKoutput.txt", "a")
                f.write("file: "+ filename + " ")
                f.write("Clauses simplified: " + str(result[1]) + " ")
                f.write("S" + " " )
                f.write("Runtime: " + runTime + "\n")
                f.close()
            else:
                f = open("WALKoutput.txt", "a")
                f.write("file:" + filename + " ")
                f.write("Clauses simplified:" + str(result[1]) + " ")
                f.write("U" + " ")
                f.write("Runtime:" + runTime + "\n")
                f.close()