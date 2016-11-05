import os
import platform

file_path = os.path.realpath(__file__)
spl = file_path.split("/")
base_dir = "/".join(spl[:-2])

LIB_PATH = base_dir + "/"
DATA_PATH = LIB_PATH + "data/"