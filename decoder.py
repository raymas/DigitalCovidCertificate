from PIL import Image
from pyzbar import pyzbar
import curses
import zlib
import base45
import flynn
import os
import sys
import json
import argparse

def main(image_path):
    # Load the image
    qrcode = Image.open(image_path)
    
    # Decode the qrcode
    qrzbar = pyzbar.decode(qrcode)
    qr_data = qrzbar[0].data

    # depack the data and crop the header 4 to the end
    data = base45.b45decode(qr_data[4:])

    # decompress
    data = zlib.decompress(data)

    # deserialize
    data = flynn.decoder.loads(data)

    # Parse each serialized values
    content = data[1]
    header = content[0]
    medical = content[2]
    signature = content[3]

    medical_json = flynn.decoder.loads(medical)
    
    print("header " + header.hex())
    print("-"*35)
    print(json.dumps(medical_json, indent=4))
    print("-"*35)
    print("signature  " + signature.hex())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Decode the EU digital covid certificate.')
    parser.add_argument('image', metavar='image_path', type=str, help='The path to the image file')
    args = parser.parse_args()
    main(args.image)
