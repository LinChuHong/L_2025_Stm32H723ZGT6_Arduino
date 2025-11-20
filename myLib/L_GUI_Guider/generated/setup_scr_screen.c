/*
* Copyright 2025 NXP
* NXP Proprietary. This software is owned or controlled by NXP and may only be used strictly in
* accordance with the applicable license terms. By expressly accepting such terms or by downloading, installing,
* activating and/or otherwise using the software, you are agreeing that you have read, and that you agree to
* comply with and are bound by, such license terms.  If you do not agree to be bound by the applicable license
* terms, then you may not retain, install, activate or otherwise use the software.
*/

#include "lvgl.h"
#include <stdio.h>
#include "gui_guider.h"
#include "events_init.h"
#include "widgets_init.h"
#include "custom.h"
#include <lvgl.h>


void setup_scr_screen(lv_ui *ui)
{
    //Write codes screen
    ui->screen = lv_obj_create(NULL);
    lv_obj_set_size(ui->screen, 1024, 600);
    lv_obj_set_scrollbar_mode(ui->screen, LV_SCROLLBAR_MODE_OFF);

    //Write style for screen, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->screen, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
#if LV_USE_GUIDER_SIMULATOR
    lv_obj_set_style_bg_image_src(ui->screen, "C:\\Users\\chuhong\\OneDrive\\Documents\\PlatformIO\\Projects\\L_2025_Stm32H723ZGT6_Arduino\\myLib\\L_GUI_Guider\\import\\image\\Chiyo_chan.jpg", LV_PART_MAIN|LV_STATE_DEFAULT);
#else
    lv_obj_set_style_bg_image_src(ui->screen, "F:/Chiyo_chan.bin", LV_PART_MAIN|LV_STATE_DEFAULT);
#endif
    lv_obj_set_style_bg_image_opa(ui->screen, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_image_recolor_opa(ui->screen, 0, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes screen_btn_2
    ui->screen_btn_2 = lv_button_create(ui->screen);
    lv_obj_set_pos(ui->screen_btn_2, 13, 16);
    lv_obj_set_size(ui->screen_btn_2, 271, 128);
    ui->screen_btn_2_label = lv_label_create(ui->screen_btn_2);
    lv_label_set_text(ui->screen_btn_2_label, "");
    lv_label_set_long_mode(ui->screen_btn_2_label, LV_LABEL_LONG_SCROLL_CIRCULAR);
    lv_obj_align(ui->screen_btn_2_label, LV_ALIGN_CENTER, 0, 0);
    lv_obj_set_style_pad_all(ui->screen_btn_2, 0, LV_STATE_DEFAULT);
    lv_obj_set_width(ui->screen_btn_2_label, LV_PCT(100));

    //Write style for screen_btn_2, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->screen_btn_2, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->screen_btn_2, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->screen_btn_2, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->screen_btn_2, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->screen_btn_2, 5, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->screen_btn_2, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
#if LV_USE_GUIDER_SIMULATOR
    lv_obj_set_style_bg_image_src(ui->screen_btn_2, "C:\\Users\\chuhong\\OneDrive\\Documents\\PlatformIO\\Projects\\L_2025_Stm32H723ZGT6_Arduino\\myLib\\L_GUI_Guider\\import\\image\\IMG_2066.JPG", LV_PART_MAIN|LV_STATE_DEFAULT);
#else
    lv_obj_set_style_bg_image_src(ui->screen_btn_2, "F:/IMG_2066.bin", LV_PART_MAIN|LV_STATE_DEFAULT);
#endif
    lv_obj_set_style_bg_image_opa(ui->screen_btn_2, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_image_recolor_opa(ui->screen_btn_2, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->screen_btn_2, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->screen_btn_2, &lv_font_montserratMedium_46, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->screen_btn_2, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->screen_btn_2, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes screen_img_1
    ui->screen_img_1 = lv_image_create(ui->screen);
    lv_obj_set_pos(ui->screen_img_1, 838, 94);
    lv_obj_set_size(ui->screen_img_1, 158, 149);
    lv_obj_add_flag(ui->screen_img_1, LV_OBJ_FLAG_CLICKABLE);
#if LV_USE_GUIDER_SIMULATOR
    lv_image_set_src(ui->screen_img_1, "C:\\Users\\chuhong\\OneDrive\\Documents\\PlatformIO\\Projects\\L_2025_Stm32H723ZGT6_Arduino\\myLib\\L_GUI_Guider\\import\\image\\IMG_2066.JPG");
#else
    lv_image_set_src(ui->screen_img_1, "F:/IMG_2066.bin");
#endif
    lv_image_set_pivot(ui->screen_img_1, 50,50);
    lv_image_set_rotation(ui->screen_img_1, 0);

    //Write style for screen_img_1, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_image_recolor_opa(ui->screen_img_1, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_image_opa(ui->screen_img_1, 255, LV_PART_MAIN|LV_STATE_DEFAULT);

    //Write codes screen_btn_3
    ui->screen_btn_3 = lv_button_create(ui->screen);
    lv_obj_set_pos(ui->screen_btn_3, 330, 46);
    lv_obj_set_size(ui->screen_btn_3, 187, 151);
    ui->screen_btn_3_label = lv_label_create(ui->screen_btn_3);
    lv_label_set_text(ui->screen_btn_3_label, "");
    lv_label_set_long_mode(ui->screen_btn_3_label, LV_LABEL_LONG_WRAP);
    lv_obj_align(ui->screen_btn_3_label, LV_ALIGN_CENTER, 0, 0);
    lv_obj_set_style_pad_all(ui->screen_btn_3, 0, LV_STATE_DEFAULT);
    lv_obj_set_width(ui->screen_btn_3_label, LV_PCT(100));

    //Write style for screen_btn_3, Part: LV_PART_MAIN, State: LV_STATE_DEFAULT.
    lv_obj_set_style_bg_opa(ui->screen_btn_3, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_color(ui->screen_btn_3, lv_color_hex(0x2195f6), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_grad_dir(ui->screen_btn_3, LV_GRAD_DIR_NONE, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_border_width(ui->screen_btn_3, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_radius(ui->screen_btn_3, 5, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_shadow_width(ui->screen_btn_3, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
#if LV_USE_GUIDER_SIMULATOR
    lv_obj_set_style_bg_image_src(ui->screen_btn_3, "C:\\Users\\chuhong\\OneDrive\\Documents\\PlatformIO\\Projects\\L_2025_Stm32H723ZGT6_Arduino\\myLib\\L_GUI_Guider\\import\\image\\dmsler.png", LV_PART_MAIN|LV_STATE_DEFAULT);
#else
    lv_obj_set_style_bg_image_src(ui->screen_btn_3, "F:/dmsler.bin", LV_PART_MAIN|LV_STATE_DEFAULT);
#endif
    lv_obj_set_style_bg_image_opa(ui->screen_btn_3, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_bg_image_recolor_opa(ui->screen_btn_3, 0, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_color(ui->screen_btn_3, lv_color_hex(0xffffff), LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_font(ui->screen_btn_3, &lv_font_montserratMedium_46, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_opa(ui->screen_btn_3, 255, LV_PART_MAIN|LV_STATE_DEFAULT);
    lv_obj_set_style_text_align(ui->screen_btn_3, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN|LV_STATE_DEFAULT);

    //The custom code of screen.


    //Update current screen layout.
    lv_obj_update_layout(ui->screen);

    //Init events for screen.
    events_init_screen(ui);
}
