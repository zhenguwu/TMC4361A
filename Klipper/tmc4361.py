import logging
import bus

#REGW = Writing Register
#REGR = Reading Register
Registers = {
    "REGW_RESET": 0xCF, 
    "REGW_FILTER_START": 0x83,
    "REGW_FILTER_ENCODER": 0x84,
    "REGW_RAMPMODE": 0xA0,
    "REGW_XTARGET": 0xB7,
    "REGR_XTARGET": 0x37,
    "REGW_VSTART": 0xA5,
    "REGW_VMAX": 0xA4,
    "REGW_VSTOP": 0xA6,
    "REGW_AMAX": 0xA8,
    "REGW_DMAX": 0xA9,
    "REGW_BOW1": 0xAD,
    "REGW_BOW2": 0xAE,
    "REGW_BOW3": 0xAF,
    "REGW_BOW4": 0xB0,
    "REGW_MS": 0x8A,
}

class TMC4361:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.spi = bus.MCU_SPI_from_config(config, 3, default_speed=4000000)
        self.bow_1 = config.getint("max_bow_1", 90000)
        self.bow_2 = config.getint("max_bow_2", 90000)
        self.bow_3 = config.getint("max_bow_3", 90000)
        self.bow_4 = config.getint("max_bow_4", 90000)
        self.enc_res = config.getint("encoder_resolution", 4096)
        self.enc_type = config.get("encoder_type", "abi")
        
        steps = {'256': 0, '128': 1, '64': 2, '32': 3, '16': 4,
                '8': 5, '4': 6, '2': 7, '1': 8}
        if config.has_section("tmc2130 stepper_x"):
            self.tmc_x = config.getsection("tmc2130 stepper_x")
        elif self.config.has_section("tmc2208 stepper_x"):
            self.tmc_x = config.getsection("tmc2208 stepper_x")
        elif config.has_section("tmc2660 stepper_x"):
            self.tmc_x = config.getsection("tmc2660 stepper_x")
        else:
            raise config.error("Drivers must be TMC for use of TMC4361")
        if config.has_section("tmc2130 stepper_y"):
            self.tmc_y = config.getsection("tmc2130 stepper_y")
        elif config.has_section("tmc2208 stepper_y"):
            self.tmc_y = config.getsection("tmc2208 stepper_y")
        elif config.has_section("tmc2660 stepper_y"):
            self.tmc_y = config.getsection("tmc2660 stepper_y")
        else:
            raise config.error("Drivers must be TMC for use of TMC4361")
        self.tmc_y = None
        #Ensure that x and y axis have 1/256 microstepping
        if self.tmc_x.getchoice("microsteps", steps) != 0: #or self.tmc_y.getchoice("microsteps", steps) != 0:
            raise self._config.error("Driver microstepping must be set to 256 for use of TMC4361")
        
        self.set_register("REGW_RESET", 0x52535400)
        self.set_register("REGW_FILTER_START", 0x00540022)
        self.set_register("REGW_FILTER_ENCODER", 0x8440000D)
        self.set_register("REGW_RAMPMODE", 0x00000006)
        self.set_register("REGW_MS", 0x00000000)
        self.set_register("REGW_BOW1", self.bow_1)
        self.set_register("REGW_BOW2", self.bow_2)
        self.set_register("REGW_BOW3", self.bow_3)
        self.set_register("REGW_BOW4", self.bow_4)  
    def set_register(self, reg_name, val):
        reg = Registers[reg_name]
        datagram = [reg & 0xff, (val >> 24) & 0xff, (val >> 16) & 0xff,
                    (val >> 8) & 0xff, val & 0xff]
        self.spi.spi_send(datagram)
    def get_register(self, reg_name):
        reg = Registers[reg_name]
        self.spi.spi_send([reg, 0x00, 0x00, 0x00, 0x00])
        params = self.spi.spi_transfer([reg, 0x00, 0x00, 0x00, 0x00])
        pr = bytearray(params['response'])
        return (pr[1] << 24) | (pr[2] << 16) | (pr[3] << 8) | pr[4]
    def get_jerk(self):
        return [self.bow_1, self.bow_2, self.bow_3, self.bow_4]
    def validate(self, accel):
        #Ensure that defined jerk, accel, and vel are reasonable
        #Needs testing?
        pass
    def generate_ramp(self, start_v, cruise_v, end_v, accel, move_d):
        #Calculates an S curve ramp
        jerk_1, jerk_2, jerk_3, jerk_4 = self.get_jerk()
        time = [0, 0, 0, accel/jerk_2, 0, accel/jerk_3, 0, 0]
        vel_1 = 0
        vel_3 = cruise_v + 0.5 * jerk_2 * time[3]**2 - accel * time[3]
        vel_5 = cruise_v - 0.5 * jerk_3 * time[5]**2
        vel_7 = 0
        d = [0, 0, 0, vel_3 * time[3] + 0.5 * accel * time[3]**2 - (1/6) * jerk_2 * time[3]**3, 0, cruise_v * time[5] - (1/6) * jerk_3 * time[5]**3, 0, 0]
        if start_v == 0:
            time[1] = accel/jerk_1
            vel_1 = 0.5 * jerk_1 * time[1]**2
            d[1] = (1/6) * jerk_1 * time[1]**3
        else:
            #time1 = 0
            vel_1 = start_v
            #d1 = 0
        time[2] = (vel_3  - vel_1) / accel
        d[2] = vel_1 * time[2] + 0.5 * accel * time[2]**2
        if end_v == 0:
            time[7] = accel/jerk_4
            vel_7 = accel * time[7] - 0.5 * jerk_4 * time[7]**2
            d[7] = vel_7 * time[7] - 0.5 * accel * time[7]**2 + (1/6) * jerk_4 * time[7]**3
        else:
            #time7 = 0 
            vel_7 = end_v
            #d7 = 0
        time[6] = (vel_5 - vel_7) / accel
        d[6] = vel_5 * time[6] - 0.5 * accel * time[6]**2
        d[4] = move_d - d[1] - d[2] - d[3] - d[5] - d[6] - d[7]
        time[4] = d[4] / cruise_v
        return time, d
    def set_junction(self, start_v, cruise_v, end_v, accel, move_d)
        time, d = self.generate_ramp(start_v, cruise_v, end_v, accel, move_d)
        return time[1] + time[2] + time[3], time[4], time[5] + time[6] + time[7]
def load_config(config):
    return TMC4361(config)