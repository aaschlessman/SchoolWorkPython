#Aaron Schlessman
#CS4630
#Homework5
#Kinematics

import sympy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import display, clear_output

t, a, v_t, s_t, v_x, v_y, s_x, s_y = sympy.symbols('t, a, v_t, s_t, v_x, v_y, s_x, s_y')
v_i, vx_i, vy_i, s_i, sx_i, sy_i = sympy.symbols('v_i, vx_i, vy_i, s_i, sx_i, sy_i')

g = 9.8
ng = -g

Input = input("Input the Height (meters) above the ground the projectile is shot from, Initial projectile velocity (meters/s) and Angle (degrees) of the projectile : ").strip().split()
InputHeight = int(Input[0])
InputVelocity = int(Input[1])
InputAngle = int(Input[2])

v_t = sympy.Integral(a, t)

s_t = sympy.Integral(v_t, t)
pvt = v_t
pst = s_t

v_t = sympy.integrate(a, t) + v_i
v_y = v_t.subs([(a, ng),(v_i, vy_i)])

vy_initial = InputVelocity * sympy.sin(np.radians(InputAngle))

tMax_eq = v_y.subs([(vy_i, vy_initial)])
t_Max = sympy.solve(tMax_eq, t)
t_Max = t_Max[0]

s_t = sympy.integrate(v_t, t) + s_i
s_y = s_t.subs([(a, ng),(s_i, sy_i),(v_i, vy_i)])

max_h = s_y.subs([(sy_i, InputHeight),(t, t_Max),(vy_i, vy_initial)])

t_ground_eq = s_y.subs([(sy_i, InputHeight),(vy_i, vy_initial)])
t_ground = sympy.solve(t_ground_eq, t)

if (t_ground[1]):
    t_ground = t_ground[1]
else:
    t_ground = t_ground[0]

vx_initial = InputVelocity * sympy.cos(np.radians(InputAngle))

s_x = s_t.subs([(a, 0),(s_i, sx_i),(v_i, vx_i)])
total_distance = s_x.subs([(sx_i, 0),(t, t_ground),(vx_i, vx_initial)])

x = []
y = []
t_range = np.linspace(0, float(t_ground), num=200)
for element in t_range:
    x.append(s_x.subs([(sx_i, 0),(t, element),(vx_i, vx_initial)]))
    y.append(s_y.subs([(sy_i, InputHeight),(t, element),(vy_i, vy_initial)]))

v_x = v_t.subs([(a, 0),(v_i, vx_i)])

display('Hardcoded Equations [Velocity  & Displacement]', pvt, pst)
display('Derived Velocity Equation [v_x]:', v_x)
display('Derived Velocity Equation [vy]:', v_y)
display('Derived Displacement Equation [s_x]', s_x)
display('Derived Displacement Equation [s_y]', s_y)
print('Time to max height (sec)', t_Max)
print('Max height (m):', max_h)
print('Range (m):', total_distance)

fig1, ax1 = plt.subplots()
ax1.set_ylabel('Height (m)')
ax1.set_xlabel('Range (m)')
ax1.set_title('Projectile Path')
ax1.plot(x, y)
plt.show()

#animation credit to https://www.geeksforgeeks.org/using-matplotlib-for-animations/

clear_output()

fig2 = plt.figure()
xc = total_distance + 50
yc = max_h + 50
ax2 = plt.axes(xlim =(-50, float(xc)), 
               ylim =(-50, float(yc)))
ax2.set_ylabel('Height (m)')
ax2.set_xlabel('Range (m)')
ax2.set_title('Projectile Path')
line, = ax2.plot([], [], lw = 2)  

def initialize():
    line.set_data([], [])
    return (line,)

x_data = []
y_data = []

def animate(i):
    x_data = x[:i]
    y_data = y[:i]
    line.set_data(x_data, y_data)
    return (line,)

animationlength = len(x)

ani = animation.FuncAnimation(fig2, animate, frames=animationlength, init_func = initialize, interval = 10, blit = True)

ani.save('Projectile Path.gif', fps = 15)