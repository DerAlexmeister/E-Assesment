import random

SIGNS = [True, False]


def checkResolution(monom, gates):
    for gate in gates:
        diff = monom.symmetric_difference(gate)
        if len(diff) == 2:
            lit1, lit2 = list(diff)
            if lit1[1] == lit2[1]\
               and lit1[0] == (not lit2[0]):
                return True
    return False

def subsumes(monom, gates):
    differences = set()
    for gate in gates:
        if monom.issubset(gate):
            differences.update(gate.difference(monom))
    return differences

def isSubsumed(monom, gates):
    for gate in gates:
        if monom.issuperset(gate):
            return True
    return False

def chooseAnd(monom, literals, gates):
    literals = literals.copy()
    monom = monom.copy()
    while literals:
        literal = random.choice(list(literals))
        literals.remove(literal)
        monom.add(literal)

        if checkResolution(monom, gates) or isSubsumed(monom, gates):
            monom.remove(literal)
            continue

        complement = not literal[0], literal[1]
        without_complement = literals.copy()
        without_complement.discard(complement)


        diff = subsumes(monom, gates)
        if diff:
            new_literals = without_complement.difference(diff)
            result = chooseAnd(monom, new_literals, gates)
            if result:
                return result
            else:
                monom.remove(literal)
                continue

        if not literals or random.choice(SIGNS):
            return monom
        else:
            result = chooseAnd(monom, without_complement, gates)
            if result:
                return result
            else:
                monom.remove(literal)
                continue

    return None



def chooseOr(literals, gates, num_ors: int):
    if len(gates) >= num_ors:
        return gates

    tabu = gates.copy()
    while True:
        monom = chooseAnd(set(), literals, tabu)
        if monom is None:
            return None

        gates.append(monom)
        result = chooseOr(literals, gates, num_ors)
        if result:
            return result

        tabu.append(gates.pop(-1))


def  minimalByConstruction(variables, num_ors):
    literals = {
        (sign, var)
        for var in variables
        for sign in SIGNS
    }

    gates = []
    return chooseOr(literals, gates, num_ors)
