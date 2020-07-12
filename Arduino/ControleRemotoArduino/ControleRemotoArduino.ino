/*
 * IRremote: IRrecvDemo - demonstrates receiving IR codes with IRrecv
 * An IR detector/demodulator must be connected to the input RECV_PIN.
 * Version 0.1 July, 2009
 * Copyright 2009 Ken Shirriff
 * http://arcfn.com
 */

#include <IRremote.h>

//Sensor TOP 4838
// Pin1 = signal; Pin2 = GND; Pin3= VCC
int RECV_PIN = 11;
//int RECV_GND_PIN = 12;
//int RECV_VCC_PIN = 13;
int RECV_GND_PIN = 10;
int RECV_VCC_PIN = 9;



IRrecv irrecv(RECV_PIN);

decode_results results;

void setup()
{
  digitalWrite(RECV_GND_PIN, LOW);
  digitalWrite(RECV_VCC_PIN, HIGH);

  pinMode(RECV_GND_PIN, OUTPUT);
  pinMode(RECV_VCC_PIN, OUTPUT);
  
  Serial.begin(9600);
  irrecv.enableIRIn(); // Start the receiver
}

void loop() {
  if (irrecv.decode(&results)) {
    Serial.println(results.value, HEX);
    irrecv.resume(); // Receive the next value
  }
}
