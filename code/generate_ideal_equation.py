import sympy as sp

def generate_ideal_equation(polynomial_degree, only_x_level=False):
    # Generiert die Gleichung des Ideals fuer einen bestimmten Grad von I

    def generate_polynomial_term(variables, degree, coefficient_name, start=0, term=1, current_degree=0, polynom=0, c=None):
        # Rekursive Funktion, die ein Polynom n-ten Grades generiert
        
        term = sp.sympify(term).subs("w", 1)
        if c is None:
            c = {}
        
        if current_degree >= degree:
            # Erzeugen einer passenden Koeffizientenbezeichnung
            c[len(c) + 1] = sp.symbols(f"{coefficient_name}_{{{term}}}")
            return polynom + c[len(c)] * term, c

        for i in range(start, len(variables)):
            polynom, c = generate_polynomial_term(variables, degree, coefficient_name, i, term=term * variables[i], current_degree=current_degree + 1, polynom=polynom, c=c)

        # Das Polynom und die Koeffizienten werden zurueckgegeben
        return polynom, c
                

    variables = sp.symbols("X y p_x p_y w")
    
    # Generiert das Polynom I
    I, c = generate_polynomial_term(variables, polynomial_degree, "c")
    print()
    print(I)
    print()
    I = I.subs("c_{1}", 0)

    # Generiert das Polynom g
    g, b = generate_polynomial_term(variables, 1, "b")
    
    f, a = generate_polynomial_term(variables, polynomial_degree - 2, "a")

    C = sp.Symbol("C")
    E = sp.Symbol("E")
    H = (variables[2]**2 + variables[3]**2 + variables[0]**2 + variables[1]**2) / 2 + variables[0]**2*variables[1] - variables[1]**3 / 3


    # Definiert die Gleichung fuer Ideal(H − E, I − C)
    ideal_equation = sp.Eq(
        sp.diff(I, variables[0]) * sp.diff(H, variables[2]) + 
        sp.diff(I, variables[1]) * sp.diff(H, variables[3]) - 
        sp.diff(I, variables[2]) * sp.diff(H, variables[0]) -
        sp.diff(I, variables[3]) * sp.diff(H, variables[1]),
        f * (H - E) + g * (I - C)
        )


    # Falls x = 0
    if only_x_level:
        ideal_equation = ideal_equation.subs("X", 0)
        

    # Zurueckgeben der Gleichung und der Variablen
    return ideal_equation, variables

if __name__ == "__main__":
    degree = 2
    ideal_equation, variables = generate_ideal_equation(degree)
    print(sp.latex(ideal_equation))