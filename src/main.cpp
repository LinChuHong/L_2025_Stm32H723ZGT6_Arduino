#include <Arduino.h>
#include <OneButton.h>
#include <rng.h>
#include <sys.h>
#include <mpu.h>
#include <norflash.h>
#include <delay.h>
#include <led.h>
#include <sdram.h>
#include <enable.h>
#include <lcd.h>
#include <key.h>
#include <touch.h>
#include <L_malloc1.h>
#include <custom.h>
#include <lvgl.h>
#include <lv_port_disp.h>
#include <lv_port_indev.h>
#include <L_FreeRTOS.h>
#include <map>
#include <string>
#include <hello.h>
#include <sdmmc_sdcard.h>
#include <lvgl_demo.h>
#include <ui.h>

std::map<std::string, OneButton> myButton1;
HardwareTimer mytimer(TIM6);

#define test 0


void setup() 
{
    #if test == 1
    Serial.begin(1500000);
    pinMode(LED_BUILTIN,OUTPUT);
    norflash_init();
    #endif
    #if test == 0
    Serial.begin(115200);
    sys_cache_enable();                     /* 使能L1-Cache */
    delay_init(520);                        /* 延时初始化 */
    led_init();                             /* 初始化LED */
    mpu_memory_protection();                /* 保护相关存储区域 */
    sdram_init();                           /* 初始化SDRAM */
    lcd_init();                             /* 初始化LCD */
    
    my_mem_init(SRAMIN);                    /* 初始化内部内存池(AXI) */
    my_mem_init(SRAMEX);                    /* 初始化外部内存池(SDRAM) */
    my_mem_init(SRAMDTCM);                  /* 初始化DTCM内存池(DTCM) */
    my_mem_init(SRAMITCM);                  /* 初始化ITCM内存池(ITCM) */
    
	lv_init();                              /* lvgl系统初始化 */
    lv_port_disp_init();                    /* lvgl显示接口初始化,放在lv_init()的后面 */
    lv_port_indev_init();                   /* lvgl输入接口初始化,放在lv_init()的后面 */
    custom_init();

    mytimer.setOverflow(1000,MICROSEC_FORMAT);
    mytimer.attachInterrupt( [] { lv_tick_inc(1); myButton1.at("button1").tick(); } );
    mytimer.resume();
    
    myButton1.insert( { "button1", OneButton() } );
	myButton1.at("button1").setup(PC1,INPUT_PULLDOWN,false);
    myButton1.at("button1").attachPress( [] {  } );
    L_FreeRTOS::SetUp::setup();
    #endif
}
#define CHUNK_SIZE 4096  // 4 KB per write
uint8_t buffer[CHUNK_SIZE];

void loop() 
{
    #if test == 1
    if (Serial.available() >= 6) { // address(4) + size(2)
        uint32_t address = 0;
        uint16_t size = 0;

        Serial.readBytes((char*)&address, 4);
        Serial.readBytes((char*)&size, 2);

        if (size > CHUNK_SIZE) size = CHUNK_SIZE; // safety

        // receive chunk
        Serial.readBytes((char*)buffer, size);

        // erase sector first
   
        // write chunk
        norflash_write(buffer, address, size);
        // send ACK
        Serial.write(0xAA);
    }

    #endif
}
void SystemClock_Config(void) { sys_stm32_clock_init(104,5,1,2); }

