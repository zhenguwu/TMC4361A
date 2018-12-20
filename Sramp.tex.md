See S-shaped Ramping.png for a diagram

Equation Naming:

$d$ = Displacement, Change in position<br />
$v$ - Final velocity<br />
$v0$ - Initial velocity<br />
$a$ = Final acceleration<br />
$a0$ = Initial acceleration<br />
$j$ = jerk<br />
$t$ = time

Equations:
1) $v = v_0 + at$
2) $x = v_0t + \frac{1}{2}at^2$
3) $v^2 = v_0^2 + 2ad$
4) $a = a_0 + jt$
5) $v = v_0 + a_0t + \frac{1}{2}jt^2$
6) $d = v_0t + \frac{1}{2}a_0t^2 + \frac{1}{6}jt^3$

Configurable:<br />
aMax (Max acceleration)<br />
j1, j2, j3, j4 (Jerk)

Given(renaming for convenience):<br />
vStart = start_v (These values are passed into set_junction's parameter)<br />
vMax = cruise_v<br />
vFinal = end_v<br />
aChange = accel_r (Calculated from GRBL cornering alg) <br />
a = aMax * accel_r<br />
d = total_distance(Needs to be confirmed)

Sent to motion controller:<br />
XTARGET = d <br />
ASTART = vStart<br />
VMAX = vMax<br />
DFINAL = vFinal<br />
AMAX = a<br />
DMAX = a<br />
BOW1 = j1<br />
BOW2 = j2<br />
BOW3 = j3<br />
BOW4 = j4

To keep equations clean: Phase B1 = 1, B12 = 2, B2 = 3, B23 = 4, B3 = 5, B34 = 6, B4 = 7

Following equations apply when vStart = 0:

PhaseB1(1):<br />
$t_1 = \frac{a}{j_1}$<br />
$v_1 = \frac{1}{2}j_1t_1^2$<br />
$d_1 = \frac{1}{6}j_1t_1^3$

PhaseB12(2) - (Calculated from PhaseB1 and PhaseB2):<br />
$t_2 = \frac{v_3 - v_1}{a}$<br />
$d_2 = v_1t_2 + \frac{1}{2}at_2^2$

PhaseB2(3):<br />
$t_3 = \frac{a}{j_2}$<br />
$v_3 = vMax + \frac{1}{2}j_2t_3^2 - at_3$ <br />
$d_3 = v_3t_3 + \frac{1}{2}at_3^2 - \frac{1}{6}j_2t_3^3$

If vStart =/= 0, PhaseB1 is skipped and goes directly to B12 with $v_1 = vStart$


Following equations apply when vFinal = 0:

PhaseB3(5):<br />
$t_5 = \frac{a}{j_3}$<br />
$v_5 = vMax - \frac{1}{2}j_3t_5^2$<br />
$d_5 = vMax(t_5) - \frac{1}{6}j_3t_5^3$

PhaseB34(6) - (Calculated from PhaseB3 and PhaseB4):<br />
$t_6 = \frac{v_7 - v_5}{a}$<br />
$d_6 = v_5t_6 - \frac{1}{2}at_6^2$

PhaseB4(7):<br />
$t_7 = \frac{a}{j_4}$<br />
$v_7 = at_7 - \frac{1}{2}j_4t_7^2$ <br />
$d_7 = v_7t_7 - \frac{1}{2}at_7^2 + \frac{1}{6}j_4t_7^3$

If vFinal =/= 0, PhaseB4 is skipped and PhaseB34 is solved with $v_7 = vFinal$


PhaseB23(4) - (Calculated after all other phases):<br />
$t_4 = \frac{d_4}{vMax}$<br />
$d_4 = d - d_1 - d_2 - d_3 - d_5 - d_6 - d_7$ 