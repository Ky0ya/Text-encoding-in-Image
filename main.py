import numpy as np 
from Crypto.Hash import MD5


def calMD5(text):
    md5_hash = MD5.new()
    md5_hash.update(text.encode())
    return md5_hash.hexdigest()

def writeOnImage(image,text):
    w,h = image.size
    pix = image.getdata()
    curr = 0
    x=0
    y=0
    for it in text:
        bin_val = format(ord(it),'08b')
        p1 = pix[curr]
        p2 = pix[curr+1]
        p3 = pix[curr+3]
        p = []
        for x in (p1,p2,p3):
            for val in x:
                p.append(val)
        for i in range(8):
            curr_bit = bin_val[i]
            if curr_bit=='0':
                if p[i]%2!=0:
                    p[i] -=1 if p[i]==255 else p[i]+1
            elif curr_bit=='1':
                if p[i]%2=='0':
                    p[i] +=1 if p[i]==255 else p[i]+1
        curr += 3
        if curr == len(text)*3:
            if p[-1]%2==0:
                p[-1]-=1
        else:
            if p[-1]%2!=0:
                p[-1]+=1