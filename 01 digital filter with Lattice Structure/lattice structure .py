import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from sympy import symbols, expand, simplify
'''
Mohammad Reza Mansouri  
num st : 4020723108
'''
print('\n \n ***********************Numerator & Denominator for G(Z) ***********************')

#------> G(z) ----- > It is in the form of problem assumptions
b = np.array([1, -0.5, 0.4, -0.3, 0.2, -0.1, 0.05, -0.02, 0.01, -0.005])
Lm = len(b)
z = sp.symbols('z')
B = sum(b[i] * z**(-i) for i in range(Lm))
BT = sp.conjugate(B.subs(z, 1 / sp.conjugate(z)))
Gz = ((z**(-(Lm - 1))) * BT) / B
print(f'numerator {((z**(-(Lm - 1))) * BT)}')
print(f'denominator : {B}')

#------> expand Of G(z)
numerator = sp.expand(sp.numer(Gz))
denominator = sp.expand(sp.denom(Gz))
denominator_coeffs = sp.Poly(denominator, z).all_coeffs()
print(f'denominator coeffs {denominator_coeffs}')



'''
In the section above, we formed 
G(z). In the next section, 
I will attempt to construct the denominator of 
Gm−1(z) and obtain Bm−1(z)
'''

print(' \n*********************** Calculate B(z) & BTild(Z)  ***********************')
#------> b
b = np.array(denominator_coeffs)
Lm = len(b)
#------> Bz(z)
z = sp.symbols('z')
Bz = sum(b[i] * z**(-i) for i in range(Lm))
print(f'Bz:{Bz}')
#------> BTild(z)
BTild = sp.conjugate(Bz.subs(z, 1 / sp.conjugate(z)))
print(f'BTild:{BTild}')



'''
I used one additional methods to calculate K_m besides the one taught in class.
I realized that only theK_m values obtained from the formula 
on page 35—the same formula taught in class—are stable and less than one.
'''


km_direct = np.zeros(Lm - 1)
km_direct = np.zeros(Lm - 1)
b_current = b.copy()
Bz_current = Bz
BTild_current = BTild


#------>Bm_1(z)---->  with  direct km
print('\n \n *********************** Calculate Bm_1(z)  ***********************')


for m in range(Lm - 1, 0, -1):
    index = Lm - m - 1
    km_direct[index] = b_current[m] / b_current[0]
    K = km_direct[index]
    Bm_1 = Bz_current - K * z ** (-m) * BTild_current
    Bm_1 = sp.simplify(Bm_1)
    if m==1:
        pass
    else:
        print(Bm_1)


    #  b_current
    coeff_dict = Bm_1.as_coefficients_dict()
    exponents = []
    for term in coeff_dict.keys():
        if term == 1:
            exp = 0
        else:
            powers = term.as_powers_dict()
            exp = powers.get(z, 0)
        exponents.append(exp)

    exponents = sorted(exponents, reverse=True)
    b_current = []
    for exp in exponents:
        term = z ** exp
        coeff = coeff_dict.get(term, 0)
        b_current.append(coeff)
    b_current = np.array(b_current, dtype=np.float64)
    Bz_current = Bm_1
    BTild_current = sp.conjugate(Bz_current.subs(z, 1 / sp.conjugate(z)))






#------> Output
print('\n \n *********************** Calculate Km  ***********************')

print("\nk_values (Direct Method):")
print(km_direct)

#------> Stability analysis with pole-zero plot for G(Z)

numerator_coeffs = sp.Poly(numerator, z).all_coeffs()
denominator_coeffs = sp.Poly(denominator, z).all_coeffs()

zeros = np.roots(numerator_coeffs)
poles = np.roots(denominator_coeffs)
# First Plot: Poles and Zeros Plot
fig, ax = plt.subplots()
ax.plot(np.real(zeros), np.imag(zeros), 'o', label='Zeros')
ax.plot(np.real(poles), np.imag(poles), 'x', label='Poles')
ax.add_artist(plt.Circle((0, 0), 1, color='b', fill=False, linestyle='--'))  # Unit circle
ax.set_xlabel('Real Part')
ax.set_ylabel('Imaginary Part')
ax.set_title('Poles and Zeros Plot For G(z)')
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.set_aspect('equal')
ax.legend()
plt.grid(True)

# Second Plot: Bar plot for km values
fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.bar(range(1, Lm), km_direct, color='skyblue')
ax2.axhline(1, color='red', linestyle='--', linewidth=0.8, label="Stability Threshold (+1)")
ax2.axhline(-1, color='red', linestyle='--', linewidth=0.8, label="Stability Threshold (-1)")
ax2.set_xlabel("Index")
ax2.set_ylabel("km Value")
ax2.set_title("km Values (Direct Method)")
ax2.legend()
ax2.grid(True)

# Show both plots
plt.show()

# Original stability analysis
if all(np.abs(poles) < 1):
    print('The system is stable (Pole-Zero Method).')
else:
    print('The system is unstable (Pole-Zero Method).')
