import numpy as np
from PIL import Image
import argparse
import os
import warnings

# Assume the input image is not malicious and disable this warning.
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--InputFile", type=str)
    parser.add_argument("--Slices", type=int)
    args = parser.parse_args()

    input_file_name = args.InputFile
    num_slices = args.Slices

    file_name, file_extension = os.path.splitext(input_file_name)

    image_array = np.asarray(Image.open(input_file_name))

    for slice_index, curr_slice in enumerate(get_slices(image_array, num_slices)):
        Image.fromarray(curr_slice).save(get_file_name(num_slices, file_name, file_extension, slice_index))


def get_slices(image_array, num_slices):
    image_width_pixels = image_array.shape[1]
    validate_before_slicing(num_slices, image_width_pixels)

    slice_width = image_width_pixels // num_slices

    for slice_index in range(num_slices):        
        curr_slice = image_array[:, slice_index * slice_width : (slice_index + 1) * slice_width, :]
        yield curr_slice


def validate_before_slicing(num_slices, image_width_pixels):
    if num_slices < 2:
        raise Exception("The number of slices must be at least two.")

    if num_slices > image_width_pixels:
        raise Exception("The number of slices cannot exceed the width of the image in pixels.")

    if image_width_pixels % num_slices != 0:
        raise Exception(f"The image width ({image_width_pixels}) is not evenly divisible by the requested number of slices ({num_slices}).")


def get_file_name(num_slices, file_name, file_extension, slice_index):
    return f"{file_name}_slice_{slice_index + 1}_of_{num_slices}{file_extension}"


if __name__ == "__main__":
    main()