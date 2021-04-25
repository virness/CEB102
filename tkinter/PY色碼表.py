#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('conda install tkinter')


# In[3]:


#python支援的色圖表

from tkinter import *
colors = '''#FFB6C1 LightPink 淺粉紅
#FFC0CB Pink 粉紅
#DC143C Crimson 深紅/猩紅
#FFF0F5 LavenderBlush 淡紫紅
#DB7093 PaleVioletRed 弱紫羅蘭紅
#FF69B4 HotPink 熱情的粉紅
#FF1493 DeepPink 深粉紅
#C71585 MediumVioletRed 中紫羅蘭紅
#DA70D6 Orchid 暗紫色/蘭花紫
#D8BFD8 Thistle 薊色
#DDA0DD Plum 洋李色/李子紫
#EE82EE Violet 紫羅蘭
#FF00FF Magenta 洋紅/玫瑰紅
#FF00FF Fuchsia 紫紅/燈籠海棠
#8B008B DarkMagenta 深洋紅
#800080 Purple 紫色
#BA55D3 MediumOrchid 中蘭花紫
#9400D3 DarkViolet 暗紫羅蘭
#9932CC DarkOrchid 暗蘭花紫
#4B0082 Indigo 靛青/紫蘭色
#8A2BE2 BlueViolet 藍紫羅蘭
#9370DB MediumPurple 中紫色
#7B68EE MediumSlateBlue 中暗藍色/中板巖藍
#6A5ACD SlateBlue 石藍色/板岩藍
#483D8B DarkSlateBlue 暗灰藍色/暗板岩藍
#E6E6FA Lavender 淡紫色/熏衣草淡紫
#F8F8FF GhostWhite 幽靈白
#0000FF Blue 純藍
#0000CD MediumBlue 中藍色
#191970 MidnightBlue 午夜藍
#00008B DarkBlue 暗藍色
#000080 Navy 海軍藍
#4169E1 RoyalBlue 皇家藍/寶藍
#6495ED CornflowerBlue 矢車菊藍
#B0C4DE LightSteelBlue 亮鋼藍
#778899 LightSlateGray 亮藍灰/亮石板灰
#708090 SlateGray 灰石色/石板灰
#1E90FF DodgerBlue 閃蘭色/道奇藍
#F0F8FF AliceBlue 愛麗絲藍
#4682B4 SteelBlue 鋼藍/鐵青
#87CEFA LightSkyBlue 亮天藍色
#87CEEB SkyBlue 天藍色
#00BFFF DeepSkyBlue 深天藍
#ADD8E6 LightBlue 亮藍
#B0E0E6 PowderBlue 粉藍色/火藥青
#5F9EA0 CadetBlue 軍蘭色/軍服藍
#F0FFFF Azure 蔚藍色
#E0FFFF LightCyan 淡青色
#AFEEEE PaleTurquoise 弱綠寶石
#00FFFF Cyan 青色
#00FFFF Aqua 淺綠色/水色
#00CED1 DarkTurquoise 暗綠寶石
#2F4F4F DarkSlateGray 暗瓦灰色/暗石板灰
#008B8B DarkCyan 暗青色
#008080 Teal 水鴨色
#48D1CC MediumTurquoise 中綠寶石
#20B2AA LightSeaGreen 淺海洋綠
#40E0D0 Turquoise 綠寶石
#7FFFD4 Aquamarine 寶石碧綠
#66CDAA MediumAquamarine 中寶石碧綠
#00FA9A MediumSpringGreen 中春綠色
#F5FFFA MintCream 薄荷奶油
#00FF7F SpringGreen 春綠色
#3CB371 MediumSeaGreen 中海洋綠
#2E8B57 SeaGreen 海洋綠
#F0FFF0 Honeydew 蜜色/蜜瓜色
#90EE90 LightGreen 淡綠色
#98FB98 PaleGreen 弱綠色
#8FBC8F DarkSeaGreen 暗海洋綠
#32CD32 LimeGreen 閃光深綠
#00FF00 Lime 閃光綠
#228B22 ForestGreen 森林綠
#008000 Green 純綠
#006400 DarkGreen 暗綠色
#7FFF00 Chartreuse 黃綠色/查特酒綠
#7CFC00 LawnGreen 草綠色/草坪綠
#ADFF2F GreenYellow 綠黃色
#556B2F DarkOliveGreen 暗橄欖綠
#9ACD32 YellowGreen 黃綠色
#6B8E23 OliveDrab 橄欖褐色
#F5F5DC Beige 米色/灰棕色
#FAFAD2 LightGoldenrodYellow 亮菊黃
#FFFFF0 Ivory 象牙色
#FFFFE0 LightYellow 淺黃色
#FFFF00 Yellow 純黃
#808000 Olive 橄欖
#BDB76B DarkKhaki 暗黃褐色/深卡嘰布
#FFFACD LemonChiffon 檸檬綢
#EEE8AA PaleGoldenrod 灰菊黃/蒼麒麟色
#F0E68C Khaki 黃褐色/卡嘰布
#FFD700 Gold 金色
#FFF8DC Cornsilk 玉米絲色
#DAA520 Goldenrod 金菊黃
#B8860B DarkGoldenrod 暗金菊黃
#FFFAF0 FloralWhite 花的白色
#FDF5E6 OldLace 老花色/舊蕾絲
#F5DEB3 Wheat 淺黃色/小麥色
#FFE4B5 Moccasin 鹿皮色/鹿皮靴
#FFA500 Orange 橙色
#FFEFD5 PapayaWhip 番木色/番木瓜
#FFEBCD BlanchedAlmond 白杏色
#FFDEAD NavajoWhite 納瓦白/土著白
#FAEBD7 AntiqueWhite 古董白
#D2B48C Tan 茶色
#DEB887 BurlyWood 硬木色
#FFE4C4 Bisque 陶坯黃
#FF8C00 DarkOrange 深橙色
#FAF0E6 Linen 亞麻布
#CD853F Peru 祕魯色
#FFDAB9 PeachPuff 桃肉色
#F4A460 SandyBrown 沙棕色
#D2691E Chocolate 巧克力色
#8B4513 SaddleBrown 重褐色/馬鞍棕色
#FFF5EE Seashell 海貝殼
#A0522D Sienna 黃土赭色
#FFA07A LightSalmon 淺鮭魚肉色
#FF7F50 Coral 珊瑚
#FF4500 OrangeRed 橙紅色
#E9967A DarkSalmon 深鮮肉/鮭魚色
#FF6347 Tomato 番茄紅
#FFE4E1 MistyRose 淺玫瑰色/薄霧玫瑰
#FA8072 Salmon 鮮肉/鮭魚色
#FFFAFA Snow 雪白色
#F08080 LightCoral 淡珊瑚色
#BC8F8F RosyBrown 玫瑰棕色
#CD5C5C IndianRed 印度紅
#FF0000 Red 純紅
#A52A2A Brown 棕色
#B22222 FireBrick 火磚色/耐火磚
#8B0000 DarkRed 深紅色
#800000 Maroon 栗色
#FFFFFF White 純白
#F5F5F5 WhiteSmoke 白煙
#DCDCDC Gainsboro 淡灰色
#D3D3D3 LightGrey 淺灰色
#C0C0C0 Silver 銀灰色
#A9A9A9 DarkGray 深灰色
#808080 Gray 灰色
#696969 DimGray 暗淡灰
#000000 Black 純黑'''
root = Tk()
i = 0
colcut = 5
for color in colors.split('\n'):
    sp = color.split(' ')
    try:
        Label(text=color, bg=sp[1]).grid(row=int(i/colcut),column=i%colcut, sticky=W+E+N+S)
    except :
        print('err',color)
        Label(text='ERR'+color).grid(row=int(i/colcut),column=i%colcut, sticky=W+E+N+S)
    i += 1
root.mainloop()

