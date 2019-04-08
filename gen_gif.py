from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from numpy import load, array, append
import os


def npy_list_sorted():
    return sorted(os.listdir('library/'), key=lambda x: os.path.getmtime('library/' + x))


def main():
    frames = []

    # font = TTFont("/home/fenchelfen/.local/share/Steam/clientui/fonts/Montserrat-Light.ttf")

    k = 0
    p = 0
    files_n = len(os.listdir('library/'))
    for filename in npy_list_sorted():
        print(filename)
        if k % 25 == 0 or k >= files_n - 20:
            p += 1
            im = Image.fromarray(load('library/' + filename))
            draw = ImageDraw.Draw(im)
            # font = ImageFont.truetype(font, size=9)
            draw.text((0, 0), 'IU_' + str(k), (255, 255, 255))
            frames.append(im)
        k += 1

    if frames:
        print(files_n)

        print(p)

        frames[1].save('yvette_tweet.gif',
                       save_all=True,
                       append_images=(frames[2:] + frames[::-2]),
                       duration=1,
                       loop=0)


if __name__ == '__main__':
    main()
