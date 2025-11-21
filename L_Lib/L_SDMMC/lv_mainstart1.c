/**
 ****************************************************************************************************
 * @file        lv_mainstart.c
 * @version     V1.0
 * @brief       LVGL 文件系统使用 实验
 ****************************************************************************************************
 * @attention   Waiken-Smart 慧勤智远
 *
 * 实验平台:    STM32H723ZGT6小系统板
 *
 ****************************************************************************************************
 */
 
#include "lv_mainstart1.h"
#include "lvgl.h"
#include <stdio.h>

/**
 * @brief  获取指针位置
 * @param  fd：文件指针
 * @return 返回名称
 */
long lv_tell(lv_fs_file_t *fd)
{
    uint32_t pos = 0;
    lv_fs_tell(fd, &pos);
    return pos;
}

/**
 * @brief  文件系统测试
 * @param  无
 * @return 无
 */
static void lv_fs_test(void)
{
    char rbuf[30] = {0};
    uint32_t rsize = 0;
    lv_fs_file_t fd;
    lv_fs_res_t res;

    res = lv_fs_open(&fd, "S:/love/what.txt", LV_FS_MODE_RD);
    
    if (res != LV_FS_RES_OK)
    {
        printf("open S:/Fatfs_test.txt ERROR\n");
        return ;
    }
    
    lv_tell(&fd);

    lv_fs_seek(&fd, 0,LV_FS_SEEK_SET);
    lv_tell(&fd);

    res = lv_fs_read(&fd, rbuf, 100, &rsize);
    
    if (res != LV_FS_RES_OK)
    {
        printf("read ERROR\n");
        return ;
    }
    
    lv_tell(&fd);
    printf("READ(%d): %s",rsize , rbuf);

    lv_fs_close(&fd);
}

/**
 * @brief  文件系统演示
 * @param  无
 * @return 无
 */
void lv_mainstart1(void)
{
    // lv_obj_t *label = lv_label_create(lv_scr_act());
    // lv_label_set_text(label, "FATFS TEST");
    // lv_obj_center(label);
    lv_fs_test();
}
