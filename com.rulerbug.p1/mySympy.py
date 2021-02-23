from sympy import *
x=symbols("x")
y=symbols("y")
fx=3*x+4/y
result=fx.evalf(subs={x:1,y:12})
print(result)
print(solve(fx,x,y))