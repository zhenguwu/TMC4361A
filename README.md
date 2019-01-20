# TMC4361A
Taking advantage of closed loop control and s-ramping in the TMC4361A for 3D printing

# Goals:
- Act as a dedicated MCU for motion control on the XY axis, through the multiple mcu feature on klipper
- Reduce the load on the main, most likely 8 bit board
- True closed loop
- Typical 5 stepper boards have the capability of running a 4 tool toolchanger setup
- Less expensive than competition
# TMC4361:
- Internal ramp generator - S-curve at 1/256th microstepping
# TMC4671:
- FOC stepper control - Internal ramp generator?
# Encoder
- AS5311
# Software goals:
- SPI motion control, DAA, and S-curve acceleration in Klipper
