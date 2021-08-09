import zlib
import base45
import base64
import os
import sys
import json
import argparse
import cbor2
from PIL import Image
from pyzbar import pyzbar
from cose.messages import CoseMessage
from cose.headers import Algorithm, KID

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
    cose = CoseMessage.decode(data)
    tag = cose.cbor_tag
    algorithm = cose.get_attr(Algorithm)
    key_id = cose.get_attr(KID)
    signature = cose.signature

    cbor = cbor2.loads(cose.payload)

    print("Cose key algorithm: " + algorithm.fullname)
    print("Cose key curve: " + str(algorithm.get_curve()))
    print("Cose key id: " + base64.b64encode(key_id).decode('utf-8'))
    print("-"*35)
    print("CBOR tag: " + str(tag))
    print("Medical data:")
    print(json.dumps(cbor, indent=4))
    print("-"*35)
    print("Cose signature [length:" + str(len(signature)) + "] " + signature.hex())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Decode the EU digital covid certificate.')
    parser.add_argument('image', metavar='image_path', type=str, help='The path to the image file')
    args = parser.parse_args()
    main(args.image)
