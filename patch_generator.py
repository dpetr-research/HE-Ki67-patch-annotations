import os
import PIL.Image
import numpy as np
import lxml
from patchify import patchify
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt

if __name__ == '__main__':
    PIL.Image.MAX_IMAGE_PIXELS = 3283937636
    HE_output_directory = ""
    IHC_output_directory = ""
    images_directory = ""
    annotations_directory = ""
    
    annotations = os.listdir(annotations_directory)
    slides = os.listdir(images_directory)
    
    for xml_file in annotations:
        pair_id = xml_file.split('_')[0]
        HE_slide = [i for i in slides if pair_id + "_HE" in i][0]
        IHC_slide = [i for i in slides if pair_id + "_Ki67" in i][0]
        HE_img = PIL.Image.open(images_directory + HE_slide)
        IHC_img = PIL.Image.open(images_directory + IHC_slide)
        # Convert the image to RGB
        HE_img = HE_img.convert('RGB')
        IHC_img = IHC_img.convert('RGB')
        #Convert the image into numpy array for processing
        HE_img_np = np.array(HE_img)
        IHC_img_np = np.array(IHC_img)
        HE_patches = patchify(HE_img_np, (224, 224, 3), step=224)
        IHC_patches = patchify(IHC_img_np, (224, 224, 3), step=224)
        
        with open(annotations_directory + xml_file, 'r') as f:
            data = f.read()

        xml_data = BeautifulSoup(data, "xml")
        patch_annotations = xml_data.find_all("patch")
        count = 0
        for patch_label in patch_annotations:
            x = patch_label['x']
            y = patch_label['y']

            count += 1
            print("Processing annotation number " + count)

            row = int(int(y) / 224)
            col = int(int(x) / 224)

            HE_patch = HE_patches[row][col][0]
            IHC_patch = IHC_patches[row][col][0]

            ratio = patch_label['ki67']
            plt.imsave(HE_output_directory + HE_slide + "-" + str(col * 224) + "-" + str(
                row * 224) + "-" + ratio + ".png", HE_patch)
            plt.imsave(IHC_output_directory + IHC_slide + "-" + str(col * 224) + "-" + str(
                row * 224) + "-" + ratio + ".png", IHC_patch)
