See S-shaped Ramping.png for a diagram

Equation Naming:
<img src="/tex/2103f85b8b1477f430fc407cad462224.svg?invert_in_darkmode&sanitize=true" align=middle width=8.55596444999999pt height=22.831056599999986pt/> = Displacement, Change in position
<img src="/tex/6c4adbc36120d62b98deef2a20d5d303.svg?invert_in_darkmode&sanitize=true" align=middle width=8.55786029999999pt height=14.15524440000002pt/> - Final velocity
<img src="/tex/ae5d2b8055caea8d4ee5dce2aff72c2c.svg?invert_in_darkmode&sanitize=true" align=middle width=16.77705149999999pt height=21.18721440000001pt/> - Initial velocity
<img src="/tex/44bc9d542a92714cac84e01cbbb7fd61.svg?invert_in_darkmode&sanitize=true" align=middle width=8.68915409999999pt height=14.15524440000002pt/> = Final acceleration
<img src="/tex/bc437d770056a8290a36f089fd92b5a9.svg?invert_in_darkmode&sanitize=true" align=middle width=16.908363449999992pt height=21.18721440000001pt/> = Initial acceleration
<img src="/tex/36b5afebdba34564d884d347484ac0c7.svg?invert_in_darkmode&sanitize=true" align=middle width=7.710416999999989pt height=21.68300969999999pt/> = jerk
<img src="/tex/4f4f4e395762a3af4575de74c019ebb5.svg?invert_in_darkmode&sanitize=true" align=middle width=5.936097749999991pt height=20.221802699999984pt/> = time

Equations:
1) <img src="/tex/a1c43925c3fc1a0a978eeba0487352d9.svg?invert_in_darkmode&sanitize=true" align=middle width=81.96896564999999pt height=21.18721440000001pt/>
2) <img src="/tex/720d887aadd7d459717582ba229f23d8.svg?invert_in_darkmode&sanitize=true" align=middle width=104.35796909999999pt height=27.77565449999998pt/>
3) <img src="/tex/ade6d1df67e8b51b1e41bfbe43cebb03.svg?invert_in_darkmode&sanitize=true" align=middle width=99.33775169999998pt height=26.76175259999998pt/>
4) <img src="/tex/720946709182e4072c855fdbe28f4b23.svg?invert_in_darkmode&sanitize=true" align=middle width=80.40810524999999pt height=21.68300969999999pt/>
5) <img src="/tex/e225177103b17f458179108945d4ba11.svg?invert_in_darkmode&sanitize=true" align=middle width=138.69689129999998pt height=27.77565449999998pt/>
6) <img src="/tex/d0a5b4a99ce9c93fccc34eedb975e7c4.svg?invert_in_darkmode&sanitize=true" align=middle width=162.50330909999997pt height=27.77565449999998pt/>

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