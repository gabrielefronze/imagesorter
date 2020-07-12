#! /usr/local/bin/python3

from imagesorter import getAvgLuminance

if __name__ == "__main__":
  print(getAvgLuminance("./test.jpg"))
  print(getAvgLuminance("./black.jpg"))
  print(getAvgLuminance("./white.png"))