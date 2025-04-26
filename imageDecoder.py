from PIL import Image
def binary_to_password(binary_data, delimiter = "#end#"): #takes the binary password that would be decoded and convert it back into characters to use.
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)] #breaks apart the binary into each character( 8 bit)
    decoded = ''.join(chr(int(char, 2)) for char in chars) #converts the 8 bit into integers, then converts the intergers into characters.
    password = decoded.split(delimiter)[0] #stop at the delimiter we set up, and splits it from the password we just decoded.
    return password

def decode_password_from_image(image_path): #decodes the encoded image, getting up binary data to convert into a password.
    img = Image.open(image_path)
    img = img.convert('RGB')
    width, height = img.size

    return password
