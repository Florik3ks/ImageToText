from PIL import Image

filename = input("input file name (file in the img-folder): ")
print("Please wait..")

im = Image.open("img/"+ filename)

r = im.convert('1')
ratio = .5
r.thumbnail((im.height // ratio, im.width // ratio))
im = r
pix = r.load()

# returns a hex value to be added to the dot position at [x y]
def add_dot_position(x, y):
    # https://en.wikipedia.org/wiki/Braille_Patterns
    pos = [["1", "8", ],
           ["2", "10",],
           ["4", "20",],
           ["40", "80"]]

    nx = x % 2
    ny = y % 4

    if pix[x, y] == 255:
        return pos[ny][nx]
    return "0"

# returns the position in the array for a pixel at [x y]
def get_arr_position(x, y):
    return x // 2, y // 4


dots = []
for y in range(im.height // 4):
    dots.append(["2800" for _ in range(im.width // 2)])

for y in range((im.height // 4) * 4):
    for x in range((im.width // 2) * 2):
        nx, ny = get_arr_position(x,y)
        value = hex(int(dots[ny][nx], 16) + int(add_dot_position(x, y), 16))
        dots[ny][nx] = value

for y in range(len(dots)):
    for x in range(len(dots[0])):
        dots[y][x] = chr(int(dots[y][x], 16))

f_name = "result/" + ''.join(filename.split(".")[:-1]) + "-result.txt"
f = open(f_name, "w", encoding="utf-8")
for line in dots:
    f.write(''.join(line) + "\n")
f.close()
print("success!\nsaved in " + f_name)