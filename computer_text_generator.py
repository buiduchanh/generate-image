import random

from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter

class ComputerTextGenerator(object):
    @classmethod
    def generate(cls, text, font, text_color, font_size):
        #font_size is a height of image
        image_font = ImageFont.truetype(font=font, size=font_size)
        text_width, text_height = image_font.getsize(text)
        
        # ratio = random.uniform(1, 1.5)

        ratio  = random.uniform(1, 1.7)
        default_height = text_height
        text_height  = int(text_height * ratio)

        txt_img = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))

        txt_draw = ImageDraw.Draw(txt_img)

        colors = [ImageColor.getrgb(c) for c in text_color.split(',')]
        c1, c2 = colors[0], colors[-1]
            
        fill = (
            random.randint(c1[0], c2[0]),
            random.randint(c1[1], c2[1]),
            random.randint(c1[2], c2[2])
        )
        
        position = int((text_height - default_height)/2)
        txt_draw.text((0,position), text, fill=fill, font=image_font)

        return txt_img
