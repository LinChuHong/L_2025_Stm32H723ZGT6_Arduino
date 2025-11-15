#pragma once
#include "L_FreeRTOS.h"



namespace L_FreeRTOS
{
    namespace Signal
    {
        extern QueueHandle_t myQueue1;
        extern SemaphoreHandle_t mySemaphore1;
        extern SemaphoreHandle_t mySemaphoreBinary1;
        extern EventGroupHandle_t myEvent1;
        extern TimerHandle_t myTimer1;

    }
}