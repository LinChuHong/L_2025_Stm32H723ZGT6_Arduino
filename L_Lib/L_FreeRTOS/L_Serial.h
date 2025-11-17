#pragma once
#include "L_FreeRTOS.h"

#define SERIALBAUDRATE 115200
namespace L_FreeRTOS
{
    namespace L_Serial
    {
        #define Serial2_RX PA3
        #define Serial2_TX PA2
        
        extern HardwareSerial mySerial2;
    }
}