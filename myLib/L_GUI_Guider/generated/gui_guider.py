# Copyright 2025 NXP
# NXP Proprietary. This software is owned or controlled by NXP and may only be used strictly in
# accordance with the applicable license terms. By expressly accepting such terms or by downloading, installing,
# activating and/or otherwise using the software, you are agreeing that you have read, and that you agree to
# comply with and are bound by, such license terms.  If you do not agree to be bound by the applicable license
# terms, then you may not retain, install, activate or otherwise use the software.

import utime as time
import usys as sys
import lvgl as lv
import ustruct
import fs_driver

lv.init()

# Register display driver.
disp_drv = lv.sdl_window_create(1024, 600)
lv.sdl_window_set_resizeable(disp_drv, False)
lv.sdl_window_set_title(disp_drv, "Simulator (MicroPython)")

# Regsiter input driver
mouse = lv.sdl_mouse_create()

# Add default theme for bottom layer
bottom_layer = lv.layer_bottom()
lv.theme_apply(bottom_layer)

fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, 'Z')

def anim_x_cb(obj, v):
    obj.set_x(v)

def anim_y_cb(obj, v):
    obj.set_y(v)

def anim_width_cb(obj, v):
    obj.set_width(v)

def anim_height_cb(obj, v):
    obj.set_height(v)

def anim_img_zoom_cb(obj, v):
    obj.set_scale(v)

def anim_img_rotate_cb(obj, v):
    obj.set_rotation(v)

global_font_cache = {}
def test_font(font_family, font_size):
    global global_font_cache
    if font_family + str(font_size) in global_font_cache:
        return global_font_cache[font_family + str(font_size)]
    if font_size % 2:
        candidates = [
            (font_family, font_size),
            (font_family, font_size-font_size%2),
            (font_family, font_size+font_size%2),
            ("montserrat", font_size-font_size%2),
            ("montserrat", font_size+font_size%2),
            ("montserrat", 16)
        ]
    else:
        candidates = [
            (font_family, font_size),
            ("montserrat", font_size),
            ("montserrat", 16)
        ]
    for (family, size) in candidates:
        try:
            if eval(f'lv.font_{family}_{size}'):
                global_font_cache[font_family + str(font_size)] = eval(f'lv.font_{family}_{size}')
                if family != font_family or size != font_size:
                    print(f'WARNING: lv.font_{family}_{size} is used!')
                return eval(f'lv.font_{family}_{size}')
        except AttributeError:
            try:
                load_font = lv.binfont_create(f"Z:MicroPython/lv_font_{family}_{size}.fnt")
                global_font_cache[font_family + str(font_size)] = load_font
                return load_font
            except:
                if family == font_family and size == font_size:
                    print(f'WARNING: lv.font_{family}_{size} is NOT supported!')

global_image_cache = {}
def load_image(file):
    global global_image_cache
    if file in global_image_cache:
        return global_image_cache[file]
    try:
        with open(file,'rb') as f:
            data = f.read()
    except:
        print(f'Could not open {file}')
        sys.exit()

    img = lv.image_dsc_t({
        'data_size': len(data),
        'data': data
    })
    global_image_cache[file] = img
    return img

def calendar_event_handler(e,obj):
    code = e.get_code()

    if code == lv.EVENT.VALUE_CHANGED:
        source = lv.calendar.__cast__(e.get_current_target())
        date = lv.calendar_date_t()
        if source.get_pressed_date(date) == lv.RESULT.OK:
            source.set_highlighted_dates([date], 1)

def spinbox_increment_event_cb(e, obj):
    code = e.get_code()
    if code == lv.EVENT.SHORT_CLICKED or code == lv.EVENT.LONG_PRESSED_REPEAT:
        obj.increment()
def spinbox_decrement_event_cb(e, obj):
    code = e.get_code()
    if code == lv.EVENT.SHORT_CLICKED or code == lv.EVENT.LONG_PRESSED_REPEAT:
        obj.decrement()

def digital_clock_cb(timer, obj, current_time, show_second, use_ampm):
    hour = int(current_time[0])
    minute = int(current_time[1])
    second = int(current_time[2])
    ampm = current_time[3]
    second = second + 1
    if second == 60:
        second = 0
        minute = minute + 1
        if minute == 60:
            minute = 0
            hour = hour + 1
            if use_ampm:
                if hour == 12:
                    if ampm == 'AM':
                        ampm = 'PM'
                    elif ampm == 'PM':
                        ampm = 'AM'
                if hour > 12:
                    hour = hour % 12
    hour = hour % 24
    if use_ampm:
        if show_second:
            obj.set_text("%d:%02d:%02d %s" %(hour, minute, second, ampm))
        else:
            obj.set_text("%d:%02d %s" %(hour, minute, ampm))
    else:
        if show_second:
            obj.set_text("%d:%02d:%02d" %(hour, minute, second))
        else:
            obj.set_text("%d:%02d" %(hour, minute))
    current_time[0] = hour
    current_time[1] = minute
    current_time[2] = second
    current_time[3] = ampm

def analog_clock_cb(timer, obj):
    datetime = time.localtime()
    hour = datetime[3]
    if hour >= 12: hour = hour - 12
    obj.set_time(hour, datetime[4], datetime[5])

def datetext_event_handler(e, obj):
    code = e.get_code()
    datetext = lv.label.__cast__(e.get_target())
    if code == lv.EVENT.FOCUSED:
        if obj is None:
            bg = lv.layer_top()
            bg.add_flag(lv.obj.FLAG.CLICKABLE)
            obj = lv.calendar(bg)
            scr = lv.screen_active()
            scr_height = scr.get_height()
            scr_width = scr.get_width()
            obj.set_size(int(scr_width * 0.8), int(scr_height * 0.8))
            datestring = datetext.get_text()
            year = int(datestring.split('/')[0])
            month = int(datestring.split('/')[1])
            day = int(datestring.split('/')[2])
            obj.set_showed_date(year, month)
            highlighted_days=[lv.calendar_date_t({'year':year, 'month':month, 'day':day})]
            obj.set_highlighted_dates(highlighted_days, 1)
            obj.align(lv.ALIGN.CENTER, 0, 0)
            lv.calendar_header_arrow(obj)
            obj.add_event_cb(lambda e: datetext_calendar_event_handler(e, datetext), lv.EVENT.ALL, None)
            scr.update_layout()

def datetext_calendar_event_handler(e, obj):
    code = e.get_code()
    calendar = lv.calendar.__cast__(e.get_current_target())
    if code == lv.EVENT.VALUE_CHANGED:
        date = lv.calendar_date_t()
        if calendar.get_pressed_date(date) == lv.RESULT.OK:
            obj.set_text(f"{date.year}/{date.month}/{date.day}")
            bg = lv.layer_top()
            bg.remove_flag(lv.obj.FLAG.CLICKABLE)
            bg.set_style_bg_opa(lv.OPA.TRANSP, 0)
            calendar.delete()

# Create screen
screen = lv.obj()
screen.set_size(1024, 600)
screen.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen.set_style_bg_image_src(load_image(r"C:\Users\chuhong\OneDrive\Documents\PlatformIO\Projects\L_2025_Stm32H723ZGT6_Arduino\myLib\L_GUI_Guider\generated\MicroPython\Chiyo_chan_1024_600.png"), lv.PART.MAIN|lv.STATE.DEFAULT)
screen.set_style_bg_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen.set_style_bg_image_recolor_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_1
screen_btn_1 = lv.button(screen)
screen_btn_1_label = lv.label(screen_btn_1)
screen_btn_1_label.set_text("LED_ON")
screen_btn_1_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_1_label.set_width(lv.pct(100))
screen_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_1.set_pos(25, 38)
screen_btn_1.set_size(100, 50)
# Set style for screen_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_1.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_1.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_1.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_2
screen_btn_2 = lv.button(screen)
screen_btn_2_label = lv.label(screen_btn_2)
screen_btn_2_label.set_text("Button")
screen_btn_2_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_2_label.set_width(lv.pct(100))
screen_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_2.set_pos(154, 114)
screen_btn_2.set_size(100, 50)
# Set style for screen_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_2.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_2.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_2.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_2.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_3
screen_btn_3 = lv.button(screen)
screen_btn_3_label = lv.label(screen_btn_3)
screen_btn_3_label.set_text("LED_OFF")
screen_btn_3_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_3_label.set_width(lv.pct(100))
screen_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_3.set_pos(60, 194)
screen_btn_3.set_size(100, 50)
# Set style for screen_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_3.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_3.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_3.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_3.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_4
screen_btn_4 = lv.button(screen)
screen_btn_4_label = lv.label(screen_btn_4)
screen_btn_4_label.set_text("Button")
screen_btn_4_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_4_label.set_width(lv.pct(100))
screen_btn_4_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_4.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_4.set_pos(450, 186)
screen_btn_4.set_size(100, 50)
# Set style for screen_btn_4, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_4.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_4.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_4.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_4.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_4.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_4.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_4.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_4.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_4.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_4.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_5
screen_btn_5 = lv.button(screen)
screen_btn_5_label = lv.label(screen_btn_5)
screen_btn_5_label.set_text("696969Button696969")
screen_btn_5_label.set_long_mode(lv.label.LONG.SCROLL_CIRCULAR)
screen_btn_5_label.set_width(lv.pct(100))
screen_btn_5_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_5.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_5.set_pos(273, 391)
screen_btn_5.set_size(100, 50)
# Set style for screen_btn_5, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_5.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_5.set_style_bg_color(lv.color_hex(0x050a0d), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_5.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_5.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_5.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_5.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_5.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_5.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_5.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_5.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_6
screen_btn_6 = lv.button(screen)
screen_btn_6_label = lv.label(screen_btn_6)
screen_btn_6_label.set_text("Button")
screen_btn_6_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_6_label.set_width(lv.pct(100))
screen_btn_6_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_6.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_6.set_pos(863, 514)
screen_btn_6.set_size(100, 50)
# Set style for screen_btn_6, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_6.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_6.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_6.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_6.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_6.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_6.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_6.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_6.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_6.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_6.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_7
screen_btn_7 = lv.button(screen)
screen_btn_7_label = lv.label(screen_btn_7)
screen_btn_7_label.set_text("Button")
screen_btn_7_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_7_label.set_width(lv.pct(100))
screen_btn_7_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_7.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_7.set_pos(71, 464)
screen_btn_7.set_size(100, 50)
# Set style for screen_btn_7, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_7.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_7.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_7.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_7.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_7.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_7.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_7.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_7.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_7.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_7.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_8
screen_btn_8 = lv.button(screen)
screen_btn_8_label = lv.label(screen_btn_8)
screen_btn_8_label.set_text("Button")
screen_btn_8_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_8_label.set_width(lv.pct(100))
screen_btn_8_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_8.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_8.set_pos(47, 332)
screen_btn_8.set_size(100, 50)
# Set style for screen_btn_8, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_8.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_8.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_8.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_8.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_8.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_8.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_8.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_8.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_8.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_8.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_9
screen_btn_9 = lv.button(screen)
screen_btn_9_label = lv.label(screen_btn_9)
screen_btn_9_label.set_text("What is done is done")
screen_btn_9_label.set_long_mode(lv.label.LONG.SCROLL_CIRCULAR)
screen_btn_9_label.set_width(lv.pct(100))
screen_btn_9_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_9.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_9.set_pos(693, 461)
screen_btn_9.set_size(144, 68)
# Set style for screen_btn_9, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_9.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_9.set_style_bg_color(lv.color_hex(0x41614b), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_9.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_9.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_9.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_9.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_9.set_style_text_color(lv.color_hex(0xdf43d5), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_9.set_style_text_font(test_font("montserratMedium", 22), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_9.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_9.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_10
screen_btn_10 = lv.button(screen)
screen_btn_10_label = lv.label(screen_btn_10)
screen_btn_10_label.set_text("What is going on")
screen_btn_10_label.set_long_mode(lv.label.LONG.SCROLL_CIRCULAR)
screen_btn_10_label.set_width(lv.pct(100))
screen_btn_10_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_10.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_10.set_pos(778, 29)
screen_btn_10.set_size(158, 69)
# Set style for screen_btn_10, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_10.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_10.set_style_bg_color(lv.color_hex(0x2FCADA), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_10.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_10.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_10.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_10.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_10.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_10.set_style_text_font(test_font("FontAwesome5", 32), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_10.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_10.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_11
screen_btn_11 = lv.button(screen)
screen_btn_11_label = lv.label(screen_btn_11)
screen_btn_11_label.set_text("69")
screen_btn_11_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_11_label.set_width(lv.pct(100))
screen_btn_11_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_11.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_11.set_pos(467, 38)
screen_btn_11.set_size(100, 50)
# Set style for screen_btn_11, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_11.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_11.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_11.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_11.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_11.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_11.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_11.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_11.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_11.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_11.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_12
screen_btn_12 = lv.button(screen)
screen_btn_12_label = lv.label(screen_btn_12)
screen_btn_12_label.set_text("6699")
screen_btn_12_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_12_label.set_width(lv.pct(100))
screen_btn_12_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_12.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_12.set_pos(283, 183)
screen_btn_12.set_size(100, 50)
# Set style for screen_btn_12, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_12.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_12.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_12.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_12.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_12.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_12.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_12.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_12.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_12.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_12.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_13
screen_btn_13 = lv.button(screen)
screen_btn_13_label = lv.label(screen_btn_13)
screen_btn_13_label.set_text("Button")
screen_btn_13_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_13_label.set_width(lv.pct(100))
screen_btn_13_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_13.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_13.set_pos(799, 236)
screen_btn_13.set_size(100, 50)
# Set style for screen_btn_13, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_13.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_13.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_13.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_13.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_13.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_13.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_13.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_13.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_13.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_13.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_14
screen_btn_14 = lv.button(screen)
screen_btn_14_label = lv.label(screen_btn_14)
screen_btn_14_label.set_text("Button")
screen_btn_14_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_14_label.set_width(lv.pct(100))
screen_btn_14_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_14.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_14.set_pos(532, 511)
screen_btn_14.set_size(100, 50)
# Set style for screen_btn_14, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_14.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_14.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_14.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_14.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_14.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_14.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_14.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_14.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_14.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_14.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_15
screen_btn_15 = lv.button(screen)
screen_btn_15_label = lv.label(screen_btn_15)
screen_btn_15_label.set_text("Button")
screen_btn_15_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_15_label.set_width(lv.pct(100))
screen_btn_15_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_15.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_15.set_pos(661, 133)
screen_btn_15.set_size(100, 50)
# Set style for screen_btn_15, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_15.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_15.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_15.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_15.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_15.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_15.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_15.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_15.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_15.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_15.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_16
screen_btn_16 = lv.button(screen)
screen_btn_16_label = lv.label(screen_btn_16)
screen_btn_16_label.set_text("Button")
screen_btn_16_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_16_label.set_width(lv.pct(100))
screen_btn_16_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_16.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_16.set_pos(289, 38)
screen_btn_16.set_size(100, 50)
# Set style for screen_btn_16, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_16.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_16.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_16.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_16.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_16.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_16.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_16.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_16.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_16.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_16.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_17
screen_btn_17 = lv.button(screen)
screen_btn_17_label = lv.label(screen_btn_17)
screen_btn_17_label.set_text("Button")
screen_btn_17_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_17_label.set_width(lv.pct(100))
screen_btn_17_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_17.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_17.set_pos(273, 511)
screen_btn_17.set_size(100, 50)
# Set style for screen_btn_17, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_17.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_17.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_17.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_17.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_17.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_17.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_17.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_17.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_17.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_17.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_18
screen_btn_18 = lv.button(screen)
screen_btn_18_label = lv.label(screen_btn_18)
screen_btn_18_label.set_text("Button")
screen_btn_18_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_18_label.set_width(lv.pct(100))
screen_btn_18_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_18.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_18.set_pos(612, 325)
screen_btn_18.set_size(100, 50)
# Set style for screen_btn_18, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_18.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_18.set_style_bg_color(lv.color_hex(0x111416), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_18.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_18.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_18.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_18.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_18.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_18.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_18.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_18.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_19
screen_btn_19 = lv.button(screen)
screen_btn_19_label = lv.label(screen_btn_19)
screen_btn_19_label.set_text("Button")
screen_btn_19_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_19_label.set_width(lv.pct(100))
screen_btn_19_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_19.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_19.set_pos(140, 257)
screen_btn_19.set_size(100, 50)
# Set style for screen_btn_19, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_19.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_19.set_style_bg_color(lv.color_hex(0x2a4256), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_19.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_19.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_19.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_19.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_19.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_19.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_19.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_19.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_20
screen_btn_20 = lv.button(screen)
screen_btn_20_label = lv.label(screen_btn_20)
screen_btn_20_label.set_text("Button")
screen_btn_20_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_20_label.set_width(lv.pct(100))
screen_btn_20_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_20.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_20.set_pos(883, 332)
screen_btn_20.set_size(100, 50)
# Set style for screen_btn_20, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_20.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_20.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_20.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_20.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_20.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_20.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_20.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_20.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_20.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_20.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_21
screen_btn_21 = lv.button(screen)
screen_btn_21_label = lv.label(screen_btn_21)
screen_btn_21_label.set_text("Button")
screen_btn_21_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_21_label.set_width(lv.pct(100))
screen_btn_21_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_21.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_21.set_pos(875, 152)
screen_btn_21.set_size(100, 50)
# Set style for screen_btn_21, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_21.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_21.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_21.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_21.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_21.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_21.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_21.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_21.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_21.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_21.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_btn_22
screen_btn_22 = lv.button(screen)
screen_btn_22_label = lv.label(screen_btn_22)
screen_btn_22_label.set_text("6699")
screen_btn_22_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_22_label.set_width(lv.pct(100))
screen_btn_22_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_22.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_22.set_pos(266, 312)
screen_btn_22.set_size(100, 50)
# Set style for screen_btn_22, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_22.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_22.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_22.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_22.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_22.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_22.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_22.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_22.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_22.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_22.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_led_1
screen_led_1 = lv.led(screen)
screen_led_1.set_brightness(255)
screen_led_1.set_color(lv.color_hex(0x00a1b5))
screen_led_1.set_pos(426, 351)
screen_led_1.set_size(40, 40)

# Create screen_btn_23
screen_btn_23 = lv.button(screen)
screen_btn_23_label = lv.label(screen_btn_23)
screen_btn_23_label.set_text("Button")
screen_btn_23_label.set_long_mode(lv.label.LONG.WRAP)
screen_btn_23_label.set_width(lv.pct(100))
screen_btn_23_label.align(lv.ALIGN.CENTER, 0, 0)
screen_btn_23.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_23.set_pos(386, 461)
screen_btn_23.set_size(100, 50)
# Set style for screen_btn_23, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_btn_23.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_23.set_style_bg_color(lv.color_hex(0x2195f6), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_23.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_23.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_23.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_23.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_23.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_23.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_23.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_btn_23.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_label_1
screen_label_1 = lv.label(screen)
screen_label_1.set_text("Label")
screen_label_1.set_long_mode(lv.label.LONG.WRAP)
screen_label_1.set_width(lv.pct(100))
screen_label_1.set_pos(588, 38)
screen_label_1.set_size(141, 47)
# Set style for screen_label_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_label_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_label_1.set_style_radius(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_label_1.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_label_1.set_style_text_font(test_font("montserratMedium", 16), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_label_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_label_1.set_style_text_letter_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_label_1.set_style_text_line_space(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_label_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_label_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_label_1.set_style_pad_top(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_label_1.set_style_pad_right(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_label_1.set_style_pad_bottom(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_label_1.set_style_pad_left(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_label_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)

screen.update_layout()
# Create screen_1
screen_1 = lv.obj()
screen_1.set_size(1024, 600)
screen_1.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# Set style for screen_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_1.set_style_bg_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1.set_style_bg_image_src(load_image(r"C:\Users\chuhong\OneDrive\Documents\PlatformIO\Projects\L_2025_Stm32H723ZGT6_Arduino\myLib\L_GUI_Guider\generated\MicroPython\Chiyo_chan_1024_600.png"), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1.set_style_bg_image_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1.set_style_bg_image_recolor_opa(0, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_1_btn_1
screen_1_btn_1 = lv.button(screen_1)
screen_1_btn_1_label = lv.label(screen_1_btn_1)
screen_1_btn_1_label.set_text("Chiyo-chan and Osaka-chan")
screen_1_btn_1_label.set_long_mode(lv.label.LONG.SCROLL)
screen_1_btn_1_label.set_width(lv.pct(100))
screen_1_btn_1_label.align(lv.ALIGN.CENTER, 0, 0)
screen_1_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_1_btn_1.set_pos(28, 0)
screen_1_btn_1.set_size(967, 149)
# Set style for screen_1_btn_1, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_1_btn_1.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_1.set_style_bg_color(lv.color_hex(0x2FDAAE), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_1.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_1.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_1.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_1.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_1.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_1.set_style_text_font(test_font("FontAwesome5", 86), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_1.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_1.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_1_btn_2
screen_1_btn_2 = lv.button(screen_1)
screen_1_btn_2_label = lv.label(screen_1_btn_2)
screen_1_btn_2_label.set_text("Chiyo-chan and Osaka-chan")
screen_1_btn_2_label.set_long_mode(lv.label.LONG.SCROLL)
screen_1_btn_2_label.set_width(lv.pct(100))
screen_1_btn_2_label.align(lv.ALIGN.CENTER, 0, 0)
screen_1_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_1_btn_2.set_pos(28, 451)
screen_1_btn_2.set_size(967, 149)
# Set style for screen_1_btn_2, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_1_btn_2.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_2.set_style_bg_color(lv.color_hex(0x2FDAAE), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_2.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_2.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_2.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_2.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_2.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_2.set_style_text_font(test_font("FontAwesome5", 86), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_2.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_2.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

# Create screen_1_btn_3
screen_1_btn_3 = lv.button(screen_1)
screen_1_btn_3_label = lv.label(screen_1_btn_3)
screen_1_btn_3_label.set_text("Chiyo-chan and Osaka-chan")
screen_1_btn_3_label.set_long_mode(lv.label.LONG.SCROLL)
screen_1_btn_3_label.set_width(lv.pct(100))
screen_1_btn_3_label.align(lv.ALIGN.CENTER, 0, 0)
screen_1_btn_3.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_1_btn_3.set_pos(23, 225)
screen_1_btn_3.set_size(967, 149)
# Set style for screen_1_btn_3, Part: lv.PART.MAIN, State: lv.STATE.DEFAULT.
screen_1_btn_3.set_style_bg_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_3.set_style_bg_color(lv.color_hex(0x2FDAAE), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_3.set_style_bg_grad_dir(lv.GRAD_DIR.NONE, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_3.set_style_border_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_3.set_style_radius(5, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_3.set_style_shadow_width(0, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_3.set_style_text_color(lv.color_hex(0xffffff), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_3.set_style_text_font(test_font("FontAwesome5", 86), lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_3.set_style_text_opa(255, lv.PART.MAIN|lv.STATE.DEFAULT)
screen_1_btn_3.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_1.update_layout()

def screen_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.SCREEN_LOADED):
        pass
        

screen.add_event_cb(lambda e: screen_event_handler(e), lv.EVENT.ALL, None)

def screen_btn_1_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.PRESSED):
        pass
screen_btn_1.add_event_cb(lambda e: screen_btn_1_event_handler(e), lv.EVENT.ALL, None)

def screen_btn_3_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.PRESSED):
        pass
screen_btn_3.add_event_cb(lambda e: screen_btn_3_event_handler(e), lv.EVENT.ALL, None)

def screen_btn_7_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
        lv.screen_load_anim(screen_1, lv.SCR_LOAD_ANIM.OVER_BOTTOM, 200, 200, False)
screen_btn_7.add_event_cb(lambda e: screen_btn_7_event_handler(e), lv.EVENT.ALL, None)

def screen_btn_8_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
        screen_led_1.set_color(lv.color_hex(0xd20404))
screen_btn_8.add_event_cb(lambda e: screen_btn_8_event_handler(e), lv.EVENT.ALL, None)

def screen_btn_10_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.PRESSED):
        pass
screen_btn_10.add_event_cb(lambda e: screen_btn_10_event_handler(e), lv.EVENT.ALL, None)

def screen_btn_22_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
        

screen_btn_22.add_event_cb(lambda e: screen_btn_22_event_handler(e), lv.EVENT.ALL, None)

def screen_1_btn_1_event_handler(e):
    code = e.get_code()
    if (code == lv.EVENT.CLICKED):
        pass
        lv.screen_load_anim(screen, lv.SCR_LOAD_ANIM.FADE_ON, 200, 200, False)
screen_1_btn_1.add_event_cb(lambda e: screen_1_btn_1_event_handler(e), lv.EVENT.ALL, None)

# content from custom.py

# Load the default screen
lv.screen_load(screen)

if __name__ == '__main__':
    while True:
        lv.task_handler()
        time.sleep_ms(5)
