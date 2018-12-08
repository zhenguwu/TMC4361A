#include <SPI.h>
#include <TMC2208Stepper.h>

// Configuration Options - Temporary
const int microstepping = 256;     // 1/256th required for closed loop
bool spreadcycle = false;          // Enable/Disable spreadcycle
const int stepsmm = 1600;              // Steps per mm of axis

// 0: VelNR, 1: VelTR, 2: VelSR, 4: PosNR, 5: PosTR, 6: PosSR 
const int rampmode = 0x00000006;  // Only PosSR supported
// VMAX, AMAX, and Bow values are automatically converted from mm/s mm/s2 mm/s3 to pps pps2 pps3
const long long VMAX = 200L * stepsmm;       // Velocity
const long long AMAX = 3000L * stepsmm;      // Acceleration
const long long DMAX = 3000L * stepsmm;      // Decceleration
const long long BOW1 = 120000L * stepsmm;    // Jerk
const long long BOW2 = 120000L * stepsmm;
const long long BOW3 = 120000L * stepsmm;
const long long BOW4 = 120000L * stepsmm;

// Some pins
const int cs1 = 8;        
const byte CLOCKOUT = 9;
const int motorEnable = 7;

// Testing
long target = 100L * stepsmm;
int MS = 0x00000000;
bool interpolation = false;


TMC2208Stepper driver = TMC2208Stepper(&Serial1); 

void setup() {
  // Set pinmodes
  pinMode(cs1, OUTPUT);
  pinMode(CLOCKOUT, OUTPUT);
  pinMode(motorEnable, OUTPUT);
  
  switch(microstepping) {
  case 256:
    MS = 0x00000000;
    interpolation = false;
  case 16:
    MS = 0x00000004;
    interpolation = false;
  }
  
  Serial.begin(9600);
  // Setup TMC2208, Serial1 on pins 19(RX) 18(TX)
  Serial1.begin(115200);              // Start hardware Serial1
  digitalWrite(motorEnable, HIGH);          // Hardware disable TMC2208
  driver.push();                      // Reset registers
  driver.pdn_disable(true);           // Use PDN/UART pin for communication
  driver.I_scale_analog(false);       // Use internal voltage reference
  driver.rms_current(500);            // Set driver current in mA
  driver.microsteps(microstepping);   // Set microstepping
  driver.intpol(interpolation);               // Disable interpolation
  driver.en_spreadCycle(spreadcycle); // Set spreadcycle mode
  driver.toff(2);                     // Enable driver in software

  // Setup TMC4361
  digitalWrite(cs1, HIGH);
  //Timer1
  pinMode(11, OUTPUT);
  TCCR1A = bit (COM1A0);
  TCCR1B = bit (WGM12) | bit (CS10);
  OCR1A = 0;
  //Setup SPI with 4361
  SPI.setBitOrder(MSBFIRST);
  SPI.setClockDivider(SPI_CLOCK_DIV8);
  SPI.setDataMode(SPI_MODE3);
  SPI.begin();
  // Send configuration to registers
  // Add 80 to register address for write access
  sendData(0xCF, 0x52535400); // Software Reset IC
  sendData(0x83, 0x00540022); // Add input filter on START and Encoder pins
  sendData(0x84, 0x8440000d); 
  sendData(0xA0, rampmode);   // Set ramp mode
  sendData(0xA4, VMAX);       // Set VMAX
  sendData(0xA9, DMAX);       // Set DMAX
  sendData(0xA8, AMAX);       // Set AMAX     
  sendData(0xAD, BOW1);       // Set BOW1-4 values
  sendData(0xAE, BOW2);
  sendData(0xAF, BOW3);
  sendData(0xB0, BOW4);
  sendData(0x8A, MS);         // Set microstepping
  

  digitalWrite(motorEnable, LOW);
  uint32_t data = 0;
  Serial.print("DRV_STATUS = 0x");
  driver.DRV_STATUS(&data);
  Serial.println(data, HEX);
  
}

void loop() {
 sendData(0xB7, target); // XTARGET = target
 sendData(0x37, 0);      // Read XTARGET register
 delay(3000);
 sendData(0xB7,0x00000000); // XTARGET = 0
 sendData(0x37, 0);         // Read XTARGET register
 delay(3000);
}

void sendData(unsigned long address, unsigned long datagram)
{
 // TMC4361 takes 40 bit data: 8 address and 32 data
 unsigned long i_datagram;
 
 digitalWrite(cs1, LOW); // Pull CS Low
 delayMicroseconds(10);
 
 SPI.transfer(address);
 // Break up data into four 8 bit numbers, and send through SPI
 // i_datagram |= only needed for echo
 i_datagram |= SPI.transfer((datagram >> 24) & 0xff);
 i_datagram <<= 8;
 i_datagram |= SPI.transfer((datagram >> 16) & 0xff);
 i_datagram <<= 8;
 i_datagram |= SPI.transfer((datagram >> 8) & 0xff);
 i_datagram <<= 8;
 i_datagram |= SPI.transfer((datagram) & 0xff);
 digitalWrite(cs1,HIGH);
 
 Serial.print("Received: ");
 Serial.println(i_datagram,HEX);
 Serial.print(" from register: ");
 Serial.println(address,HEX);
}
