#include <OneWire.h>
#include <Wire.h>
#include <Adafruit_MMA8451.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_APDS9960.h"

const int leftButton = 10;
const int homeButton = A2;
const int rightButton = 9;
const int slider = A0;
const int temperature = A1;

OneWire  ds(temperature);
Adafruit_MMA8451 mma = Adafruit_MMA8451();

Adafruit_APDS9960 apds;

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
  
  pinMode(leftButton, INPUT_PULLUP);
  pinMode(homeButton, INPUT_PULLUP);
  pinMode(rightButton, INPUT_PULLUP);
  
  mma.begin();
  mma.setRange(MMA8451_RANGE_2_G);
  
  apds.begin();
  apds.enableProximity(true);
  //apds.enableGesture(true);
}

void loop() {
  if (Serial.available()) {
    String response = "";
    byte s = Serial.read();

    //left button
    int sensorVal = digitalRead(leftButton);
    if (sensorVal == LOW) {
      response += "1:";
    }
    else {
      response += "0:";
    }

    //home button
    sensorVal = digitalRead(homeButton);
    if (sensorVal == LOW) {
      response += "1:";
    }
    else {
      response += "0:";
    }

    //right button
    sensorVal = digitalRead(rightButton);
    if (sensorVal == LOW) {
      response += "1:";
    }
    else {
      response += "0:";
    }

    //slider with zero padding
    sensorVal = analogRead(slider);
    if (sensorVal < 1000) {
      response += "0";
    }
    if (sensorVal < 100) {
      response += "0";
    }
    if (sensorVal < 10) {
      response += "0";
    }
    response += String(sensorVal);
    response += ":";

    //temperature
    
    byte i;
    byte present = 0;
    byte type_s;
    byte data[12];
    byte addr[8];
    float celsius;
    
    if ( !ds.search(addr)) {
      ds.reset_search();
    }
    ds.reset();
    ds.select(addr);
    ds.write(0x44, 1);
    
    
    present = ds.reset();
    ds.select(addr);    
    ds.write(0xBE);
  
    for ( i = 0; i < 9; i++) {
      data[i] = ds.read();
    }
  
    int16_t raw = (data[1] << 8) | data[0];
    if (type_s) {
      raw = raw << 3;
      if (data[7] == 0x10) {
        raw = (raw & 0xFFF0) + 12 - data[6];
      }
    } else {
      byte cfg = (data[4] & 0x60);
      if (cfg == 0x00) raw = raw & ~7;
      else if (cfg == 0x20) raw = raw & ~3;
      else if (cfg == 0x40) raw = raw & ~1;
    }
    
    celsius = (float)raw / 16.0;
    response += String(celsius);
    response += ":";

    //accelerometer
    mma.read();
    response += String(mma.x);
    response += ":";
    response += String(mma.y);
    response += ":";
    response += String(mma.z);
    response += ":";

    sensors_event_t event; 
    mma.getEvent(&event);

    response += String(event.acceleration.x);
    response += ":";
    response += String(event.acceleration.y);
    response += ":";
    response += String(event.acceleration.z);
    response += ":";
    /*Serial.println("starting gesture");
    uint8_t gesture = apds.readGesture();
    Serial.println("done gesture");
    if(gesture == APDS9960_DOWN) {
      response += "v";
    }
    else if(gesture == APDS9960_UP) {
      response += "^";
    }
    else if(gesture == APDS9960_LEFT) {
      response += "<";
    }
    else if(gesture == APDS9960_RIGHT) {
      response += ">";
    }
    else {
      response += "0";
    }
    response += ":";
*/
    uint8_t proximity = apds.readProximity();

    if (proximity < 100) {
      response += "0";
    }
    if (proximity < 10) {
      response += "0";
    }
    response += String(proximity);
    response += ":";
    

    Serial.print(response);
  }
}


