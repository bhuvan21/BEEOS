# BEEOS

## Overview
This is the GUI system that will run on BEE v2.
"BEE" is essentially a modern day smartphone I created . . . if modern day meant 2007.
It aims to function as a portable entertainment device with e-reader and music playing capabilities.
This is the second iteration of BEE.

| BEE v1.0 | BEE v2.0 | BEE v2.0 CAD |
|----------|----------|--------------|
|![alt text](https://i.imgur.com/oTUWWay.jpg "BEE v1.0")|![alt text](https://i.imgur.com/mHhpkSA.jpg "BEE v2.0")|![alt text](https://i.imgur.com/nFKj3L9.png "BEE v2.0 CAD")|

## Features
It has a fully fledged app system, and there is even an app store!
Currently Implemented:  
- Lock Screen  
- PIN Unlock  
- Existance of Home Screen  
- App system  
- App store  
- Settings app - Bluetooth + Wifi, Change Wallpapers
- Volume, Lock + Screen Dimming
- File Transfer System
- Music app
- EPUB Reading app  
- Weather/Temperature App

Future Ideas:  
- Project Gutenberg Ebook Getter
- Calculator
- Email
- Tic Tac Toe
- Clock, Timer, Stopwatch
- File Browser?
- Broswer?
- Dice Rolling?
- Reddit?

## Physical Build
B.E.E contains the following parts:
- Raspberry Pi Zero
- Powerboost 1000
- 2000mAh Lipo Battery
- Arduino Beetle
- USB B cable
- I2C Accelerometer
- Thermistor
- Buttons
- Linear Potentiometer
- Light/Color/IR Sensor
- Hyperpixel 4.0 HAT

The electronic connections are described in the following section.
The plastic chasis for the build was 3D printed in grey PLA in two parts. The two parts fit together and lock this way due to their snap fit design.

## Signal Flow
All sensors were connected to the arduino beetle. The arduino beetle was powered from the powerboost 1000 board, and connected by a USB B on the go cable to the Raspberry Pi Zero. The sensor information was sent by serial across this connection. The RPI Zero was also powered by the powerboost 1000 which in turn was connected to the 2000mAh Lipo battery.

## Future Improvements
- Rewrite GUI not using kivy, due to the strain it puts on the RPI Zero
- Place temperature sensor further from the powerboost board as this affects temperature readings
