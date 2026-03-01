import generate_ideal_equation
import sympy as sp
import time
import os

# beliebiger Grad fur das Polynom I
degree = 2

start_time = time.time()

# erzeugt die Gleichung fur Ideal
ideal_equation, variables = generate_ideal_equation.generate_ideal_equation(degree, True)

# aufteilen der linken und rechten Seite der Gleichung
left = ideal_equation.lhs
right = ideal_equation.rhs

# erzeugt Subtraktion der zwei Terme
diff = sp.expand(left - right)

# Polynomdarstellungdes
poly = sp.Poly(diff, *variables)

# zerlegen in die einzelen Terme vor den Variablen
terms = poly.terms()



# speichert einzelne Koeffizienten in Gleichungen gleich Null
equations = [sp.Eq(coeff, 0, evaluate=False) for exponent, coeff in terms]


# findet die verwendeten Symbole in den Gleichungen
used_symbols = set().union(*[eq.free_symbols for eq in equations])


'''
# filtert alle c's raus
filtered_symbols = {symbol for symbol in used_symbols if str(symbol).startswith('c')}
'''

shortened_equations = [equations[j] for j in range(len(used_symbols))]

print(shortened_equations)

print(len(equations), len(shortened_equations), len(used_symbols))

# lost die Gleichungen nach den Symbolen
solutions = sp.solve(shortened_equations, used_symbols)

# Ausgabe der Losungen
print(solutions)

# berechnet die benotigte Zeit
duration = round(time.time() - start_time, 2)
print(duration)

'''
with open (f"Loesungen/Loesungen_Grad_{degree}.txt", "w") as file:
    # speichern der Ergebnisse in einer Textdatei
    
    file.write(f"GRAD 2: \n \n \n Alle equations ({len(equations)}): \n")
    for gleichung in list(equations):
        file.write(sp.latex(gleichung))
        file.write("\n")
        
    file.write(f"\n \n Die Lösung hat nur folgende equations beachtet ({len(shortened_equations)}): \n")
    for gleichung in list(shortened_equations):
        file.write(sp.latex(gleichung))
        file.write("\n")
    
    file.write("\n \n Die Lösungen sind: \n")
    for solution in solutions:
        file.write(sp.sstr(solution))
    file.write(f"\n \n \n Alle Variablen sind {used_symbols}")
    file.write(f"\n \n \n Dauer: {duration} Sekunden")
    
'''
    
print(f"fertig für Grad {degree}")