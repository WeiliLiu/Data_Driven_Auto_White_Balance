import cv2 as cv
import numpy as np
import math

class EvaluationParameter():
    def __init__(self):
        self.pixel_const = 256
        self.pixel_bit_list = range(0, self.pixel_const)

    #Otsu threshold
    def otsu(self, frame):
        img_gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
        ret, th = cv.threshold(img_gray,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
        return th
    
    #Peak Signal to Noise Ratio，PSNR
    def PSNR(self, input_frame, gdth_frame):
        mse = np.mean((input_frame/255.0 - gdth_frame/255.0) ** 2)
        return 20 * math.log10(1.0 / math.sqrt(mse))


def main():
    eval_tools = EvaluationParameter()
    img_path = "./icons/default1.jpg"
    img = cv.imread(img_path)
    psnr_value = eval_tools.PSNR(img1, img2)
    print("psnr value = {}".format(psnr_value))

if __name__ == "__main__":
    main()