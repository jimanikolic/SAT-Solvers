import os
import time
"""
About: https://en.wikipedia.org/wiki/DPLL_algorithm
"""
def DPLL(clauses):
    #Retrieve a clause and simplify clauses
    while True:
        unitClause = findUnitClause(clauses)
        if not unitClause:
            break
        clauses = unitPropagate(unitClause, clauses)
        storeSimplifications(clauses)
    
    #While there is a pure literal in the set, simplify clauses
    while True:
        pureLiteral = findPureLiteral(clauses)
        if not pureLiteral:
            break
        clauses = pureLiteralAssign(pureLiteral, clauses)
        storeSimplifications(clauses)
    
    #While there is a unit clause in the set, if no more clauses, the set is satisfiable
    if not clauses:
        return True
    
    #If the set contains any empty clauses, clauses are unsatisfiable
    if any(len(clause) == 0 for clause in clauses):
        return False
    
    #If there are still clauses left in the set, we need to assign truth, choose a literal
    literal = chooseLiteral(clauses)

    #Run DPLL twice, one for "true", one for "false".
    #If either returns true, a satisfying is found, else not found.
    storeSimplifications(clauses)
    return DPLL(clauses + [[literal]]) or DPLL(clauses + [[-literal]])

#Find a unit clause based off length
def findUnitClause(clauses):
    for clause in clauses:
        if len(clause) == 1:
            return clause[0]
    return None

#Takes a unit clause, 
def unitPropagate(literal, clauses):
    #Filter out clauses that contain the literal, create a new list of clauses
    clauses = [clause for clause in clauses if literal not in clause]
    #Return list of clauses, removing unit literals and their negations from the list of clauses, increase num simplifications done
    return [[l for l in clause if l != -literal] for clause in clauses]

def findPureLiteral(clauses):
    #Create a set called literals, iterate each literal within each clause, collect all unique literals
    literals = set(literal for clause in clauses for literal in clause)
    pureLiterals = set()
    
    #If a negated version of literal not present, it is pure
    for literal in literals:
        if -literal not in literals:
            pureLiterals.add(literal)
    #If there are pure literals return one
    return pureLiterals.pop() if pureLiterals else None

def pureLiteralAssign(literal, clauses):
    #Return list of clauses without any pure literals, increase number of simplifications done
    return [clause for clause in clauses if literal not in clause]

def chooseLiteral(clauses):
    #Choose the first literal of the first clause, to be assigned
    return clauses[0][0]

def storeSimplifications(clauses):
    global simplifications
    simplifications = len(clauses)

#directoryPath = r"PA3_Benchmarks\PA3_Benchmarks\CNF Formulas"
directoryPath = r"PA3_Benchmarks\PA3_Benchmarks\HARD CNF Formulas"

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
        timeStart = time.time()
        result = DPLL(clauses)
        simplifications = numClauses - simplifications
        simplifications = str(simplifications)
        timeEnd = time.time()

        runTime = timeEnd-timeStart
        runTime = str(runTime)
        #print("Runtime:", timeEnd-timeStart)
        if result:
            f = open("output.txt", "a")
            f.write("file: "+ filename + " ")
            f.write("Clauses simplified: " + simplifications + " ")
            #f.write("Result: SATISFIABLE" + "\n" )
            f.write("Runtime: " + runTime + "\n")
            f.close()
        else:
            f = open("output.txt", "a")
            f.write("file:" + filename + " ")
            f.write("Clauses simplified:" + simplifications + " ")
            #f.write("Result: UNSATISFIABLE" + " ")
            f.write("Runtime:" + runTime + "\n")
            f.close()
            

