import itertools


def to_bigram(text, size):
    # ngebagi input jadi sepasang huruf
    it = iter(text)
    while True:
        bigram = tuple(itertools.islice(it, size))
        if not bigram:
            return
        yield bigram


def preprocessor_input(dirty):
    # ubah jadi kapital
    # ganti huruf J jadi I
    # menyisipkan "X" ketika ada huruf yang berulang

    dirty = "".join([c.upper() for c in dirty if c != chr(32)])
    dirty = dirty.replace("J", "I")
    clean = ""

    if len(dirty) < 2:
        return dirty

    for i in range(len(dirty) - 1):
        clean += dirty[i]

        if dirty[i] == dirty[i + 1]:
            clean += "X"

    clean += dirty[-1]

    if len(clean) & 1:  # bitwise operator buat cek ganjil
        clean += "X"  # klo ganjil tambahin "X" di akhir

    return clean


def generate_table(key):
    # gapake J
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ1234567890!@#$%^&*(){}[]"
    table = []  # ALAN GANESHA SEPULUH

    # masukin char ke table, cuma pake huruf pertama klo ada duplikat
    for char in key.upper():
        if char not in table and char in alphabet:
            table.append(char)

    # masukin huruf alphabet yang belum masuk ke table
    for char in alphabet:
        if char not in table:
            table.append(char)

    return table


def encrypt(message, key):
    table = generate_table(key)
    # check=0
    # for i in range(len(table)):
    #     print(table[i], end="")
    #     check+=1
    #     if(check == 7):
    #         print()
    #         check=0
    plaintext = preprocessor_input(message)
    ciphertext = ""

    for char1, char2 in to_bigram(plaintext, 2):
        row_char1, col_char1 = divmod(table.index(char1), 7)  # (hasilDiv, hasilMod) => (row_char, col)
        row_char2, col_char2 = divmod(table.index(char2), 7)

        if row_char1 == row_char2:  # baris sama
            ciphertext += table[row_char1 * 7 + (col_char1 + 1) % 7]
            ciphertext += table[row_char2 * 7 + (col_char2 + 1) % 7]
        elif col_char1 == col_char2:  # kolom sama
            ciphertext += table[((row_char1 + 1) % 7) * 7 + col_char1]
            ciphertext += table[((row_char2 + 1) % 7) * 7 + col_char2]
        else:  # jadiin rectangle
            ciphertext += table[row_char1 * 7 + col_char2]
            ciphertext += table[row_char2 * 7 + col_char1]

    return ciphertext


def decrypt(ciphertext, key):
    table = generate_table(key)
    plaintext = ""

    for char1, char2 in to_bigram(ciphertext, 2):
        row_char1, col_char1 = divmod(table.index(char1), 7)
        row_char2, col_char2 = divmod(table.index(char2), 7)

        if row_char1 == row_char2:  # baris sama
            plaintext += table[row_char1 * 7 + (col_char1 - 1) % 7]
            plaintext += table[row_char2 * 7 + (col_char2 - 1) % 7]
        elif col_char1 == col_char2:  # kolom sama
            plaintext += table[((row_char1 - 1) % 7) * 7 + col_char1]
            plaintext += table[((row_char2 - 1) % 7) * 7 + col_char2]
        else:  # jadiin rectangle
            plaintext += table[row_char1 * 7 + col_char2]
            plaintext += table[row_char2 * 7 + col_char1]

    return plaintext

if __name__ == '__main__':
    print("Playfair Cipher")
    pilih = input("Choose :\n1) Encrypting \n2) Decrypting\n")

    if pilih == "1":
        message = "l3o im00etz bgtz cl4lu cl4many4 pt2"
        key = "leo"
        print("\nEncrypting...\n" + "Plaintext: " + message)
        print("Ciphertext: " + encrypt(message, key))
    elif pilih == "2":
        key = "leo"
        cipher = "DWAHN935BQ1AKQ2AF!CPDE9FDIW6QU3Y"
        print("\nDecrypting: \n" + "Cipher: " + cipher)
        print(decrypt(cipher, key))
        with open("decrypt.txt", 'w+') as file:
            file.write(decrypt(cipher, key))
    else:
        print("Error")