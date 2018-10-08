from PIL import ImageStat
from PIL import Image

class Singleton(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

class ImagePool(object, metaclass = Singleton):

    _originalImage = None
    # _images stores locations of images
    _images = 0
    _aveRed = 0
    _aveGreen = 0
    _aveBlue = 0
    _yVal = 0
    _xVal = 0
    _originalRGB = []

    def __init__(self, originalImage, xVal, yVal):

        self._images = []
        self._aveRed = []
        self._aveGreen = []
        self._aveBlue = []
        self._originalImage=originalImage
        self._xVal=xVal
        self._yVal=yVal
        self._originalRGB = [[0 for x in range(self._xVal)] for y in range(self._yVal)]
        self.calcOriginalRGB()

    def calcOriginalRGB(self):
        for x in range(self._xVal):
            for y in range(self._yVal):
                x1=x*int(self._originalImage.width / self._xVal)
                y1=y*int(self._originalImage.height/self._yVal)
                x2=x1+int(self._originalImage.width / self._xVal)
                y2=y1+int(self._originalImage.height/self._yVal)
                tmp = self._originalImage.crop((x1,y1,x2,y2))
                stat = ImageStat.Stat(tmp)
                self._originalRGB[y][x] = stat.mean

    def add(self, image):
        openImage = Image.open(image)
        stat = ImageStat.Stat(openImage)
        r = 0
        b = 0
        g = 0
        try:
            r, g, b = stat.mean
        except:
            print("Image could not open")
        if r != 0 and b != 0 and g != 0:
            self._aveRed.append(r)
            self._aveGreen.append(g)
            self._aveBlue.append(b)
            self._images.append(image)
        openImage.close()

    def setOriginalImage(self, originalImage):
        self._originalImage = originalImage

    def getImage(self, index):
        openImage = Image.open(self._images[index])
        openImage = openImage.resize((int(self._originalImage.width/self._xVal), int(self._originalImage.height/self._yVal)))
        return openImage
