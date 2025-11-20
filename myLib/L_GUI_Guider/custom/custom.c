/*
 * Copyright 2024 NXP
 * NXP Proprietary. This software is owned or controlled by NXP and may only be used strictly in
 * accordance with the applicable license terms. By expressly accepting such terms or by downloading, installing,
 * activating and/or otherwise using the software, you are agreeing that you have read, and that you agree to
 * comply with and are bound by, such license terms.  If you do not agree to be bound by the applicable license
 * terms, then you may not retain, install, activate or otherwise use the software.
 */

/*********************
 *      INCLUDES
 *********************/
#include <stdio.h>
#include "lvgl.h"
#include "custom.h"
#include <custom_events_cb.h>
#include <gui_guider.h>


/*********************
 *      DEFINES
 *********************/
lv_ui guider_ui;

/**********************
 *      TYPEDEFS
 **********************/

/**********************
 *  STATIC PROTOTYPES
 **********************/

/**********************
 *  STATIC VARIABLES
 **********************/

/**
 * Create a demo application
 */
void custom_init()
{
    /* Add your codes here */
    setup_ui(&guider_ui);
}

void screen_btn_22_event_handler_custom(lv_event_t * e)
{
    lv_event_code_t code = lv_event_get_code(e);

    if(code == LV_EVENT_CLICKED)
    {
        // cpp_cb_bridge();
    }
}

#if USEMYCBINC == 1
void mycb(lv_event_t * e)
{
    lv_obj_t *target = lv_event_get_target(e);  // Get the object that triggered the event
    lv_ui *ui = (lv_ui*)lv_event_get_user_data(e);
    
    if (lv_event_get_code(e) == LV_EVENT_PRESSED) 
    {
        if (target == ui->screen_btn_2) 
        {
            printf("button 2 pressed\n");
        }
        else if (target == ui->screen_btn_3)
        {
            printf("button 3 pressed\n"); 
        }
    } else if (lv_event_get_code(e) == LV_EVENT_PRESSING) 
    {
        if (target == ui->screen_btn_2) 
        {
            printf("button 2 pressing\n");
        }
        else if (target == ui->screen_btn_3)
        {
            printf("button 3 pressing\n"); 
        }
    }
}
#endif