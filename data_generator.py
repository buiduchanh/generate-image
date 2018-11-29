import os
import random
import cv2
import numpy as np

from PIL import Image, ImageFilter

from computer_text_generator import ComputerTextGenerator
# try:
from handwritten_text_generator import HandwrittenTextGenerator
# except ImportError as e:
#     print('Missing modules for handwritten text generation.')
from background_generator import BackgroundGenerator
from distorsion_generator import DistorsionGenerator

from utils.augumentor import BatchGenerator

class FakeTextDataGenerator(object):
    @classmethod
    def generate_from_tuple(cls, t):
        """
            Same as generate, but takes all parameters as one tuple
        """

        cls.generate(*t)

    @classmethod
    def generate(cls, index, name, text, font, out_dir, height, extension, skewing_angle, random_skew, blur, random_blur, background_type, distorsion_type, distorsion_orientation, is_handwritten, name_format, width, alignment, text_color):
        image = None
        ##########################
        # Create picture of text #
        ##########################
        if font == 'error':
            return

        if is_handwritten:
            image = HandwrittenTextGenerator.generate(text)
        else:
            image = ComputerTextGenerator.generate(text, font, text_color, height)
        
        open_cv_image = np.array(image) 
        image = open_cv_image[:, :, ::-1].copy() 

        im_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        color_img = cv2.cvtColor(im_bw, cv2.COLOR_GRAY2RGB)

        generator = BatchGenerator()
        final_image = generator.aug_image(color_img)

        
        image_name = '{}'.format(name)
        
        with open ('texts/newadd.txt', 'a') as f_ :
            f_.writelines('{} {}'.format(name ,text) + '\n')
        f_.close()

        with open('texts/generate.log', 'a') as log:
            log.writelines('{} {}'.format(index , text) + '\n' )

        # Save the image
        # final_image.convert('RGB').save(os.path.join(out_dir, image_name))
        cv2.imwrite(os.path.join(out_dir, image_name), final_image)
