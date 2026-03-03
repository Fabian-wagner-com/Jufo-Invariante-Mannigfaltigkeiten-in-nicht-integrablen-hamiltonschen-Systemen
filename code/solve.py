import generate_ideal_equation
import sympy as sp
import time

degree = 2
only_x_level = False
max_subcase = 50

start_time = time.time()

# erzeugt die Gleichung für das Ideal
ideal_equation, variables = generate_ideal_equation.generate_ideal_equation(degree, only_x_level)

# aufteilen der linken und rechten Seite
left = ideal_equation.lhs
right = ideal_equation.rhs

# Differenz der Terme
diff = sp.expand(left - right)

# Polynom
poly = sp.Poly(diff, *variables)

# Koeffizienten extrahieren
terms = poly.terms()
equations = [sp.Eq(coeff, 0, evaluate=False) for exponent, coeff in terms]
used_symbols = set().union(*[eq.free_symbols for eq in equations])


# alle cs mit x rausfiltern
if only_x_level:
    used_symbols = {symbol for symbol in used_symbols if "X" not in str(symbol)}

# Ausgabe aller relevanter Symbole
print(used_symbols)

unique_solutions = set()

def case_solver(new_equations, knowns=[], subcase=0, first=False, path=None):
    # Vereinfachung und Loesung des GLS
    
    global max_subcase
    global stop

    # Ausgabe des Fortschritts
    print("Aktueller Subfall:", ".".join(map(str, path)) if path else "Start")
    

    if len(path) >= max_subcase:
        # loest das vereinfachte GLS, wenn max_subcase erreicht ist
        
        solutions = sp.nonlinsolve(new_equations, list(used_symbols))
        subs_dict = dict([(s, 0) for s in knowns])
        
        for sol in solutions:
            full_sol = tuple(val.subs(subs_dict) for val in sol)
            unique_solutions.add(full_sol)
        return

    more_cases = False
    
    number_of_eq = 0

    for eq in new_equations:
        # sucht passende Gleichungen und vereinfacht
        
        symbol = eq.free_symbols
        
        if isinstance(eq, sp.Equality) and eq.lhs.is_Mul:
            factors = eq.lhs.args
            more_cases = True
            for idx, f in enumerate(factors):
                if not f.is_real:                    
                    new_eqs = [e.subs(f, 0) if e != eq else sp.Eq(f, 0) for e in new_equations]
                    case_solver(new_eqs, knowns + [f], subcase + 1, path=path + [idx + 1])
            return

    if more_cases == False:
        # loest, falls keine neuen Subfälle erzeugt werden koennen
        
        print(new_equations)
        print(unique_solutions)
        
        solutions = sp.nonlinsolve(new_equations, list(used_symbols))

        subs_dict = dict([(s, 0) for s in knowns])
        for sol in solutions:
            full_sol = tuple(val.subs(subs_dict) for val in sol)
            unique_solutions.add(full_sol)
            print(unique_solutions)
        return

# startet loesen durch Bildung von Subfällen
case_solver(equations, first=True, path=[])

print("write txt file...")


addition = ""

if only_x_level:
    addition = "_nur_x_Ebene"


with open (f"Loesungen/step_by_step/Loesungen_Grad_{degree}{addition}_mit_{max_subcase}_subfällen.txt", "w", encoding="utf-8") as file:
    # speichern der Ergebnisse in einer Textdatei
    
    file.write(f"GRAD {degree} mit maximal {max_subcase} Subfällen: \n \n \n Alle equations ({len(equations)}): \n")
    
    for gleichung in list(equations):
        file.write(sp.latex(gleichung))
        file.write("\n")

    
    file.write(f"\n \n Die {len(unique_solutions)} Lösungen sind: \n")
    i = 0
    for solution in unique_solutions:
        i = i + 1
        file.write(f"Loesung {i}: \n")
        file.write("\\begin{equation} \n \\begin{aligned}")
        file.write(" \\\\ \n".join(f"{var} = {value}" for var, value in zip(used_symbols, solution)))
        file.write("\n \\end{aligned} \n \\end{equation}")
        file.write("\n \n")
        
    duration = round(time.time() - start_time, 2)
        
    file.write(f"\n \n \n Dauer: {duration} Sekunden")
    
print("ready!!!")




