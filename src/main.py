import sys

from src.ImageDirectoryImporter import ImageDirectoryHandler
from PIL import Image
from src.Observer import View

print(len(sys.argv[1]))
if len(sys.argv) == 5:
    imageDirectoryHandler = ImageDirectoryHandler(sys.argv[1], Image.open(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))

    view = View()
    view.run()
else:
    print("Invalid number or args")
