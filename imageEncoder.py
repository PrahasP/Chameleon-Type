from PIL import Image

def password_to_binary(password, delimiter = "#end#"):
    # Converts the password to binary, with a delimiter to mark the end
    full_text = password + delimiter
    #converts the new text into binary and returns it. 
    return ''.join(format(ord(char), '08b') for char in full_text) 

def encode_password_in_image(image_path, password, output_path): #this will take in a password input, an image, and encode the picture, and create a new image.
    #opens the image and converts it to RGB format so we can read the pixel RGB values.
    img = Image.open(image_path).convert('RGB') 
    #converts the password into binary format.
    binary_password = password_to_binary(password) 

    #find width and height of the image, so we can calculate the maximum capacity of the image.
    width, height = img.size()
    #calculates the maximum capacity of the image, bc we can modify both the red, green, and blue values of each pixel, we multiply by 3. 
    max_capacity = width * height * 3 

    #checks if password is too big for the image. sends error message and returns if it is. 
    if len(binary_password) > max_capacity: 
        print("Password is too big for the image.")
        return
    #gets the pixel data from the image, and inserts it into a list. 
    pixels = list(img.getdata()) 

#from here, with this pixel data, we need to convert to binary, and then modify the pixel data with the password.
#after that is done, we will create a new image with the modified pixel data. 
#we only need to loop through the length of the password, since we are only modifying the pixel data for the length of the password. (includes delimiter)
    
    #flattens the pixel data into a single list. (R, G, B ,R, G, B, R, G, B...)
    flattened_pixels = [] 
    for r, g, b in pixels:
        flattened_pixels.extend([format(r, '08b'), format(g, '08b'), format(b, '08b')]) 

    #for each bit in the binary password, we will modify the pixel data.
    # we do this by taking the last one of the pixel data, and replacing it with the bit from the password.
    for i in range(len(binary_password)): 
        current_pixel_bin = flattened_pixels[i] 
        new_pixel_bin = current_pixel_bin[:-1] + binary_password[i] 
        flattened_pixels[i] = new_pixel_bin
    #creates a new image with the modified pixel data.
    modded_pixels = [tuple(flattened_pixels[i:i + 3]) for i in range(0, len(flattened_pixels), 3)] 

    #creates new image with the modified pixel data and saves it to the output path.
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(modded_pixels) 
    new_img.save(output_path)
