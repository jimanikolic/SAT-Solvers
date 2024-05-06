import random
import os
import time

#return the variable that minimizes the number of unsatisfied caluses in the new assignment
def getBestVariable(clauses, assignment):
    #Init Vars
    bestVariable = None
    xSatisfied = 0
    #Looks at each variable in a literal in an assignment
    for each in assignment:
        var = abs(each)

        #Assigns a T or F to test the effect
        assignment[var-1] = not assignment[var-1]

        #Determins the number of clauses that are satisfied after the change
        numSats = sum(1 for clause in clauses if isClauseSat(clause, assignment))

        #return variable to original value, flips back
        assignment[var-1] = not assignment[var-1]

        #Determines which variable makes the most clauses satisfied and returns it
        if numSats > xSatisfied:
            xSatisfied = numSats
            bestVariable = var
    return bestVariable

#Returns the max of the values passed in
def returnMax(x, y):
    return max(x, y)

#Returns the number of subclauses that are satisfied by given assignments
def genNumSatClauses(clauses, assignment):
    count = 0
    for subclause in clauses:
        if isClauseSat(subclause, assignment):
            count += 1
    return count

#Returns true if a clause has an assigned true, else it returns false
def isClauseSat(clause, assignment):
    for literal in clause:
        if literal > 0 and assignment[abs(literal)-1] or literal < 0 and not assignment[abs(literal)-1]:
            return True
    return False

#Runs isClauseSat on all clauses with given assignments
def allClausesSatisfied(clauses, assignment):
    return all(isClauseSat(subclause, assignment) for subclause in clauses)

def gsat(clauses, num_variables):
    #Init vars
    randomAssignment = [0 for _ in range(num_variables)]
    xSatisfied = 0

    #Set timeout conditions if ever stuck in local minima ARBITRAY
    max_flips = num_variables
    maxRestarts = 10

    #Looks at each variable in a clause
    for _ in range(maxRestarts):

        for i in range(num_variables):
            #Generate random assignments for all vars
            randomAssignment[i] = random.choice([True, False])
       
        for _ in range(max_flips):
            #Exit condition for satisfiable
            if allClausesSatisfied(clauses, randomAssignment):
                return True, xSatisfied, randomAssignment

            #If not satisfied, assign a probability
            p = random.randint(0, 99)

            #If the random assignment is satisfied, new random clause
            if p < 65:
                #Grab best var makes, minimizes the number of unsatisfied clauses in the new assignment
                flip = getBestVariable(clauses, randomAssignment)

                #If the value was true, its now false, and if it was false, it is now true
                randomAssignment[flip - 1] = not randomAssignment[flip - 1]

                #Calculate how many clauses are satisfied with random assignment, store it in most satisfied
                numSatisfied = genNumSatClauses(clauses, randomAssignment)
                xSatisfied = returnMax(xSatisfied, numSatisfied)

                #35% probability will enter, flip random var
            else:
                #Get random var from range of vars
                varToFlip = random.choice(range(num_variables))

                #Randomly assign it T or F
                randomAssignment[varToFlip - 1] = not randomAssignment[varToFlip - 1]

                #Get number of satisfied clauses
                numSatisfied = genNumSatClauses(clauses, randomAssignment)

                #Return the improvements
                xSatisfied = returnMax(xSatisfied, numSatisfied)

    return False, xSatisfied

#directoryPath = r'PA3_Benchmarks\CNF Formulas'
directoryPath = r'PA3_Benchmarks\HARD CNF Formulas'

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
            result = gsat(clauses, numVars)
            simplifications = int(simplifications)
            simplifications = numClauses - simplifications
            simplifications = str(simplifications)
            timeEnd = time.time()

            runTime = timeEnd-timeStart
            runTime = str(runTime)
            #print("Runtime:", timeEnd-timeStart)
            if result[0]:
                f = open("GSAToutput.txt", "a")
                f.write("file: "+ filename + " ")
                f.write("Clauses simplified: " + str(result[1]) + " ")
                f.write("S" + " " )
                f.write("Runtime: " + runTime + "\n")
                f.close()
            else:
                f = open("GSAToutput.txt", "a")
                f.write("file:" + filename + " ")
                f.write("Clauses simplified:" + str(result[1]) + " ")
                f.write("U" + " ")
                f.write("Runtime:" + runTime + "\n")
                f.close()