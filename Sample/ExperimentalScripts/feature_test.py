import os
import numpy as np

def get_images():
    images_list = os.listdir("Images/")
    labels_list = [x[0:-5] for x in os.listdir("Labels/")]
    todo_list = [x for x in images_list if x not in labels_list]
    return todo_list


get_images()