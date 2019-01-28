# Project Plans

# Goals:
- Act as a dedicated high performance MCU(external board) for motion control on the XY axis
- Reduce the load on the main mcu, which is most likely an 8 bit board
- True closed loop: No more skipped steps
- Typical 5 stepper boards have the capability of running a 4 tool toolchanger setup
- Compatability with most existing boards by using SPI channel and one pin for chip select
- LiPo to provide higher peak current
- Accurate and precise sensorless homing
- Quieter: Stealthchop can be used without fear of skipped steps
- Less expensive than competition
# TMC4361:
- Internal ramp generator, Scurve at 1/256th microstepping, closed loop correction
# TMC2160:
- Connected via step/dir to 4361
- Mosfets capable of running 3a motors
- Driver is configured through the firmware(SPI)
- Possibly available by itself/separate of 4361?
# Encoder options
- AS5311, AMT112, A5047D
# Software goals:
- SPI motion control, DAA, and S-curve acceleration in Klipper and Marlin

# Future Plans
- TMC4671 using stepstick format and mosfets on external board. Internal ramp generator would be preferred
- Custom motion controller
- TI motion controllers
- Cheap controller board with properly cooled tmc2208 or tmc5072
- High end controller board with AM437x or AM335x, motion controllers for x and y, high power 2160s on all axis
- EtherCAT / CAN
