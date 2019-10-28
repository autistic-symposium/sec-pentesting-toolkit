from PIL import Image

img = Image.open('steg100.png')

strbit1 = ''
for y in range(0, img.size[1], 19):
	for x in range(0, img.size[0], 19):
		r = img.getpixel((x, y))
		strbit1 += str(r & 1)

strbit2 = ''
for y in range(171, 171 + 19):
	for x in range(171, 171 + 19):
		a = img.getpixel((x, y))
		strbit2 += str(a & 1)

xored = ''.join(str(int(A) ^ int(B)) for A, B in zip(strbit1, strbit2))
print ''.join(chr(int(xored[i:i + 8], 2)) for i in range(0, len(xored), 8))
