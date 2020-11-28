# Legify
Converts images into LEGO mosaic.

![image](https://github.com/nicomignoni/Legify/blob/master/docs/screenshot.jpg)

The conversion is made using LEGO 1x1 ([part](https://www.bricklink.com/v2/catalog/catalogitem.page?P=3005#T=C) ID: 3005) as pixel. Each pixel RBG is mapped to the limited LEGO Digital Designer palette: if we consider each color as a ![](https://latex.codecogs.com/gif.latex?%5Cmathbb%7BR%7D%5E3) vector, ![](https://latex.codecogs.com/gif.latex?c_i) as the ![](https://latex.codecogs.com/gif.latex?i)-th color from the palette, ![](https://latex.codecogs.com/gif.latex?c_o) as the original pixel color, then the new color ![](https://latex.codecogs.com/gif.latex?c_n) is calculated as 

<div align="center">
  ![eq](https://latex.codecogs.com/gif.latex?c_n%20%3D%20%5Cmin_%7Bc_i%7D%7B%7C%7Cc_i%20-%20c_o%7C%7C%7D)
</div>

for each pixel in the image
