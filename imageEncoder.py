from PIL import Image
import cryptocode

def password_to_binary(key: str, password: str, delimiter: str = "#end#") -> str:
    # encrypt the password with a key
    encoded = cryptocode.encrypt(password, key)
    #convert the password and delimiter to binary
    password = ''.join(format(ord(char), '08b') for char in encoded)
    delimiter_binary = ''.join(format(ord(char), '08b') for char in delimiter)
    #combine the two and return it
    full_password = password + delimiter_binary
    return full_password

def encode_password_in_image(image: Image.Image, password: str, output_path: str): #this will take in a password input, an image, and encode the picture, and create a new image.
    #opens the image and converts it to RGB format so we can read the pixel RGB values.
    image = image.convert('RGB')

    #converts the password into binary format.
    binary_password: str = password_to_binary("!T&*(EIUGHy8fdihd89oj3g8g3@UHGYGg2786f<L:W<:ldl;,,.;LOKEOPJO#p)", password)

    #find width and height of the image, so we can calculate the maximum capacity of the image.
    width, height = image.size
    #calculates the maximum capacity of the image, bc we can modify both the red, green, and blue values of each pixel, we multiply by 3. 
    max_capacity = width * height * 3 

    #checks if password is too big for the image. sends error message and returns if it is. 
    if len(binary_password) > max_capacity: 
        print("Password is too big for the image.")
        return
    #gets the pixel data from the image, and inserts it into a list. 
    pixels = list(image.getdata()) 

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
        flattened_pixels[i] = flattened_pixels[i][:-1] + binary_password[i] #this will replace the last bit of the pixel data with the bit from the password.

    #we reformat the pixel data back into RGB values so that we can create a new image with the modified pixel data.
    modded_pixels = [tuple(int(flattened_pixels[i + j], 2) for j in range(3)) for i in range(0, len(flattened_pixels), 3)] 

    #creates new image with the modified pixel data and saves it to the output path.
    new_image = Image.new(image.mode, image.size)
    new_image.putdata(modded_pixels) 
    new_image.save(output_path)

