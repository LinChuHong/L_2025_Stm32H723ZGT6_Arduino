#include <Arduino.h>
#include <OneButton.h>
#include <rng.h>
#include <sys.h>
#include <mpu.h>
#include <norflash.h>
#include <delay.h>
#include <led.h>
#include <sdram.h>
#include <lcd.h>
#include <key.h>
#include <touch.h>
#include <L_malloc1.h>
#include <custom.h>
#include <lvgl.h>
#include <lv_port_disp.h>
#include <lv_port_indev.h>
// #include <lv_port_fs.h>
#include <L_FreeRTOS.h>
#include <map>
#include <string>
#include <hello.h>
#include <sdmmc_sdcard.h>
#include <lvgl_demo.h>
std::map<std::string, OneButton> myButton1;
HardwareTimer mytimer(TIM6);


void setup() 
{
    Serial.begin(115200);
    sys_cache_enable();                     /* 使能L1-Cache */
    delay_init(520);                        /* 延时初始化 */
    led_init();                             /* 初始化LED */
    mpu_memory_protection();                /* 保护相关存储区域 */
    sdram_init();                           /* 初始化SDRAM */
    lcd_init();                             /* 初始化LCD */
    sd_init();
    
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
    
    
    lvgl_demo();
    
    // L_FreeRTOS::SetUp::setup();
}

void loop() { }
void SystemClock_Config(void) { sys_stm32_clock_init(104,5,1,2); }

// void SystemClock_Config(void)
// {
//   RCC_OscInitTypeDef RCC_OscInitStruct = {0};
//   RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

//   /** Supply configuration update enable
//   */
//   HAL_PWREx_ConfigSupply(PWR_LDO_SUPPLY);

//   /** Configure the main internal regulator output voltage
//   */
//   __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE0);

//   while(!__HAL_PWR_GET_FLAG(PWR_FLAG_VOSRDY)) {}

//   /** Initializes the RCC Oscillators according to the specified parameters
//   * in the RCC_OscInitTypeDef structure.
//   */
//   RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI48|RCC_OSCILLATORTYPE_HSE;
//   RCC_OscInitStruct.HSEState = RCC_HSE_ON;
//   RCC_OscInitStruct.HSI48State = RCC_HSI48_ON;
//   RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
//   RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
//   RCC_OscInitStruct.PLL.PLLM = 2;
//   RCC_OscInitStruct.PLL.PLLN = 44;
//   RCC_OscInitStruct.PLL.PLLP = 1;
//   RCC_OscInitStruct.PLL.PLLQ = 2;
//   RCC_OscInitStruct.PLL.PLLR = 2;
//   RCC_OscInitStruct.PLL.PLLRGE = RCC_PLL1VCIRANGE_3;
//   RCC_OscInitStruct.PLL.PLLVCOSEL = RCC_PLL1VCOWIDE;
//   RCC_OscInitStruct.PLL.PLLFRACN = 0;
//   if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
//   {
//     Error_Handler();
//   }

//   /** Initializes the CPU, AHB and APB buses clocks
//   */
//   RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
//                               |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2
//                               |RCC_CLOCKTYPE_D3PCLK1|RCC_CLOCKTYPE_D1PCLK1;
//   RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
//   RCC_ClkInitStruct.SYSCLKDivider = RCC_SYSCLK_DIV1;
//   RCC_ClkInitStruct.AHBCLKDivider = RCC_HCLK_DIV2;
//   RCC_ClkInitStruct.APB3CLKDivider = RCC_APB3_DIV2;
//   RCC_ClkInitStruct.APB1CLKDivider = RCC_APB1_DIV2;
//   RCC_ClkInitStruct.APB2CLKDivider = RCC_APB2_DIV2;
//   RCC_ClkInitStruct.APB4CLKDivider = RCC_APB4_DIV2;

//   if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_3) != HAL_OK)
//   {
//     Error_Handler();
//   }
// }