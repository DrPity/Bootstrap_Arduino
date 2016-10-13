// Use DEBUG_PRINT for easy turning on of debug messages

#ifndef DEBUG_H
#define DEBUG_H

#include <Arduino.h>

#ifdef DEBUG
#define DEBUG_PRINT(x) Serial.print(x); Serial.print("\t")
#define DEBUG_PRINTLN(x) Serial.println(x)
#else
#define DEBUG_PRINT(x)
#define DEBUG_PRINTLN(x)
#endif



#endif
