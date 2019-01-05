import logging
import bus, chelper

#REGW = Writing Register
#REGR = Reading Register
Registers = {
    "REGW_RESET": 0xCF, 
    "REGW_FILTER_START": 0x83,
    "REGW_FILTER_ENCODER": 0x84,
    "REGW_RAMPMODE": 0xA0,
    "REGW_XTARGET": 0xB7,
    "REGR_XTARGET": 0x37,
    "REGW_VSTART": 0xA5
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
        self._config = config
        self.printer = config.get_printer()
        self.spi = bus.MCU_SPI_from_config(config, 3, default_speed=4000000)
        self.bow1 = config.getint("bow1", 90000)
        self.bow2 = config.getint("bow2", 90000)
        self.bow3 = config.getint("bow3", 90000)
        self.bow4 = config.getint("bow4", 90000)
        self.enc_res = config.getint("encoder_resolution", 4096)
        self.enc_type = config.get("encoder_type", "abi")
        self.check_tmc()
        self.check_reasonable()
        self.set_register("REGW_RESET", 0x52535400)
        self.set_register("REGW_FILTER_START", 0x00540022)
        self.set_register("REGW_FILTER_ENCODER", 0x8440000D)
        self.set_register("REGW_RAMPMODE", 0x00000006)
        self.set_register("REGW_MS", 0x00000000)
        self.set_register("REGW_BOW1", self.bow1)
        self.set_register("REGW_BOW2", self.bow2)
        self.set_register("REGW_BOW3", self.bow3)
        self.set_register("REGW_BOW4", self.bow4)	

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
	
    def check_tmc(self):
        #Ensure that x and y axis have 1/256 microstepping
        steps = {'256': 0, '128': 1, '64': 2, '32': 3, '16': 4,
                '8': 5, '4': 6, '2': 7, '1': 8}
        if self._config.has_section("tmc2130 stepper_x"):
            self.tmc_x = self._config.getsectio("tmc2130 stepper_x")
        elif self._config.has_section("tmc2208 stepper_x"):
            self.tmc_x = self._config.getsection("tmc2208 stepper_x")
        elif config.has_section("tmc2660 stepper_x"):
            self.tmc_x = self._config.getsection("tmc2660 stepper_x")
        else:
            raise self._config.error("Drivers must be TMC for use of TMC4361")
        if self._config.has_section("tmc2130 stepper_y"):
            self.tmc_x = self._config.getsection("tmc2130 stepper_y")
        elif self._config.has_section("tmc2208 stepper_y"):
            self.tmc_x = self._config.getsection("tmc2208 stepper_y")n
        elif self._config.has_section("tmc2660 stepper_y"):
            self.tmc_x = self._config.getsection("tmc2660 stepper_y")
        else:
            raise self._config.error("Drivers must be TMC for use of TMC4361")
        self.tmc_y = None
        if self.tmc_x.getchoice("microsteps", steps) != 0: #or self.tmc_y.getchoice("microsteps", steps) != 0:
            raise self._config.error("Driver microstepping must be set to 256 for use of TMC4361")
	
    def check_reasonable(self):
        pass
    def dist_to_time(self):

	def kinematics(self):


class MCU_4361_Stepper:


def load_config(config):
	return TMC4361(config)