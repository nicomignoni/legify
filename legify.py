import cv2
import json
import numpy as np
from math import floor

class Legify:
    def __init__(self, file_path='docs/test.lxfml', image_path='docs/test.jpg', scale=0.5):
        self.file_path = file_path
        full_image     = cv2.imread(image_path)
        full_image     = cv2.cvtColor(full_image, cv2.COLOR_BGR2RGB)
        self.image     = cv2.resize(full_image, (0,0), fx=scale, fy=scale)

        # index: {RGB: [.,.,.],  id: Lego color id}
        with open('data/colors.json', 'r') as c:
            self.colors = json.load(c)

        self.rgb = np.array([col['rgb'] for col in self.colors.values()])
        
        self.n_palette         = len(self.colors)
        self.h, self.w, self.c = self.image.shape

    '''Since the Lego DD palette is limited, each pixel in the image
       is converted to the closest RGB vector in the palette'''
    def quantization(self):
        # Shape: n_palette x heigh x width x self.c,nels
        reshaped_image = self.image.reshape((1, self.h, self.w, self.c))
        images_stack   = np.repeat(reshaped_image, self.n_palette, axis=0)

        reshaped_rgb    = self.rgb.reshape((self.n_palette, 1, 1, self.c))
        distances       = np.power((reshaped_rgb - images_stack), 2).sum(axis=3)
        palette_map     = np.argmin(distances, axis=0)
        quantized_image = self.rgb[palette_map.flatten(), :].reshape(self.h, self.w, self.c)
        return palette_map, quantized_image

    '''After quantization, each pixel gets mapped from the palette_map to a brick
       on the platform (i.e. <part> is written on the template.lxfml file).'''
    def legify(self):
        # Part template
        with open('data/part.xml', 'r') as p:
            part = ' '*7 + p.readline() + '\n'
        parts = list()
            
        # ty for vertical movements
        # tx for horizontal movements
        x_step = 0.40000000596046448
        y_step = 0.95999997854232788

        # Starting (line, col) of the model template
        line = 13
        
        palette_map, _ = self.quantization()
        flatten_map    = np.flipud(palette_map).flatten()
      
        for i in range(self.h*self.w):
            refID  = i
            matID  = self.colors[str(flatten_map[i])]['id']
            tx, ty = floor(i / self.w), i % self.w
            parts.append(part.format(refID, matID, matID, (tx + 1)*x_step, ty*y_step))
        
        with open('data/template.lxfml', 'r') as t:
            template = t.readlines()

        template = template[:line] + parts + template[line:]

        with open(self.file_path, 'w') as f:
            f.write(" ".join(template))
        
                
        
                                                     
                       
                       
                       
