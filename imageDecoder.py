import cryptocode
from PIL import Image

def binary_to_password(key: str, binary_data: str, delimiter: str = "#end#") -> str: #takes the binary password that would be decoded and convert it back into characters to use.
    #converts binary data into characters
    chars = [chr(int(binary_data[i : i + 8], 2)) for i in range(0, len(binary_data), 8)]
    encrypted = ''.join(chars)
    #since the delimiter was not encrypted, we know where to stop. Split off delimiter from encrypted data
    password = encrypted.split(delimiter)[0]
    #decrypt the password
    decrypted = cryptocode.decrypt(password, key)
    return decrypted

def decode_password_from_image(image: Image.Image): #decodes the encoded image, getting up binary data to convert into a password.
    #opens the image and converts it to RGB format so we can read the pixel RGB values.
    image = image.convert('RGB')

    #gets the pixel data from the image, and inserts it into a list. 
    pixels = list(image.getdata()) 

#from here, with this pixel data, we need to convert to binary, and then read the pixel data for the password.
#after that is done, we will return the pasword.
    
    #flattens the pixel data into a single list. (R, G, B ,R, G, B, R, G, B...)
    #we can take this logic and apply it to the encoding function here.
    flattened_pixels = [] 
    for r, g, b in pixels:
        flattened_pixels.extend([format(r, '08b'), format(g, '08b'), format(b, '08b')]) 

    #take the lsb of each pixel, and then combine them into a single string.
    binary_data = []
    for pixel in flattened_pixels:
        lsb = int(pixel[-1]) 
        binary_data.append(str(lsb))
    binary_data_string = ''.join(binary_data) #this will combine the binary data into a single string.

    #with this data, we can then convert it back into a password.
    password = binary_to_password("fortnite", binary_data_string) #this here will convert the binary data into a password until it hits the delimiter.
    #return the password we decoded from the image. 
    return password
