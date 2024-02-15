from PIL import Image
from math import pi, floor, log, atan2
import numpy as np
import colorsys

# Test full image: 1056
# Test mini image: 332

# TV
# zoom_factor = 1056 / 332

# Test
# zoom_factor = 3

# Selfie
zoom_factor = 5030 / 393

# Creates a test image with zoom factor 3
def create_test_image(size):
   pixels = []
   for y in np.linspace(-1, 1, size):
      row = []
      for x in np.linspace(-1, 1, size):
         if abs(x) > 1/3 or abs(y) > 1/3:
            angle = atan2(y,x)
            if angle < 0:
               angle += 2*pi
            hue = angle/(2*pi)
            (r, g, b) = colorsys.hsv_to_rgb(hue, 1, 1)
            row.append((int(r*255), int(g*255), int(b*255)))
         else:
            row.append((0,0,0))
      pixels.append(row)
   pix_array = np.array(pixels, dtype=np.uint8)
   test_image = Image.fromarray(pix_array)
   test_image.save('test.png')

# Given a complex number z, determine how many zoom factors small it is
def scale_up_factor(z):
   s1 = floor(log(abs(z.real), 1/zoom_factor))
   s2 = floor(log(abs(z.imag), 1/zoom_factor))
   s = min(s1, s2)
   if s < 1:
      return 1
   return zoom_factor**s

# Complex valued function which warps the image
def warp_function(z):
   alpha = 1 + log(zoom_factor)/(2*pi*1j)
   return pow(z, alpha)
   # return z

# Given a complex number, get the color of the source pixel
def get_source_pixel(z, src_img):
   w, h = src_img.size
   recur_w = floor(w / zoom_factor)
   pos = (floor((z.real+1)*w/2) % w, floor((z.imag+1)*h/2) % h)
   return src_img.getpixel(pos)

def get_pixel_array(src_img):
   w, h = src_img.size
   pixels = []

   for y in np.linspace(-0.5, 0.5, w):
      row = []
      for x in np.linspace(-0.5, 0.5, h):
         z = x + y * 1j
         fz = warp_function(z)
         fz *= scale_up_factor(fz)
         row.append(get_source_pixel(fz, src_img))
      pixels.append(row)

   return pixels

def main():
   src_img = Image.open('source-images/selfie.png').convert('RGB')
   # src_img = Image.open('test.png').convert('RGB')
   w, h = src_img.size

   pixels = np.array(get_pixel_array(src_img), dtype=np.uint8)
   out_img = Image.fromarray(pixels)
   out_img.save('out.png')

if __name__ == '__main__':
   main()