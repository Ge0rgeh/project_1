import sys
from byuimage import Image


def validate_commands(flag, args):
    """Validates if the format of the input is accurate
    Args: a list of inputs from the command line

    returns a bollean True if the format matches else false
    """
    commands = {"-d":1, "-k":3, "-s":2,"-g":2, "f":2, "m":2, "-b":6, "-c":6, "-y":5}
    if flag in commands and args == commands[flag]:
        return True



def display(filename):
    image = Image(filename)
    new_image = image.blank(image.width,image.height)
    for y in range(image.height):
        for x in range(image.width):
            pixel = image.get_pixel(x,y)
            new_pixel = new_image.get_pixel(x,y)
            new_pixel.red = pixel.red
            new_pixel.green = pixel.green
            new_pixel.blue = pixel.blue

    return new_image


def darken(filename, percent,outfile):
    """
    Darkens an image by a percentage

    Arg: filename: an image file
    Arg: a percentage that is passed

    returns an image darkened by a percentage
    """
    image = Image(filename)
    for pixel in image:
        pixel.red *= 1-percent
        pixel.green *= 1-percent
        pixel.blue *= 1-percent
    image.save(outfile)


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
            pixel_new = new_image.get_pixel(x,y1 - y-1)
            pixel_new.red = pixel.red
            pixel_new.green = pixel.green
            pixel_new.blue = pixel.blue
    image.save(outfile)

def mirrored(filename, outfile):
    ###
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
            pixel_new = new_image.get_pixel(x1-x-1, y)
            pixel_new.red = pixel.red
            pixel_new.green = pixel.green
            pixel_new.blue = pixel.blue
    image.save(outfile)



def make_borders(filename, outfile, thickness, red, green ,blue):
    #####Needs work#####

    """
    Puts a border around an image

    Arg1: filename = image file
    Arg2: Passes in a thickness
    Arg3-5: Passes in rgb color values

    returns an image with borders around it
    """
    image = Image(filename)
    y1 = image.height + 2 * thickness
    x1 = image.width + 2 * thickness
    new_image = Image.blank(x1,y1)

    for pixel in new_image:
        pixel.red = red
        pixel.blue = blue
        pixel.green = green


    for y in range(image.height):
        for x in range(image.width):
            pixel = image.get_pixel(x,y)
            pixel_new = new_image.get_pixel(x + thickness,y + thickness)
            pixel_new.red = pixel.red
            pixel_new.green = pixel.green
            pixel_new.blue = pixel.blue

    image.save(outfile)








def main(flag, args):
    if validate_commands(flag, args):
        if flag == '-d':
            display(args)
        elif flag == 'k':
            darken(args)
        elif flag == "-g":
            grayscale(args)
        elif flag == "-s":
            sepia(args)
        elif flag == "-f":
            flipped(args)
        elif flag == "-m":
            mirrored(args)
    else:
        print('Please input valid arguments')




if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2:])