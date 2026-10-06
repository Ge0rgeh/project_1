import sys
from byuimage import Image

def validate_commands(flag, args):
    """Validates if the format of the input is accurate
    Args: a list of inputs from the command line

    returns a boolean True if the format matches else false
    """
    commands = {"-d":1, "-k":3, "-s":2, "-g":2, "-f":2, "-m":2, "-b":6, "-c":6, "-y":5}
    print(args)
    if flag in commands and len(args) == commands[flag]:
        return True

    return False

def display(filename):
    """
    Displays an image using the native image display
    :param filename: filename of image to display
    :return: None
    """
    image = Image(filename)
    image.show()

    return None

def darken(filename, outfile, percent):
    """
    Darkens an image by a percentage

    Arg: filename: an image file
    Arg: a percentage that is passed

    returns an image darkened by a percentage
    """
    image = Image(filename)
    print("hi")
    percent = float(percent)
    for pixel in image:
        pixel.red *= 1-percent
        pixel.green *= 1-percent
        pixel.blue *= 1-percent

    image.save(outfile)

    return image

def grayscale(filename, outfile):
    """
    Changes an image into black and white

    Arg: an image file is passed in

    returns an image in black and white

    """
    image = Image(filename)
    for pixel in image:
        average = (pixel.red + pixel.green + pixel.blue)/3
        pixel.red = average
        pixel.green = average
        pixel.blue = average
    image.save(outfile)

    return image

def sepia(filename,outfile):
    """
    Filters an image into sepia

    Arg: an image file

    returns an image filtered into sepia
    """
    image = Image(filename)
    for pixel in image:
        true_red = 0.393 * pixel.red +0.769 * pixel.green + 0.189 * pixel.blue
        true_green = 0.349 * pixel.red + 0.686 * pixel.green + 0.168 * pixel.blue
        true_blue = 0.272 * pixel.red + 0.534 * pixel.green + 0.131 * pixel.blue

        pixel.red = true_red
        pixel.green = true_green
        pixel.blue = true_blue

        if pixel.red > 255:
            pixel.red = 255

        elif pixel.green > 255:
            pixel.green = 255

        elif pixel.blue > 255:
            pixel.blue = 255
    image.save(outfile)

    return image

def flipped(filename, outfile):
    """
    Creates a flipped copy of an image

    Arg: passes in an image file

    returns a flipped copy of an image
    """
    image = Image(filename)
    y1 = image.height
    x1 = image.width
    new_image = Image.blank(x1,y1)
    for y in range(0, y1):
        for x in range(0, x1):
            pixel = image.get_pixel(x,y)
            pixel_new = new_image.get_pixel(x,image.height - y - 1)
            pixel_new.red = pixel.red
            pixel_new.green = pixel.green
            pixel_new.blue = pixel.blue
    new_image.save(outfile)

    return new_image

def mirrored(filename, outfile):
    """
   Creates a flipped copy of an image

   Arg: passes in an image file

   returns a flipped copy of an image
   """
    image = Image(filename)
    y1 = image.height
    x1 = image.width
    new_image = Image.blank(x1, y1)
    for y in range(0, y1):
        for x in range(0, x1):
            pixel = image.get_pixel(x, y)
            pixel_new = new_image.get_pixel(image.width-x-1, y)
            pixel_new.red = pixel.red
            pixel_new.green = pixel.green
            pixel_new.blue = pixel.blue
    new_image.save(outfile)

    return new_image

def make_borders(filename, outfile, thickness, red, green, blue):
    """
    Puts a border around an image

    Arg1: filename = image file
    Arg2: Passes in a thickness
    Arg3-5: Passes in rgb color values

    returns an image with borders around it
    """
    thickness, red, green, blue = int(thickness), int(red), int(green), int(blue)

    image = Image(filename)
    y1 = image.height + 2 * thickness
    x1 = image.width + 2 * thickness
    new_image = Image.blank(x1,y1)
    print(red, green, blue)
    for pixel in new_image:
        pixel.red = red
        pixel.blue = blue
        pixel.green = green


    for y in range(image.height):
        for x in range(image.width):
            pixel = image.get_pixel(x,y)
            pixel_new = new_image.get_pixel(x + thickness, y + thickness)
            pixel_new.red = pixel.red
            pixel_new.green = pixel.green
            pixel_new.blue = pixel.blue

    new_image.save(outfile)

    return new_image

def collage(file1, file2, file3, file4, outfile, border_thickness):
    """
    Takes in 4 files and outputs a collage with borders around each image
    :param file1: image1 filepath
    :param file2: image2 filepath
    :param file3: image3 filepath
    :param file4: image4 filepath
    :param outfile: output filepath
    :param border_thickness: how thick the border between images
    :return: collage that was created
    """

    ## Could be a possible off by one error with the last 3 images for x/y
    image1 = Image(file1)
    image2 = Image(file2)
    image3 = Image(file3)
    image4 = Image(file4)

    border_thickness = int(border_thickness)
    new_collage = Image.blank(image1.width + image2.width + border_thickness * 3, image1.height + image2.height + border_thickness * 3)

    for pixel in new_collage:
        pixel.red = 0
        pixel.green = 0
        pixel.blue = 0

    for x1 in range(image1.width):
        for y1 in range(image1.height):
            old_pixel = image1.get_pixel(x1, y1)
            new_pixel = new_collage.get_pixel(x1 + border_thickness, y1 + border_thickness)
            new_pixel.red = old_pixel.red
            new_pixel.green = old_pixel.green
            new_pixel.blue = old_pixel.blue

    for x1 in range(image2.width):
        for y1 in range(image2.height):
            old_pixel = image2.get_pixel(x1, y1)
            new_pixel = new_collage.get_pixel(x1 + border_thickness * 2 + image1.width, y1 + border_thickness)
            new_pixel.red = old_pixel.red
            new_pixel.green = old_pixel.green
            new_pixel.blue = old_pixel.blue

    for x1 in range(image3.width):
        for y1 in range(image3.height):
            old_pixel = image3.get_pixel(x1, y1)
            new_pixel = new_collage.get_pixel(x1 + border_thickness, y1 + border_thickness * 2 + image1.height)
            new_pixel.red = old_pixel.red
            new_pixel.green = old_pixel.green
            new_pixel.blue = old_pixel.blue

    for x1 in range(image4.width):
        for y1 in range(image4.height):
            old_pixel = image4.get_pixel(x1, y1)
            new_pixel = new_collage.get_pixel(x1 + border_thickness * 2 + image1.width, y1 + border_thickness * 2 + image1.height)
            new_pixel.red = old_pixel.red
            new_pixel.green = old_pixel.green
            new_pixel.blue = old_pixel.blue

    new_collage.save(outfile)
    return new_collage

def green_screen(foreground_image_name, background_image_name, outfile, threshold, factor):
    """
    Takes two images and replaces the green screen with the background image
    :param foreground_image_name: filepath to foreground image with greenscreen
    :param background_image_name: filepath to the background image
    :param outfile: filepath to the output file to save
    :param threshold: threshold to detect green pixels
    :param factor: factor to detect green pixels
    :return: the image with the green screen replaced
    """
    foreground_image = Image(foreground_image_name)
    background_image = Image(background_image_name)
    new_image = Image.blank(foreground_image.width, foreground_image.height)

    for x1 in range(new_image.width):
        for y1 in range(new_image.height):
            foreground_pixel = foreground_image.get_pixel(x1, y1)
            background_pixel = background_image.get_pixel(x1, y1)
            new_pixel = new_image.get_pixel(x1, y1)

            if detect_green(foreground_pixel, threshold, factor):
                new_pixel.red = background_pixel.red
                new_pixel.green = background_pixel.green
                new_pixel.blue = background_pixel.blue
            else:
                new_pixel.red = foreground_pixel.red
                new_pixel.green = foreground_pixel.green
                new_pixel.blue = foreground_pixel.blue

    new_image.save(outfile)
    return new_image

def detect_green(pixel, threshold: str, factor: str):
    """
    Detects if a pixel is green based on threshold and factor
    :param pixel: pixel object to check
    :param threshold: threshold to check by
    :param factor: factor to check by
    :return: Boolean if its green or not
    """
    factor = float(factor)
    threshold = int(threshold)
    average = (pixel.red + pixel.green + pixel.blue) / 3
    if (pixel.green >= factor * average) and (pixel.green > threshold):
        return True
    else:
        return False

def main(flag, args):
    if validate_commands(flag, args):
        # here the * symbol unpacks the list so that all args are put in separately
        if flag == '-d':
            display(*args)
        elif flag == '-k':
            darken(*args)
        elif flag == "-g":
            grayscale(*args)
        elif flag == "-s":
            sepia(*args)
        elif flag == "-f":
            flipped(*args)
        elif flag == "-m":
            mirrored(*args)
        elif flag == "-b":
            make_borders(*args)
        elif flag == "-c":
            collage(*args)
        elif flag == "-y":
            green_screen(*args)
        else:
            print('Please input valid arguments.')
    else:
        print('Please input valid arguments.')

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])