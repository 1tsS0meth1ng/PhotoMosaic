from random import randint

import copy
from PIL import Image
from src.ImagePool import ImagePool
from threading import Thread


class Chromosome:
    fitnessVal = 0
    def __init__(self):
        self.fitnessVal = 0

    def getFitnessVal(self):
        return self.fitnessVal

    def setFitnessVal(self, newFitness):
        self.fitnessVal = newFitness

class ImageChromosome(Chromosome):

    image = 0
    fitnessVal = 0

    def __init__(self):
        imagePool=ImagePool()
        self.image=[[0 for x in range(imagePool._xVal)] for y in range(imagePool._yVal)]
        Chromosome.__init__(self)

    def random(self):
        imagePool=ImagePool()
        print("Generating chromosome")
        count=0
        imagesUsed=[]
        imagesToUse=list(range(0,len(imagePool._images)))
        for x in range(imagePool._xVal):
            for y in range(imagePool._yVal):
                if len(imagesUsed)==len(imagePool._images):
                    imagesToUse=imagesUsed
                    imagesUsed=[]
                val=randint(0, len(imagesToUse) - 1)
                self.image[y][x] = val
                imagesUsed.append(val)
                count += 1

    def getFitnessVal(self):
        return self.fitnessVal

    def createImage(self):
        imagePool = ImagePool()
        image = Image.new("RGB", (imagePool._xVal*int(imagePool._originalImage.width/imagePool._xVal),imagePool._yVal*int(imagePool._originalImage.height/imagePool._yVal)))
        threads = []
        x_width = int(imagePool._originalImage.width/imagePool._xVal)
        y_height = int(imagePool._originalImage.height/imagePool._yVal)
        divVal = 100

        if imagePool._xVal > imagePool._yVal:
            xMod = divmod(imagePool._xVal, divVal)
            while xMod[0] <= 5:
                divVal = int(divVal/2)
                xMod = divmod(imagePool._xVal, divVal)
            print(xMod[0]/imagePool._xVal)
            for i in range(xMod[0]):
                threads.append(Thread(target=self.image_builder, args=(
                    imagePool, self.image, image, i * int(imagePool._xVal/xMod[0]), x_width,
                    int(imagePool._xVal / xMod[0]), 0, y_height, imagePool._yVal)))
            if xMod[1] > 0:
                leftOver = imagePool._xVal - int(int(imagePool._xVal / xMod[0]) * xMod[0])
                threads.append(Thread(target=self.image_builder, args=(
                    imagePool, self.image, image, (i+1) * int(imagePool._xVal / xMod[0]), x_width,
                    leftOver, 0, y_height, imagePool._yVal)))
        else:
            yMod = divmod(imagePool._yVal, divVal)
            while yMod[0] <= 5:
                divVal = int(divVal / 2)
                yMod = divmod(imagePool._yVal, divVal)
            for j in range(int(yMod[0])):
                threads.append(Thread(target=self.image_builder, args=(
                    imagePool, self.image, image, 0, x_width, imagePool._xVal, j * int(imagePool._yVal / yMod[0]),
                    y_height, int(imagePool._yVal / yMod[0]))))
            if yMod[1] > 0:
                leftOver = imagePool._yVal - int(int(imagePool._yVal / yMod[0]) * yMod[0])
                threads.append(Thread(target=self.image_builder, args=(
                    imagePool, self.image, image, 0, x_width, imagePool._xVal, (j+1) * int(imagePool._yVal / yMod[0]),
                    y_height, leftOver)))

        for t in threads:
            t.start()

        for t in threads:
            t.join()
        return image

    def image_builder(self, image_pool, image_arr, image, x_point, x_size, x_number, y_point, y_size, y_number):
        i = 0
        for x in range(x_number):
            for y in range(y_number):
                pst = image_pool.getImage(image_arr[y+y_point][x+x_point])
                image.paste(pst, ((x+x_point)*x_size, (y+y_point)*y_size))
                pst.close()
                i += 1



    def calculateFitness(self):
        imagePool = ImagePool();
        overAllFitness=0
        for x in range(imagePool._xVal):
            for y in range(imagePool._yVal):
                total=self.getFitnessForBlock(x,y)
                overAllFitness+=total
        self.setFitnessVal(overAllFitness)

    def crossOver(self, other):
        child1 = ImageChromosome()
        child2 = ImageChromosome()
        imagePool = ImagePool()
        if randint(0,1)==0:
            swapVal = randint(1, imagePool._xVal - 2)
            for x in range(imagePool._xVal):
                for y in range(imagePool._yVal):
                    if x >= swapVal:
                        child1.image[y][x] = self.image[y][x]
                    else:
                        child1.image[y][x] = other.image[y][x]

            for x in range(imagePool._xVal):
                for y in range(imagePool._yVal):
                    if x <= swapVal:
                        child2.image[y][x] = self.image[y][x]
                    else:
                        child2.image[y][x] = other.image[y][x]
        else:
            swapVal = randint(1, imagePool._yVal-2)
            for x in range(imagePool._xVal):
                for y in range(imagePool._yVal):
                    if y >= swapVal:
                        child1.image[y][x] = self.image[y][x]
                    else:
                        child1.image[y][x] = other.image[y][x]

            for x in range(imagePool._xVal):
                for y in range(imagePool._yVal):
                    if y <= swapVal:
                        child2.image[y][x] = self.image[y][x]
                    else:
                        child2.image[y][x] = other.image[y][x]
        child1.calculateFitness()
        child2.calculateFitness()
        return child1,child2

    def getFitnessForBlock(self, x,y):
        imagePool=ImagePool()
        orR, orG, orB = imagePool._originalRGB[y][x]
        tmpR = imagePool._aveRed[self.image[y][x]]
        tmpG = imagePool._aveGreen[self.image[y][x]]
        tmpB = imagePool._aveBlue[self.image[y][x]]
        changeRed = (tmpR - orR) ** 2
        changeGreen = (tmpG - orG) ** 2
        changeBlue = (tmpB - orB) ** 2
        total = (changeRed + changeBlue + changeGreen) ** 0.5
        return total

    def mutation(self):
        imagePool = ImagePool()
        newImg = copy.deepcopy(self)
        xVal=randint(0, imagePool._xVal - 1)
        yVal=randint(0, imagePool._yVal - 1)
        valsCantUse=[]
        valsCantUse.append(newImg.image[yVal][xVal])
        prevFitness=newImg.getFitnessForBlock(xVal,yVal)

        newVal=randint(0, len(imagePool._images) - 1)
        while valsCantUse.__contains__(newVal):
            newVal = randint(0, len(imagePool._images) - 1)
        newImg.image[yVal][xVal] =newVal
        newImg.calculateFitness()
        return newImg

    def twoPointCrossover(self, other):
        child1=ImageChromosome()
        child2=ImageChromosome()
        imagePool= ImagePool()

        if randint(0,1)==0:
            large = randint(1, imagePool._xVal)
            small = randint(int(large/2),large-1)

            for x in range(imagePool._xVal):
                for y in range(imagePool._yVal):
                    if x >= small and x<=large:
                        child1.image[y][x] = self.image[y][x]
                        child2.image[y][x] = other.image[y][x]
                    else:
                        child1.image[y][x] = other.image[y][x]
                        child2.image[y][x] = self.image[y][x]

        else:
            large = randint(1,imagePool._yVal)
            small = randint(int(large/2),large-1)

            for x in range(imagePool._xVal):
                for y in range(imagePool._yVal):
                    if y >= small and y<=large:
                        child1.image[y][x] = self.image[y][x]
                        child2.image[y][x] = other.image[y][x]
                    else:
                        child1.image[y][x] = other.image[y][x]
                        child2.image[y][x] = self.image[y][x]

        child1.calculateFitness()
        child2.calculateFitness()
        return child1,child2