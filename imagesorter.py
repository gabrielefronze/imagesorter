#! /usr/local/bin/python3

from PIL import Image
from math import sqrt
import os
from shutil import copyfile, rmtree
import argparse

def getAvgLuminance(imagePath):
  imag = Image.open(imagePath)
  imag = imag.convert ('RGB')

  pixels = list(imag.getdata())
  totalLumi = 0

  for pixel in pixels:
    R, G, B = pixel
    totalLumi += sqrt(0.299*(R**2) + 0.587*(G**2) + 0.114*(B**2))

  return int(round(totalLumi / len(pixels),0))

def main(srcDir, dstDir, useSymlink = True):
  luminancesDict = {}

  for fileName in os.listdir(srcDir):
    if fileName.endswith(".jpg") or fileName.endswith(".png") or fileName.endswith(".bmp"):
      luminancesDict[srcDir+fileName] = getAvgLuminance(srcDir+fileName)

  sortedLuminancesDict = sorted(luminancesDict.items(), key=lambda x: x[1])

  if (os.path.isdir(dstDir)):
    rmtree(dstDir)
  
  os.mkdir(dstDir)

  for i,origFile in enumerate(sortedLuminancesDict):
    print("Source: "+origFile[0])
    print("Dest: "+dstDir+"/"+str(i)+os.path.splitext(origFile[0])[1])
    print("Luminance: "+str(origFile[1]))
    if(useSymlink):
      os.symlink(origFile[0], dstDir+"/"+str(i)+os.path.splitext(origFile[0])[1])
    else:
      copyfile(origFile[0], dstDir+"/"+str(i)+os.path.splitext(origFile[0])[1])

  return

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Sort all pictures in source directory using the average luminance.')

  parser.add_argument("source_dir", help="Source directory of pictures to sort. Defaults to current directory.", nargs='?')
  parser.add_argument("dest_dir", help="Destination directory of sorted pictures. Defaults to 'sorted' in current directory", nargs='?')
  parser.add_argument('-s', '--symlink', action='store_true', help="Avoid copies by using symlinks")

  args = parser.parse_args()

  if args.source_dir is None:
    args.source_dir = "./"

  if args.dest_dir is None:
    args.dest_dir = "./sorted"

  main(args.source_dir, args.dest_dir, args.symlink)