from PIL import Image
import imagehash

def get_hash(img_path):
    img = Image.open(img_path)
    return imagehash.average_hash(img)

def is_similar(img1, img2, threshold=10):
    return get_hash(img1) - get_hash(img2) < threshold
