#include "L_Signal.h"
namespace L_FreeRTOS
{
    namespace Signal
    {
        QueueHandle_t myQueue1;
        QueueHandle_t myQueue2;
        SemaphoreHandle_t mySemaphore1;
        SemaphoreHandle_t mySemaphoreBinary1;
        EventGroupHandle_t myEvent1;
        TimerHandle_t myTimer1;
    }
}