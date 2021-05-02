from PIL import Image, ImageStat
import os
import shutil

# full white photo - 255.0
# full black photo - 0.0


class ImageSelection:
    def __init__(self, path):
        self.path = path

    def brightness_check(self, image):
        '''count function to set value of brightness, 0 - full black, 100 - full bright'''
        with Image.open(image).convert("L") as img:
            z = ImageStat.Stat(img)
            stat = 100*(255-z.mean[0])/255
        return int(stat)

    def averange_threshold(self, dictionary, img_list):
        '''counts thrshold which is RMS of all images value'''
        sum = 0
        for value in dictionary.values():
            sum += value
        return int(sum/len(img_list))

    def image_analysis(self):
        '''execution of class, creates two folders (bright, dark) in path
           to images name is added theior value of brightness'''
        img_list = os.listdir(self.path)
        img_list = [os.path.join(self.path,elem) for elem in img_list]
        extend_set = {".png", ".jpeg", ".jpg"}
        dictionary = {os.path.basename(img): ImageSelection.brightness_check(self, img) for ext in extend_set for img in img_list if ext in img}
        threshold = ImageSelection.averange_threshold(self, dictionary, img_list)
        for key, value in dictionary.items():
            if value < threshold:
                os.makedirs(os.path.join(self.path, "bright"), exist_ok=True)
                shutil.copy(os.path.join(self.path,key), os.path.join(self.path, "bright", key[:key.index(".")] + "_" + str(value) + key[key.index("."):]))
            else:
                os.makedirs(os.path.join(self.path, "dark"), exist_ok=True)
                shutil.copy(os.path.join(self.path,key), os.path.join(self.path, "dark", key[:key.index(".")] + "_" + str(value) + key[key.index("."):]))


path = r"D:\Programy\z.programowanie\learning\to be sorted"
a = ImageSelection(path)
a.image_analysis()
