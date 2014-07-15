import numpy
from PIL import Image


class WebBasedPreviews:


    def __init__(self,pil_image,center=25,contrast=3):
        self.output_image = None
        self.image = pil_image
        self.gen()
        self.combine(center,contrast)
        
    def gen(self):
        self.level_data = []
        im = self.image.convert("L")
        im = im.resize((200,200),Image.ANTIALIAS)
        w,h = im.size
        im_arr = numpy.asarray(im, numpy.uint8)

        for image in range(51):
            a = (im_arr > (image*(255/50.0))) * 255
            a = numpy.uint8(a)
            self.level_data.append(a)

    def getImage(self):
        return self.output_image

    def combine(self,center=25,contrast=3):

        c = center
        cs = contrast

        levels = [0]
        levels.append(c-cs*3)
        levels.append(c-cs*2)
        levels.append(int(round(c-cs/2.0)))
        levels.append(int(round(c+cs/2.0)))
        levels.append(c+cs*2)
        levels.append(c+cs*3)

        my_level_data = []

        for l in levels:
            my_level_data.append(self.level_data[l])

        a = 0
        counter = 0
        for data in my_level_data:
            ld = (data == 0) *1
            counter += 1
            a = a + ld

        colors = [

            (250,250,250),
            (220,220,220),
            (170,170,170),
            (255,100,100),
            (255,0,0),
            (80,30,30),
            (0,0,0)

        ]

        _r = 0
        _g = 0
        _b = 0
        counter = 0
        for r in levels:
            __r = (a == counter) * colors[counter][0]
            __g = (a == counter) * colors[counter][1]
            __b = (a == counter) * colors[counter][2]

            _r = _r + __r
            _g = _g + __g
            _b = _b + __b

            counter += 1

        a = numpy.dstack((_r,_g,_b))

        a = numpy.uint8(a)
        t = Image.fromarray(a)
        self.output_image = t


if __name__ == "__main__":
    pr = WebBasedPreviews(Image.open("miles.jpg"),25,5)
    im = pr.getImage()
    im.show()




