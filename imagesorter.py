#! /usr/local/bin/python3

from PIL import Image
from math import sqrt
from os import listdir, mkdir, symlink, path
from shutil import copyfile, rmtree
import argparse

def normalize(pixel):
  R, G, B = pixel
  return (R/255., G/255., B/255.)

def gammaCorrect(pixel):
  def correction(V):
    if (V <= 0.04045):
      return V / 12.92
    else:
      return pow(((V + 0.055) / 1.055), 2.4)

  return tuple(correction(V) for V in pixel)

def photometricalLumi(pixel):
  R, G, B = pixel
  return 0.2126*float(R) + 0.7152*float(G) + 0.0722*float(B)

def digitalLumi(pixel):
  R, G, B = pixel
  return 0.299*float(R) + 0.587*float(G) + 0.114*float(B)

def physiologicalLumi(pixel):
  R, G, B = pixel
  return sqrt(0.299*(pow(float(R),2)) + 0.587*(pow(float(G),2)) + 0.114*(pow(float(B),2)))

algos = {"photometrical" : photometricalLumi, "digital" : digitalLumi, "physiological" : physiologicalLumi}

def wrapperGamma(pixel, algo, gammacorr):
  if gammacorr:
      return algo(gammaCorrect(normalize(pixel)))
  else:
      return algo(normalize(pixel))

def getAvgLuminance(imagePath, algo, gammacorr, useContrast):
  print(imagePath)
  imag = Image.open(imagePath)
  imag = imag.convert ('RGB')

  pixels = list(imag.getdata())

  totalLumi = 0

  for pixel in pixels:
    totalLumi += wrapperGamma(pixel, algo, gammacorr)

  avgLumi = float(totalLumi / len(pixels))

  if useContrast:
    totalContrast = 0

    for pixel in pixels:
      totalContrast += 1 - float(wrapperGamma(pixel, algo, gammacorr))/float(avgLumi)

    return float(totalContrast / len(pixels))

  else:
    return avgLumi

def main(srcDir, dstDir, algoname, useContrast, gammacorr, useSymlink):
  luminancesDict = {}

  print("Source directory: "+srcDir)
  print("Destination directory: "+dstDir)
  if(useSymlink):
    print("Using symlinks.")
  print()

  if algoname in algos:
    algo = algos[algoname]
  else:
    print("ERROR: Selected algoritm not available")
    return

  for i,fileName in enumerate(listdir(srcDir)):
    if fileName.endswith(".jpg") or fileName.endswith(".png") or fileName.endswith(".bmp"):
      print(str(i)+"%: Processing "+fileName)
      luminancesDict[srcDir+"/"+fileName] = getAvgLuminance(srcDir+"/"+fileName, algo, gammacorr, useContrast)
      print(luminancesDict[srcDir+"/"+fileName])

  sortedLuminancesDict = sorted(luminancesDict.items(), key=lambda x: x[1])

  if (path.isdir(dstDir)):
    rmtree(dstDir)
  
  mkdir(dstDir)

  for i,origFile in enumerate(sortedLuminancesDict):
    print()
    print("Source: "+origFile[0])
    print("Dest: "+dstDir+"/"+str(i)+path.splitext(origFile[0])[1])
    if useContrast:
      print("Contrast: "+str(origFile[1]))
    else:
      print("Luminance: "+str(origFile[1]))
    if(useSymlink):
      symlink(path.abspath(origFile[0]), dstDir+"/"+str(i)+path.splitext(origFile[0])[1])
    else:
      copyfile(origFile[0], dstDir+"/"+str(i)+path.splitext(origFile[0])[1])
  
  print()
  print("Done!")
  print("Processed "+str(len(sortedLuminancesDict))+" files.")

  return

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Sort all pictures in source directory using the average luminance.')

  parser.add_argument("source_dir", help="Source directory of pictures to sort. Defaults to current directory.", nargs='?')
  parser.add_argument("dest_dir", help="Destination directory of sorted pictures. Defaults to 'sorted' in current directory", nargs='?')
  parser.add_argument('-s', '--symlink', action='store_true', help="Avoid copies by using symlinks")
  parser.add_argument('-g', '--gamma', action='store_true', help="Correct RGB colors to take in account gamma")
  parser.add_argument('-c', '--contrast', action='store_true', help="Use average contrast as rating algorithm, based on the specified luminance algorithm")
  parser.add_argument('-a', '--algo', help="Select luminance algorithm: photometrical, digital, physiological. Defaults to physiological", nargs='?')

  args = parser.parse_args()

  if args.source_dir is None:
    args.source_dir = "./"

  if args.dest_dir is None:
    parser.print_help()
  else:
    if args.algo is None:
      args.algo = "physiological"

    main(args.source_dir, args.dest_dir, args.algo, args.contrast, args.gamma, args.symlink)