import neopixel
import time
from machine import Pin

# フォントを設定
import font_basic_8x8size
import font_basic_8x5size

# LEDの設定
NUM_LEDS =  26 * 8  # LEDの数 (アルファベットの文字数 × 8)
PIN = 0             # データピン

# NeoPixelオブジェクトの作成
np = neopixel.NeoPixel(Pin(PIN), NUM_LEDS)


colors = {
    'off'  : (0, 0, 0),
    'white': (10, 10, 10),
    'red'  : (10, 0, 0), 
    'green': (0, 10, 0),
    'blue' : (0, 0, 10),
}

# LEDにアルファベットを描画する関数
def draw_alphabet(alphabet, form, in_color, out_color):
    if form == '8x8': 
        pattern = font_basic_8x5size.alphabets.get(alphabet, None)
        if pattern:
            for y in range(8):
                for x in range(8):
                    index = y * 8 + x
                    if pattern[y][x] == '0':
                        np[index] = in_color  # 文字の色
                    else:
                        np[index] = out_color # 背景の色
            np.write()
            
# テキストを描画する関数
def draw_text(text, form, in_color_name, out_color_name, speed):
    in_color = colors.get(in_color_name, (0, 0, 0))
    out_color = colors.get(out_color_name, (0, 0, 0))
    for letter in text:
        draw_alphabet(letter, form, in_color, out_color)
        time.sleep(speed)  # 1秒ごとに次の文字に移動



def slide_in_animation(letter,  form, in_color, out_color, speed):
    pattern = font_basic_8x5size.alphabets.get(letter, None)
    if pattern:
        # 初期位置は画面外の右端に設定する
        for x_offset in range(8, -8, -1):  # 右端から左端に向かってシフト
            for y in range(8):
                for x in range(8):
                    if 0 <= x + x_offset < 8:  # 画面内に収まる範囲のLEDのみを操作
                        index = y * 8 + x + x_offset
                        if pattern[y][x] == '0':
                            np[index] = in_color
                        else:
                            np[index] = out_color
                    else:
                        # 画面外の部分は消灯
                        np[y * 10 + x] = out_color
                        
            np.write()
            time.sleep(speed)  # 表示の速度を調整するための待機時間

def draw_text_with_slide_in(text, form, in_color_name="white", out_color_name="off", speed=0.1):
    in_color = colors.get(in_color_name, (0, 0, 0))
    out_color = colors.get(out_color_name, (0, 0, 0))
    for letter in text:
        slide_in_animation(letter, form, in_color, out_color, speed)
        time.sleep(0.01)  # 文字と文字の間に少し待機する

# メインループ
while True:
    #draw_text("text", "8x5", "red", "off", time)
    #draw_text("ABC", "8x8", "red", "off", 1.0)
    draw_text_with_slide_in("ABC", "8x5", "blue", "off", 0.2)
    