import PIL
import matplotlib.pyplot as plt # single use of plt is commented out
import os.path  
import PIL.ImageDraw
import math            

directory = os.getcwd()

image_list = [] # Initialize aggregaotrs
file_list = []

directory_list=os.listdir(directory)
for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            image_list += [image]
        except IOError:
            pass # do nothing with errors tying to open non-images
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def crossfade(original_image_name,overlay_image_name):
    #Get images initialized
    original_image=PIL.Image.open(original_image_name)
    overlay_image=PIL.Image.open(overlay_image_name)
    overlay_image_resized=overlay_image.resize(original_image.size)
    
    #Make the images into a list of tuples
    list_of_pixels_original = list(original_image.getdata())
    list_of_pixels_overlay = list(overlay_image_resized.getdata())
    
    #Will it blend? That is the question...
    list_of_pixels_new=[]
    if original_image.size[0]%2==0:
        #If the width is even (this extra stuff removes vertical scanlines that will show up)
        counter=0
        for i in xrange(original_image.size[1]):
            
            if i%2==0:#Alternates which image starts first each line
                for n in xrange(original_image.size[0]):
                    if n%2==0:
                        list_of_pixels_new.append(list_of_pixels_original[n])
                    else:
                        list_of_pixels_new.append(list_of_pixels_overlay[n])
            
            else:
                for n in xrange(original_image.size[0]):
                    if n%2==0:
                        list_of_pixels_new.append(list_of_pixels_overlay[n])
                    else:
                        list_of_pixels_new.append(list_of_pixels_original[n])
                        
    else:#Regular, faster algorithm
        for n in xrange(original_image.size[0]*original_image.size[1]):
            if n%2==0:
                list_of_pixels_new.append(list_of_pixels_original[n])
            else:
                list_of_pixels_new.append(list_of_pixels_overlay[n])
    #Return the blended image
    working_image=PIL.Image.new('RGB',original_image.size,(0,0,0))
    working_image.putdata(list_of_pixels_new)
    working_image.save('blended_image.jpg')
    original_image.close()
    overlay_image.close()
    overlay_image_resized.close()
   #image.blend
def round_corners_one_image(original_image, percent_of_side=.3):
    """ Rounds the corner of a PIL.Image
    
    original_image must be a PIL.Image
    Returns a new PIL.Image with rounded corners, where
    0 < percent_of_side < 1
    is the corner radius as a portion of the shorter dimension of original_image
    """
    #set the radius of the rounded corners
    width, height = original_image.size
    radius = int(percent_of_side * min(width, height)) # radius in pixels
    
    ###
    #create a mask
    ###
    
    #start with transparent mask
    rounded_mask = PIL.Image.new('RGBA', (width, height), (127,0,127,0))
    drawing_layer = PIL.ImageDraw.Draw(rounded_mask)
    
    # Overwrite the RGBA values with A=255.
    # The 127 for RGB values was used merely for visualizing the mask
    
    # Draw two rectangles to fill interior with opaqueness
    drawing_layer.polygon([(radius,0),(width-radius,0),
                            (width-radius,height),(radius,height)],
                            fill=(127,0,127,255))
    drawing_layer.polygon([(0,radius),(width,radius),
                            (width,height-radius),(0,height-radius)],
                            fill=(127,0,127,255))

    #Draw four filled circles of opaqueness
    drawing_layer.ellipse((0,0, 2*radius, 2*radius), 
                            fill=(0,127,127,255)) #top left
    drawing_layer.ellipse((width-2*radius, 0, width,2*radius), 
                            fill=(0,127,127,255)) #top right
    drawing_layer.ellipse((0,height-2*radius,  2*radius,height), 
                            fill=(0,127,127,255)) #bottom left
    drawing_layer.ellipse((width-2*radius, height-2*radius, width, height), 
                            fill=(0,127,127,255)) #bottom right
                         
    # Uncomment the following line to show the mask
    # plt.imshow(rounded_mask)
    
    # Make the new image, starting with all transparent
    result = PIL.Image.new('RGBA', original_image.size, (0,0,0,0))
    result.paste(original_image, (0,0), mask=rounded_mask)
    return result
    
def get_images(directory=None):
    """ Returns PIL.Image objects for all the images in directory.
    
    If directory is not specified, uses current directory.
    Returns a 2-tuple containing 
    a list with a  PIL.Image object for each image file in root_directory, and
    a list with a string filename for each image file in root_directory
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    image_list = [] # Initialize aggregaotrs
    file_list = []
    
    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            image_list += [image]
        except IOError:
            pass # do nothing with errors tying to open non-images
    return image_list, file_list

def round_corners_of_all_images(directory=None):
    """ Saves a modfied version of each image in directory.
    
    Uses current directory if no directory is specified. 
    Places images in subdirectory 'modified', creating it if it does not exist.
    New image files are of type PNG and have transparent rounded corners.
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    # Create a new directory 'modified'
    new_directory = os.path.join(directory, 'modified')
    try:
        os.mkdir(new_directory)
    except OSError:
        pass # if the directory already exists, proceed  
    
    # Load all the images
    image_list, file_list = get_images(directory)  

    # Go through the images and save modified versions
    for n in range(len(image_list)):
        # Parse the filename
        print n
        filename, filetype = os.path.splitext(file_list[n])
        
        # Round the corners with default percent of radius
        curr_image = image_list[n]
        new_image = round_corners_one_image(curr_image) 
        
        # Save the altered image, suing PNG to retain transparency
        new_image_filename = os.path.join(new_directory, filename + '.png')
        new_image.save(new_image_filename)    
