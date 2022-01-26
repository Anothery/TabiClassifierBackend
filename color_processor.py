import colorsys
import cv2
from PIL import Image
import libs.webcolors as webcolors
import numpy as np
from libs.colorgroups import ColorGroups
from math import sqrt


def get_color_group(color_name):
    for(color_group, colors) in ColorGroups.items():
        if(color_name in colors): return color_group
    raise ValueError('No color group found for the requested color')


def get_colors(image_file, numcolors=150):
    paletted = image_file.convert('P', palette=Image.ADAPTIVE, colors=numcolors)

    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    colors = list()
    for i in range(min(numcolors, len(color_counts))):
        palette_index = color_counts[i][1]
        dominant_color = palette[palette_index*3:palette_index*3+3]
        colors.append(tuple(dominant_color))

    return colors


def closest_color(requested_color):
    min_colors = {}
    for key, value in webcolors.CSS3_NAMES_TO_HEX.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(value)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[rd + gd + bd] = key
    return min_colors[min(min_colors.keys())]


def get_dominant_colors_palette(image):
    palette = get_colors(image) 
    colors_response = dict()
    for p in palette:
        try:
            closest_color_name = closest_color(p)
            #closest_color_hex = webcolors.name_to_hex(closest_color_name)
            color_group = get_color_group(closest_color_name).lower()
            
            if color_group in colors_response:
                colors_response[color_group]['percentage'] += 1/len(palette)
                colors_response[color_group]['colors'].append(p)
            else:
                colors_response[color_group] = { 'percentage' : 0 + 1/len(palette), 'colors': [p]}
        except Exception:
           continue

    colors_final = []
    
    for group, colordict in colors_response.items():
        # Getting the mean color from colors array
        rgb_mean = np.mean(colordict['colors'], axis=0).astype(int)
        colordict['meanHexColor'] = '#%02x%02x%02x' % (rgb_mean[0],rgb_mean[1], rgb_mean[2])
        # Colors array is useless now so remove it
        colordict.pop('colors', None)  
        colordict['percentage'] = round(colordict['percentage'], 2)
        colordict['name'] = group
        colors_final.append(colordict)
 
    return colors_final


#def most_common(lst):
#    return max(set(lst), key=lst.count)

# def get_color_category(r,g,b):
#     hsv = colorsys.rgb_to_hsv(r/255,g/255,b/255)
#     hue, sat, lgt = round(hsv[0]*360), round(hsv[1]*100), round(hsv[2]*100)

#     if(lgt <= 20): return Colors.BLACK
#     if(lgt >= 90 and sat <= 10): return Colors.WHITE
#     if(sat < 15): return Colors.GRAY

#     if((hue <= 10 or hue >= 340) and sat <= 50 and lgt >= 90): return Colors.PINK
#     if(20 <= hue <= 35 and lgt < 70): return Colors.BROWN
#     if(25 <= hue <= 35 and lgt >= 70): return Colors.ORANGE
#     if(25 <= hue <= 70 and sat <= 30 and lgt >= 70): return Colors.BEIGE

#     if(hue < 30): return Colors.RED
#     if(hue < 85): return Colors.YELLOW
#     if(hue < 150): return Colors.GREEN
#     if(hue < 190): return Colors.CYAN
#     if(hue < 265): return Colors.BLUE
#     if(hue < 330): return Colors.VIOLET
#     return Colors.RED