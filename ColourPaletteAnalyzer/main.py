import os
import numpy as np
import pandas as pd
from scipy import cluster
import matplotlib.pyplot as plt
from PIL import Image
import math
import colorsys

def get_hex_colour(rgb):
    return '%02x%02x%02x' % rgb

def find_top_rgb(input_file):
    img = plt.imread(input_file)
    red, green, blue = (img[:, :, i].ravel() for i in (0, 1, 2))
    df = pd.DataFrame({
        'red': red,
        'green': green,
        'blue': blue
    })
    red_std, green_std, blue_std = df[['red', 'green', 'blue']].std()
    
    df['red'] = cluster.vq.whiten(df['red'])
    df['green'] = cluster.vq.whiten(df['green'])
    df['blue'] = cluster.vq.whiten(df['blue'])

    color_palette, distortion = cluster.vq.kmeans(df[['red', 'green', 'blue']], 3)

    colors = []
    for color in color_palette:
        scaled_red, scaled_green, scaled_blue = color
        colors.append((
            math.ceil(scaled_red * red_std), 
            math.ceil(scaled_green * green_std), 
            math.ceil(scaled_blue * blue_std), 
        ))
    
    colors.sort(key=lambda x: step(x[0], x[1], x[2], 8))

    return colors

def step(r, g, b, repetitions=1):
    lum = math.sqrt(0.241 * r + 0.691 * g + 0.068 * b)

    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    h2 = int(h * repetitions)
    lum2 = int(lum * repetitions)
    v2 = int(v * repetitions)

    if h2 % 2 == 1:
        v2 = repetitions - v2
        lum = repetitions - lum

    return (h2, lum, v2)

def main():
    

    input_file = "/Users/kanchshres/Desktop/Code Projects/ColourPaletteAnalyzer/ColourPaletteAnalyzer/MeDaniel.jpg"
    top_rgb = find_top_rgb(input_file)
    print("The three most common colours values were:")
    for rgb in top_rgb:
        print(get_hex_colour(rgb), " (", rgb, ")")

main()