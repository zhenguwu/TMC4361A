See S-shaped Ramping.png for a diagram

Equation Naming:
$d$ = Displacement, Change in position
$v$ - Final velocity
$v0$ - Initial velocity
$a$ = Final acceleration
$a0$ = Initial acceleration
$j$ = jerk
$t$ = time

Equations:
1) $v = v0 + at$
2) $x = v_0t + \frac{1}{2}at^2$
3) $v^2 = v_0^2 + 2ad$
4) $a = a_0 + jt$
5) $v = v_0 + a_0t + \frac{1}{2}jt^2$
6) $d = v_0t + \frac{1}{2}a_0t^2 + \frac{1}{6}jt^3$

Configurable:
aMax (Max acceleration)
j1, j2, j3, j4 (Jerk)

Given(renaming for convenience):
vStart = start_v (These values are passed into set_junction's parameter)
vMax = cruise_v
vFinal = end_v
aChange = accel_r (Calculated from GRBL cornering alg) 
a = aMax * accel_r
d = total_distance(Needs to be confirmed)

Sent to motion controller:
ASTART = vStart
VMAX = vMax
DFINAL = vFinal
AMAX = a
DMAX = a
BOW1 = j1
BOW2 = j2
BOW3 = j3
BOW4 = j4


To keep equations clean: B1 = 1, B12 = 2, B2 = 3, B23 = 4, B3 = 5, B34 = 6, B4 = 7;
PhaseB1(1):
t1 = a / j1
v1 = vStart + 0.5(j1)(t1^2)
d1 = (vStart)(t1) + (1/6)(j1)(t1^3)

PhaseB12(2) - (Calculated from PhaseB1 and PhaseB2):
t2 = (v3 - v1) / a
d2 = (v1)(t2) + 0.5(a)(t2^2)

PhaseB2(3):
t3 = a / j2
v3 = vMax + 0.5(j2)(t3^2) - a(t3) *
d3 = (v3)(t3) + 0.5(a)(t3^2) - (1/3)(j2)(t3^3) **

PhaseB23(4) - (Calculated after all other phases):
t4 = d4 / vMax
d4 = d - d1 - d2 - d3 - d5 - d6 - d7

Note: acceleration is technically negative in the phases below

PhaseB3(5):
t5 = a / j3
v5 = vMax - 0.5(j3)(t5^2)
d5 = (vMax)(t5) - (1/6)(j3)(t5^3)

PhaseB34(6) - (Calculated from PhaseB3 and PhaseB4):
t6 = (v7 - v5) / a
d6 = (v5)(t6) - 0.5(a)(t6^2)

PhaseB4(7):
t7 = a / j4
v7 = vFinal + (a)(t7) - 0.5(j4)(t7^2) ***
d7 = d7 = (v7)(t7) - 0.5(a)(t7^2) + (1/3)(j4)(t7^3) ****


Derivations:

* Substitute equation 4 --> 5, replaces a0(unknown)
4) a = a0 + (j2)(t3) --> a0 = a - (j2)(t3)
5) vMax = v3 + (a0)(t3) + 0.5(j2)(t3^2) --> v3 = vMax - (a0)(t3) - 0.5(j2)(t3^2)
Substitute) v3 = vMax - (a - (j2)(t3))(t3) - 0.5(j2)(t3^2) --> v3 = vMax - a(t3) + 0.5(j2)(t3^2)

** Substitute equation 4 --> 6
4) a = a0 + (j2)(t3) --> a0 = a - (j2)(t3)
6) d3 = (v3)(t3) + 0.5(a0)(t3^2) + (1/6)(j2)(t3^3)
Substitute) d3 = (v3)(t3) + 0.5(a - (j2)(t3))(t3^2) + (1/6)(j2)(t3^3) --> d3 = (v3)(t3) + 0.5(a)(t3^2) - (1/3)(j2)(t3^3)
NOTE TRINAMIC HAD: d3 = (v3)(t3) + 0.5(a)(t3^2) - (1/6)(j2)(t3^3), but -0.5 + (1/6) = -(2/6) = -(1/3) not -(1/6) 

*** Substitute equation 4 --> 5
4) a = a0 + (j4)(t7) --> a0 = a - (j4)(t7)
5) vFinal = v7 - (a0)(t7) - 0.5(j4)(t7^2) --> v7 = vFinal + (a0)(t7) + 0.5(j4)(t7^2)
Substitute) v7 = vFinal + (a - (j4)(t7))(t7) + 0.5(j4)(t7^2) --> v7 = vFinal + (a)(t7) - 0.5(j4)(t7^2)

**** Substitute equation 4 --> 6
4) a = a0 + (j4)(t7) --> a0 = a - (j4)(t7)
5) d7 = (v7)(t7) - 0.5(a0)(t7^2) - (1/6)(j4)(t7^3)
Substitute) d7 = (v7)(t7) - 0.5(a - (j4)(t7))(t7^2) - (1/6)(j4)(t7^2) --> d7 = (v7)(t7) - 0.5(a)(t7^2) + (1/3)(j4)(t7^3)

NOTE TRINAMIC HAD: d3 = (v3)(t3) + 0.5(a)(t3^2) - (1/6)(j2)(t3^3), but -0.5 + (1/6) = -(2/6) = -(1/3) not -(1/6)
and d7 = (v7)(t7) - 0.5(a)(t7^2) + (1/6)(j4)(t7^3), but 0.5 - (1/6) = (1/3) not (1/6)