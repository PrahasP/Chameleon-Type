from PIL import Image

def password_to_binary(password, delimiter ="#end#"):
    # Converts the password to binary, with a delimiter to mark the end
    full_text = password + delimiter
    return ''.join(format(ord(char), '08b') for char in full_text) #converts the new text into binary.
def encode_password_in_image(image_path, password, output_path): #this will take in a password input, an image, and encode the picture, and create a new image.
    img = Image.open(image_path)
    img = img.convert('RGB')
    width, height = img.size()
    if password_to_binary(password).length() > width * height:
        print("Password is too big for the image.")
        return


    return output_path
