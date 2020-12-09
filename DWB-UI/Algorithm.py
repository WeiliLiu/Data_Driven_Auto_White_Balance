import cv2 as cv
import numpy as np

class ProcessAlgorithm():
    def __init__(self):
        pass

    def gasuss_noise(self, image, mean, var):
        # add gaussian noise into the image
        image = np.array(image, dtype=float)
        image = image/255.0
        noise = np.random.normal(mean, var ** 0.5, image.shape)
        out = image + noise
        if out.min() < 0:
            low_clip = -1.
        else:
            low_clip = 0.
        out = np.clip(out, low_clip, 1.0)
        out = np.uint8(out*255)
        #cv.imshow("gasuss", out)
        return out

if __name__ == "__main__":
    process = ProcessAlgorithm()
    