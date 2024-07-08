import cv2

def encode(image, text, filename):
    h, w, _ = image.shape
    curr = 0
    len_covered = 0
    text_len = len(text)
    
    for it in text:
        bin_val = format(ord(it), '08b')
        p1 = image[curr // w, curr % w]
        p2 = image[(curr + 1) // w, (curr + 1) % w]
        p3 = image[(curr + 2) // w, (curr + 2) % w]
        p = list(p1) + list(p2) + list(p3)
        
        for i in range(8):
            curr_bit = bin_val[i]
            if curr_bit == '0':
                if p[i] % 2 != 0:
                    p[i] -= 1
            elif curr_bit == '1':
                if p[i] % 2 == 0:
                    p[i] += 1

        curr += 3
        len_covered += 1

        if len_covered == text_len:
            if p[-1] % 2 == 0:
                p[-1] += 1
        else:
            if p[-1] % 2 != 0:
                p[-1] -= 1

        # Update the image with the modified pixel values
        image[curr // w, curr % w] = tuple(p[:3])
        image[(curr + 1) // w, (curr + 1) % w] = tuple(p[3:6])
        image[(curr + 2) // w, (curr + 2) % w] = tuple(p[6:9])

    updatedImageFile = filename.split('.')[0] + "-upd.png"
    cv2.imwrite(updatedImageFile, image)
    return updatedImageFile

def decode(image):
    h, w, _ = image.shape
    curr = 0
    text = ""
    
    while True:
        bin_val = ""
        p1 = image[curr // w, curr % w]
        p2 = image[(curr + 1) // w, (curr + 1) % w]
        p3 = image[(curr + 2) // w, (curr + 2) % w]
        p = list(p1) + list(p2) + list(p3)
        
        for i in range(8):
            if p[i] % 2 == 0:
                bin_val += "0"
            else:
                bin_val += "1"

        ascii_val = int(bin_val, 2)
        text += chr(ascii_val)
        curr += 3

        if p[-1] % 2 != 0:
            break

    return text