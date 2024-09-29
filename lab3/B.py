import random


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

def main():
    n = int(input('Enter the number of variables: '))
    m = int(input('Enter the number of clauses: '))
    k = int(input('Enter the number of variables in one clause: '))
    
    expression, variables = clause_gen(n, m, k)


if __name__ == "__main__":
    main()