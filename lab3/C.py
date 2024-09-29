import random
import itertools

def clause_gen(n, m, k):
    variables = random.sample([chr(i) for i in range(97, 123)], n)
    clauses = []
    
    for _ in range(m):
        clause = random.sample(variables, k)
        clause = [var if random.random() < 0.5 else f'!{var}' for var in clause]
        clauses.append(clause)
    
    expression = '&'.join('(' + '|'.join(clause) + ')' for clause in clauses)
    print(f"Variables are: {variables}")
    print(f"Expression Generated is: {expression}")
    return expression, variables

def parse(expression, variables, assignment):
    expr = expression
    for var, val in zip(variables, assignment):
        expr = expr.replace(var, str(val))
        expr = expr.replace(f'!{str(val)}', str(1-val))
    
    clauses = expr.split('&')
    return sum(eval(clause.strip('()')) for clause in clauses)

def hill_climbing(expression, variables, m, n, max_iterations=1000):
    current = [random.randint(0, 1) for _ in range(n)]
    for _ in range(max_iterations):
        if parse(expression, variables, current) == m:
            return current
        
        neighbors = []
        for i in range(n):
            neighbor = current.copy()
            neighbor[i] = 1 - neighbor[i]
            neighbors.append((neighbor, parse(expression, variables, neighbor)))
        
        best_neighbor = max(neighbors, key=lambda x: x[1])
        if best_neighbor[1] <= parse(expression, variables, current):
            return current
        current = best_neighbor[0]
    return current

def beam_search(expression, variables, m, n, width, max_iterations=1000):
    beam = [[random.randint(0, 1) for _ in range(n)] for _ in range(width)]
    
    for _ in range(max_iterations):
        candidates = []
        for assignment in beam:
            if parse(expression, variables, assignment) == m:
                return assignment
            
            for i in range(n):
                neighbor = assignment.copy()
                neighbor[i] = 1 - neighbor[i]
                candidates.append((neighbor, parse(expression, variables, neighbor)))
        
        beam = [x[0] for x in sorted(candidates, key=lambda x: x[1], reverse=True)[:width]]
    
    return max(beam, key=lambda x: parse(expression, variables, x))

def variable_neighborhood_descent(expression, variables, m, n, max_neighbors=3, max_iterations=1000):
    current = [random.randint(0, 1) for _ in range(n)]
    
    for _ in range(max_iterations):
        if parse(expression, variables, current) == m:
            return current
        
        improved = False
        for k in range(1, max_neighbors + 1):
            neighbors = []
            for indices in itertools.combinations(range(n), k):
                neighbor = current.copy()
                for i in indices:
                    neighbor[i] = 1 - neighbor[i]
                neighbors.append((neighbor, parse(expression, variables, neighbor)))
            
            best_neighbor = max(neighbors, key=lambda x: x[1])
            if best_neighbor[1] > parse(expression, variables, current):
                current = best_neighbor[0]
                improved = True
                break
        
        if not improved:
            return current
    
    return current

def main():
    n = int(input('Enter the number of variables: '))
    m = int(input('Enter the number of clauses: '))
    k = int(input('Enter the number of variables in one clause: '))
    width = int(input("Enter the beam width: "))
    
    expression, variables = clause_gen(n, m, k)
    
    hc_solution = hill_climbing(expression, variables, m, n)
    bs_solution = beam_search(expression, variables, m, n, width)
    vnd_solution = variable_neighborhood_descent(expression, variables, m, n)
    
    print(f"Hill Climbing solution: {hc_solution}, Satisfied clauses: {parse(expression, variables, hc_solution)}/{m}")
    print(f"Beam Search solution: {bs_solution}, Satisfied clauses: {parse(expression, variables, bs_solution)}/{m}")
    print(f"Variable Neighborhood Descent solution: {vnd_solution}, Satisfied clauses: {parse(expression, variables, vnd_solution)}/{m}")

if __name__ == "__main__":
    main()