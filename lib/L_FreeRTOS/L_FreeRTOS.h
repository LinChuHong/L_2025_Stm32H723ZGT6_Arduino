#pragma once
#include <Arduino.h>
#include <STM32FreeRTOS.h>
namespace L_FreeRTOS
{
    namespace TaskManager
    {
        void myTask1(void * pvParameters);
        void myTask2(void * pvParameters);
        void myTask3(void * pvParameters);
        void myTask4(void * pvParameters);
        void myTask5(void * pvParameters);
        void myTask6(void * pvParameters);
        
    }

    namespace SetUp
    {
        void setup();
        extern std::vector<int> ledPins;
        typedef enum
        {
            RED1,
            GREEN1,
            BLUE1
        } RGB1;
    }
    

}