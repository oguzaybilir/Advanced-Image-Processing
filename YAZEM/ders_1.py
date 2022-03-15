import sympy as smp
import math
import sympy.integrals.trigonometry as trig


x = smp.symbols('x')
y = smp.symbols('y')
a = smp.symbols('a')
c = smp.symbols('c')

y = smp.integrate(smp.sin(x)**2,str(smp.sin(x)))

print(y)

