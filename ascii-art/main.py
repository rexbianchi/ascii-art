from PIL import Image


ASCII_CHARACTERS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
MAX_BRIGHTNESS = 255
MAX_TERMINAL_WIDTH = 250


def getPixelMatrix(img):
    img.thumbnail((MAX_TERMINAL_WIDTH, img.height))
    pixels = list(img.getdata())
    return [pixels[i:i+img.width] for i in range(0, len(pixels), img.width)]


def getBrightnessMatrix(pixelMatrix, algorithm="average", inverted=False):
    brightnessMatrix = []
    for pixelRow in pixelMatrix:
        brightnessRow = []
        for pixel in pixelRow:
            red, blue, green = pixel

            if(algorithm == "average"):
                brightness = (red + blue + green) / 3.0
            elif(algorithm == "min_max"):
                brightness = (max(pixel) + min(pixel)) / 2
            elif(algorithm == "luminosity"):
                brightness = (0.21 * red + 0.72 * green + 0.07 * blue)
            else:
                raise Exception(f"{algorithm} is not a valid algorithm!")

            if(inverted == True):
                brightness = MAX_BRIGHTNESS - brightness

            brightnessRow.append(brightness)
        brightnessMatrix.append(brightnessRow)
    return brightnessMatrix


def getASCIIMatrix(brightnessMatrix):
    asciiMatrix = []
    for brightnessRow in brightnessMatrix:
        asciiRow = []
        for brightness in brightnessRow:
            asciiChar = ASCII_CHARACTERS[int(
                brightness / MAX_BRIGHTNESS * (len(ASCII_CHARACTERS) - 1))]
            asciiRow.append(asciiChar)
        asciiMatrix.append(asciiRow)
    return asciiMatrix


def printASCIIMatrix(asciiMatrix):
    for row in asciiMatrix:
        line = [p + p + p for p in row]
        print("".join(line))


def main():

    fileName = r"C:\Users\rexbi\Desktop\ascii-pineapple.jpg"

    try:
        with Image.open(fileName) as picture:
            if not picture.mode == "RGB":
                picture = picture.convert("RGB")

            pixelMatrix = getPixelMatrix(picture)

        brightnessMatrix = getBrightnessMatrix(pixelMatrix)

        asciiMatrix = getASCIIMatrix(brightnessMatrix)

    except IOError:
        exit(f"File {fileName} not found!")

    except Exception as e:
        exit(e)

    printASCIIMatrix(asciiMatrix)


if __name__ == "__main__":
    main()
