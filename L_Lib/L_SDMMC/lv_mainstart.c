/**
 ****************************************************************************************************
 * @file        lv_mainstart.c
 * @version     V1.0
 * @brief       LVGL JPEG图片显示实验
 ****************************************************************************************************
 * @attention   Waiken-Smart 慧勤智远
 *
 * 实验平台:    STM32H723ZGT6小系统板
 *
 ****************************************************************************************************
 */
 
#include "lv_mainstart.h"
#include "lvgl.h"
#include <stdio.h>

/**
 * @brief       LVGL程序入口
 * @param       无
 * @retval      无
 */
void lv_mainstart()
{
    /* 创建标签 */
    lv_obj_t *label = lv_label_create(lv_scr_act());
    /* 设置标签文本 */
    lv_label_set_text(label, "JPEG_Decoder");
    /* 设置文本颜色 */
    lv_obj_set_style_text_color(label, lv_palette_main(LV_PALETTE_RED), LV_STATE_DEFAULT);
    /* 设置文本字体 */
    lv_obj_set_style_text_font(label, &lv_font_montserrat_32, LV_STATE_DEFAULT);
    /* 设置顶部中间对齐 */
    lv_obj_align(label, LV_ALIGN_TOP_MID, 0, 0);
    /* 设置背景颜色 */
    lv_obj_set_style_bg_color(lv_scr_act(), lv_palette_main(LV_PALETTE_BLUE), LV_STATE_DEFAULT);   
    /* 初始化 JPEG 解码器 */
    lv_tjpgd_init();    
    /* 创建 image 控件 */
    lv_obj_t *img = lv_img_create(lv_scr_act());
    /* 设置图像源 */
    // lv_img_set_src(img, "S:/PICTURE/JPEG/Mini GD32.jpg");
    lv_img_set_src(img, "S:/PICTURE/JPEG/Chiyo and Osaka.jpg");
    /* 中间对齐 */
    lv_obj_align(img, LV_ALIGN_CENTER, 0, 0);
}
