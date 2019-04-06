from PIL import Image, ImageDraw, ImageFont
from numpy import load, array, append
import os


def npy_list_sorted():
    return sorted(os.listdir('library/'), key=lambda x: os.path.getmtime('library/' + x))


def main():
    frames = []

    k = 0
    for filename in npy_list_sorted():
        print(filename)
        if k < 32 or k % 2500 == 0 or (k > 20000 and k % 250 == 0):
            im = Image.fromarray(load('library/' + filename))
            draw = ImageDraw.Draw(im)
            # font = ImageFont.truetype("sans-serif.ttf", 9)
            draw.text((0, 0), 'delta_' + filename.split('_')[3].split('npy')[0] + '\n' + str(k), (255, 255, 255))
            frames.append(im)
        k += 1

    # reversed = deepcopy(frames)
    # reversed.reverse()

    if frames:
        print(len(os.listdir('library/')))
        frames[0].save('ryder.gif',
                       save_all=True,
                       append_images=(frames[1:]),
                       duration=10,
                       loop=0)


if __name__ == '__main__':
    main()
