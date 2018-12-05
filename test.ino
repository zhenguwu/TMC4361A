#include <SPI.h>
#include <TMC2208Stepper.h>

// Configuration Options - Temporary
const int microstepping = 256;    // 1/256th required for closed loop
bool spreadcycle = true;          // Enable/Disable spreadcycle
const int stepsmm = 1280L;               // Steps per mm of axis
// 0: VelNR, 1: VelTR, 2: VelSR, 4: PosNR, 5: PosTR, 6: PosSR 
const int rampmode = 6;  // Only PosSR supported
// VMAX, AMAX, and Bow values are automatically converted from mm/s mm/s2 mm/s3 to pps pps2 pps3
const long VMAX = 80L * stepsmm;
const long AMAX = 3000L * stepsmm;
const long DMAX = 3000L * stepsmm;
const long bow1 = 120000L * stepsmm;
const long bow2 = 120000L * stepsmm;
const long bow3 = 120000L * stepsmm;
const long bow4 = 120000L * stepsmm;

// Some pins
const int cs1 = 8;        
const byte CLOCKOUT = 9;
const int enable = 7;

TMC2208Stepper driver = TMC2208Stepper(&Serial1); 

void setup() {
  Serial.begin(9600);
  // Setup TMC2208, Serial1 on pins 19(RX) 18(TX)
  Serial1.begin(115200);              // Start hardware Serial1
  driver.push();                      // Reset registers
  driver.pdn_disable(true);           // Use PDN/UART pin for communication
  driver.I_scale_analog(false);       // Use internal voltage reference
  driver.rms_current(500);            // Set driver current 500mA
  driver.microsteps(microstepping);   // Set microstepping
  driver.intpol(false);               // Disable interpolation
  driver.en_spreadCycle(spreadcycle); // Set spreadcycle mode
  driver.toff(2);                     // Enable driver in software

  // Setup TMC4361
  pinMode(cs1, OUTPUT);
  pinMode(CLOCKOUT, OUTPUT);
  pinMode(enable, OUTPUT);
  digitalWrite(cs1, HIGH);
  digitalWrite(enable, LOW);
  //Timer1
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
  sendData(0xA0, rampmode); // Set ramp mode
  sendData(0xA4, VMAX);
  sendData(0xA8, AMAX);
  sendData(0xA9, DMAX);
  sendData(0xAD, bow1); // Bow Values
  sendData(0xAE, bow2);
  sendData(0xAF, bow3);
  sendData(0xB0, bow4);
  
  
  
  
  
}

void loop() {
 sendData(0xB7,0x00019000); // XTARGET = 100.000
 delay(3000);
 sendData(0xB7,0x00000000); // XTARGET = 0
 delay(3000);
}

void sendData(unsigned long address, unsigned long datagram)
{
 //TMC4361 takes 40 bit data: 8 address and 32 data
 //delay(100) ?????
 unsigned long i_datagram;
 
 digitalWrite(cs1, LOW);
 delayMicroseconds(10);
 
 SPI.transfer(address);
 
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
