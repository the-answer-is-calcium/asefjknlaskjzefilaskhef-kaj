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
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def crossfade(original_image_name,overlay_image_name):
    #Get images initialized
    original_image=PIL.Image.open(original_image_name)
    overlay_image=PIL.Image.open(overlay_image_name)
    #Resizes overlay image to match the original image
    overlay_image_resized=overlay_image.resize(original_image.size)
    
    #Make the images into a list of tuples of RGB values
    list_of_pixels_original = list(original_image.getdata())
    list_of_pixels_overlay = list(overlay_image_resized.getdata())
    
    #Will it blend? That is the question...
    list_of_pixels_new=[]
    if original_image.size[0]%2==0:
        #If the width is even (this extra stuff removes vertical scanlines that will show up)
        #NOTE: Using element from size instead of direct width/height until I figure out the correct order to do stuff in
        for i in xrange(original_image.size[1]):
            
            #Alternates which image starts first each line
            if i%2==0:
                for n in xrange(original_image.size[0]*i,original_image.size[0]*(i+1)):
                    if n%2==0:
                        list_of_pixels_new.append(list_of_pixels_original[n])
                    else:
                        list_of_pixels_new.append(list_of_pixels_overlay[n])
            
            else:
                for n in xrange(original_image.size[0]*i,original_image.size[0]*(i+1)):
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
    #Closes images for memory reasons
    original_image.close()
    overlay_image.close()
    overlay_image_resized.close()
   #NOTE: image.blend is the built in function for crossfading