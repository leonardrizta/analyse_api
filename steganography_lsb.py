import numpy as np
from PIL import Image


def encode(cypher_text, image_file):
    binary_idx = 0
    binary_string = ''.join(format(ord(char), '08b') for char in cypher_text)
    img = Image.open(image_file).convert('RGB')
    img_array = np.array(img, dtype='uint8') #ngambil array rgb, unsigned integer
    img.close()
    img_list = img_array.tolist() #dari numpy array jadi list biar bisa diedit seenak jidat leo
    rows = []
    for row in img_list:
        columns = []
        for column in row:
            elements = []
            for element in column:
                element = format(element, '08b')
                if binary_idx < len(binary_string):
                    element = element[:-1] + str(binary_string[binary_idx])
                    binary_idx += 1
                else:
                    element = element[:-1] + '0'
                element = int(element, 2)
                elements += [element]
            columns += [elements]
        rows += [columns]
    img_array = np.array(rows)
    img = Image.fromarray(img_array.astype(np.uint8))
    img.convert('RGB').save('static/uploads/encrypted_image.png', format="png")
    img.close()


def decode(filename):
    img = Image.open(filename).convert('RGB')
    img_array = np.asarray(img)
    img.close()
    img_list = img_array.tolist()
    decoded_text = ""
    null_checker = ''
    for row in img_list:
        for column in row:
            for element in column:
                element = format(element, '08b')
                decoded_text += element[-1]
                null_checker += element[-1]
                if len(null_checker) == 8:
                    if null_checker == '00000000':
                        return decoded_text[:-8]
                    else:
                        decoded_text += ' '
                        null_checker = ''


if __name__ == "__main__":
    print("What do you want to do?")
    print("1. Encode an Image")
    print("2. Decode an Image")
    choose = input("Select your choice [1-2] = ")
    if choose == '1':
        encode()
    elif choose == '2':
        binary_decode = decode().split()
        binary_string = ''
        for char in binary_decode:
            binary_string += chr(int(char, 2))
        print("Decode done! The hidden text is saved to image/hidden_message.txt")
        with open("image/hidden_message.txt", 'w+') as file:
            file.write(binary_string)
    else:
        print("Wrong Choose!")

