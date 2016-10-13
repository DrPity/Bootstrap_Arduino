//Some common helper functions
#include <Arduino.h>

void setHigh(int pin){
  digitalWrite(pin, HIGH);
}

void setLow(int pin){
  digitalWrite(pin, LOW);
}

void sendPulse(int pin){
	digitalWrite(pin, HIGH);
	digitalWrite(pin, LOW);
}

void sendNegativePulse(int pin){
	digitalWrite(pin, LOW);
	digitalWrite(pin, HIGH);
}
