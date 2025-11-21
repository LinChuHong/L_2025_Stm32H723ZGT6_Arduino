#include "L_FreeRTOS.h"
#include "L_Signal.h"
#include "L_Serial.h"
#include <algorithm>
#include <SPI.h>
#include <sdmmc_sdcard.h>
#include <lvgl.h>
#include <lv_mainstart1.h>
#include <USBSerial.h>

#include <map>
#include <string>
#include <OneButton.h>

namespace L_FreeRTOS
{
    namespace TaskManager
    {
        void myTask1(void * pvParameter)
        {
         
            for(;;)
            {    
                lv_timer_handler();
                vTaskDelay(pdMS_TO_TICKS(5));
            }

        }
        void myTask2(void * pvParameter)
        {
            char buf[64];
            // SerialUSB.begin();
            for(;;)
            {   
                if (xQueueReceive(Signal::myQueue2,buf,portMAX_DELAY) == pdPASS)
                {       
                    if (strcmp(buf,"test") == 0)
                    {
                        // SerialUSB.println("hello, world");
                    }
                    

                 
                }
                vTaskDelay(pdMS_TO_TICKS(5));
            }

        }
        void myTask3(void * pvParameter)
        {
            // UBaseType_t highWater = uxTaskGetStackHighWaterMark(NULL);
            // Serial.printf("Free stack words left: %u\n", highWater);
            for(;;)
            {   
                // if (xSemaphoreTake(Signal::mySemaphore1,portMAX_DELAY) == pdTRUE)
                // {
                //     Serial.println("myTask->3");
                //     xSemaphoreGive(Signal::mySemaphore1);
                // }
                // if(L_Serial::mySerial2.available())
                // {
                //     String st = L_Serial::mySerial2.readStringUntil('\n');
                // }
                vTaskDelay(pdMS_TO_TICKS(5));
            }

        }
        void myTask4(void * pvParameter)
        {
     
            for(;;)
            {   
                // if (xSemaphoreTake(Signal::mySemaphore1,portMAX_DELAY) == pdTRUE)
                // {
                //     Serial.println("myTask->4");
                //     xSemaphoreGive(Signal::mySemaphore1);
                // }
                // if(L_Serial::mySerial2.available())
                // {
                //     String st = L_Serial::mySerial2.readStringUntil('\n');
                // }
                vTaskDelay(pdMS_TO_TICKS(5));
            }

        }
        void myTask5(void * pvParameter)
        {

            char buf[64];
            std::vector<std::string> vst;
            for(;;)
            {   
                if (xQueueReceive(Signal::myQueue1,buf,portMAX_DELAY) == pdPASS)
                { 
                    vst.push_back(buf);
                    if (strcmp(buf,"Osaka") == 0)
                        Serial.println("hello, Osaka");
                    else if (strcmp(buf,"Chiyo") == 0)
                        Serial.println("hello, Chiyo");
                    for (const auto i : vst)
                    {
                        Serial.println(i.c_str());
                    }
                    bool i1 = std::find(vst.begin(),vst.end(),"Osaka") != vst.end();
                    bool i2 = std::find(vst.begin(),vst.end(),"Chiyo") != vst.end();
                    if (i1 and i2 == true)
                    {
                        Serial.println("hello, Osaka and Chiyo");
                        vst.clear();
                    }
                }

                vTaskDelay(pdMS_TO_TICKS(5));
            }

        }
        void myTask6(void * pvParameter)
        {

            bool connectToComputer = false;
            for(;;)
            {   
                if (Serial.available())
                {
                    String st = Serial.readStringUntil('\n');
                    if (st == "lin")
                        xQueueSend(Signal::myQueue1,"Osaka",portMAX_DELAY);
                    else if (st == "chu")
                        xQueueSend(Signal::myQueue1,"Chiyo",portMAX_DELAY);
                    else if (st == "hong")
                        xQueueSend(Signal::myQueue1,"Kawaii",portMAX_DELAY);
                    else if (st == "test w")
                        xQueueSend(Signal::myQueue2,"test w",portMAX_DELAY);
                    else if (st == "test r")
                        xQueueSend(Signal::myQueue2,"test r",portMAX_DELAY);
                    else if (st == "unmount")
                        xQueueSend(Signal::myQueue2,"unmount",portMAX_DELAY);
                    else if (st == "test")
                        xQueueSend(Signal::myQueue2,"test",portMAX_DELAY);
                    else if (st == "hello there 9527")
                    {
                        Serial.println("connected to computer->");
                        connectToComputer = true;
                    }
                    else if (st == "insertsd")
                    {
                        xSemaphoreGive(Signal::mySemaphoreBinary1);
                    }
                }
                if (L_Serial::mySerial2.available())
                {
                    

                }
                
                // if (connectToComputer == false)
                // {
                //     Serial.println("id:9527");
                //     vTaskDelay(pdMS_TO_TICKS(100));
                // }
                vTaskDelay(pdMS_TO_TICKS(5));
            }

        }

    }
    namespace SetUp
    {

        
        void buttonTickCallback(xTimerHandle t)
        {
            
        }
        void setup()
        {
            
            // Task
            xTaskCreate(TaskManager::myTask1,"myTask1",2000,NULL,1,NULL);
            xTaskCreate(TaskManager::myTask2,"myTask2",2000,NULL,2,NULL);
            xTaskCreate(TaskManager::myTask3,"myTask3",2000,NULL,1,NULL);
            xTaskCreate(TaskManager::myTask4,"myTask4",2000,NULL,1,NULL);
            xTaskCreate(TaskManager::myTask5,"myTask5",2000,NULL,1,NULL);
            xTaskCreate(TaskManager::myTask6,"myTask6",2000,NULL,1,NULL);

            // semaphore
            Signal::mySemaphore1 = xSemaphoreCreateMutex();
            Signal::mySemaphoreBinary1 = xSemaphoreCreateBinary();
            Signal::myQueue1 = xQueueCreate(10,sizeof(char[64]));
            Signal::myQueue2 = xQueueCreate(10,sizeof(char[64]));
        
            
            // Timer
            Signal::myTimer1 = xTimerCreate("T1",pdMS_TO_TICKS(10),pdTRUE,NULL,buttonTickCallback);
            if (Signal::myTimer1 != NULL) xTimerStart(Signal::myTimer1,0); else Serial.println("Timer1 does not exit");

            // Serial
            Serial.begin(SERIALBAUDRATE);
            // L_Serial::mySerial2.begin(4000000);

            // SD Card
            // L_SDCARD::myFile = SD.open("L_linchuhong.txt",FA_WRITE);

            // Led
    
            
            // Button






            Serial.println("Init Done");
            vTaskStartScheduler();

        }
    
    
    }
}