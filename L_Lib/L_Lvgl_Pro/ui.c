/**
 * @file ui.c
 */

/*********************
 *      INCLUDES
 *********************/

#include "ui.h"

/*********************
 *      DEFINES
 *********************/

/**********************
 *      TYPEDEFS
 **********************/

/**********************
 *  STATIC PROTOTYPES
 **********************/

/**********************
 *  STATIC VARIABLES
 **********************/

/**********************
 *      MACROS
 **********************/

/**********************
 *   GLOBAL FUNCTIONS
 **********************/


void ui_init(const char * asset_path)
{
    ui_init_gen(asset_path);

    /* Add your own custom code here if needed */
    lv_obj_t *ui = screen_animations_create();
    lv_scr_load(ui);
}

/**********************
 *   STATIC FUNCTIONS
 **********************/