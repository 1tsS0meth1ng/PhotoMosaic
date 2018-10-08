import glob
from random import randint

from src.ImagePool import ImagePool


class ImageDirectoryHandler:
    imgList = []
    originalImage = 0
    _xVal = 0
    _yVal = 0

    def __init__(self, dir, originalImage, xVal, yVal):
        dir += "*.jpg"
        self._xVal = xVal
        self._yVal = yVal
        self.originalImage = originalImage
        print(dir)
        for tmp in glob.glob(dir):
            print(tmp)
            self.imgList.append(tmp)
        self.setUpImagePool()

    def getModifiedImgList(self):
        return self.imgList

    def getRandomImage(self):
        return self.imgList[randint(0, self.imgList.__sizeof__()-1)]

    def getImgListSize(self):
        return len(self.imgList)

    def setUpImagePool(self):
        ret = ImagePool(self.originalImage, self._xVal, self._yVal)
        for i in self.imgList:
            ret.add(i)
