# Python3
import numpy as np
import matplotlib.pyplot as plt

# Graph Resolution
res = 0.00005

# Ramp Configuration
xtarget = 5      # mm
vstart = 0       # mm/s
vmax = 100       # mm/s
vfinal = 0       # mm/s
accel = 4000     # mm/s^2
jerk1 = 1000000  # mm/s^3
jerk2 = 1000000  # mm/s^3
jerk3 = 1000000  # mm/s^3
jerk4 = 1000000  # mm/s^3

# Initializing Variables
time1 = 0
time3 = accel/jerk2
time4 = 0
time5 = accel/jerk3
time6 = 0
time7 = 0
vel1 = 0
vel3 = vmax + 0.5 * jerk2 * time3**2 - accel * time3
vel5 = vmax - 0.5 * jerk3 * time5**2
vel7 = 0
d1 = 0
d2 = 0
d3 = vel3 * time3 + 0.5 * accel * time3**2 - (1/6) * jerk2 * time3**3
d4 = 0
d5 = vmax * time5 - (1/6) * jerk3 * time5**3
d6 = 0
d7 = 0


if vstart == 0:
    # Initial velocity = 0
    time1 = accel/jerk1
    vel1 = 0.5 * jerk1 * time1**2
    d1 = (1/6) * jerk1 * time1**3
else:
    # Initial velocity =/= 0
    #time1 = 0  Note: These are not necessary as variables start off as 0, just here for acknowledgement
    vel1 = vstart
    #d1 = 0
time2 = (vel3  - vel1) / accel
d2 = vel1 * time2 + 0.5 * accel * time2**2

if vfinal == 0:
    # Final velocity = 0
    time7 = accel/jerk4
    vel7 = accel * time7 - 0.5 * jerk4 * time7**2
    d7 = vel7 * time7 - 0.5 * accel * time7**2 + (1/6) * jerk4 * time7**3
else:
    # Final velocity =/= 0
    #time7 = 0 
    vel7 = vfinal
    #d7 = 0
time6 = (vel5 - vel7) / accel
d6 = vel5 * time6 - 0.5 * accel * time6**2

d4 = xtarget - d1 - d2 - d3 - d5 - d6 - d7
time4 = d4 / vmax

# Make sure nothing is negative
times = [time1, time2, time3, time4, time5, time6, time7]
times = [i if i >=0 else 0 for i in times]
times1 = times[0]
times2 = times[1]
times3 = times[2]
times4 = times[3]
times5 = times[4]
times6 = times[5]
times7 = times[6]

print(times)
print(d1, d2, d3, d4, d5, d6, d7)


def graph():
    t, v = phase()
    plt.plot(t, v)
    plt.show()

def phase():
    t = np.arange(0, time1 + time2 + time3 + time4 + time5 + time6 + time7, res)
    v = []

    # Solve for slope and intercept for phases of constant acceleration
    m1, c1 = lineEq((time1, vel1), (time1 + time2, vel3))
    m2, c2 = lineEq((time1 + time2 + time3 + time4 + time5, vel5), (time1 + time2 + time3 + time4 + time5 + time6, vel7))

    # Sorry this is not very efficient
    for time in t:
        if 0 <= time and time < times1:
            v.append(0.5 * jerk1 * time**2)
        elif times1 <= time < time1 + time2:
            v.append(m1 * time  + c1)
        elif time1 + time2 <= time and time < time1 + time2 + time3:
            time -= time1 + time2
            v.append(vel3 - 0.5 * jerk2 * time**2 + accel * time)
        elif time1 + time2 + time3 <= time < time1 + time2 + time3 + time4:
            v.append(vmax)
        elif time1 + time2 + time3 + time4 <= time < time1 + time2 + time3 + time4 + time5:
            time -= time1 + time2 + time3 + time4
            v.append(vmax - 0.5 * jerk3 * time**2)
        elif time1 + time2 + time3 + time4 + time5 <= time < time1 + time2 + time3 + time4 + time5 + time6:
            v.append(m2 * time + c2)
        elif time1 + time2 + time3 + time4 + time5 + time6 <= time < time1 + time2 + time3 + time4 + time5 + time6 + time7:
            time -= time1 + time2 + time3 + time4 + time5 + time6
            v.append(vel7 + 0.5 * jerk4 * time**2 - accel * time)

    return t, v

def lineEq(l1, l2):
    m = (l2[1] - l1[1]) / (l2[0] - l1[0])
    c = (l2[1] - (m * l2[0]))
    return m, c


if __name__ == "__main__":
    graph()
    
