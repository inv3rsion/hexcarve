import sys;
import argparse;
import subprocess;
import re;
from termcolor import colored;

FILE_SIGNATURES = {};

def usage():
    print "Usage: carver.py <file>"
    quit();

def load_file_signatures():
    with open("filesigs.txt", "r") as f:
        l = [];
        for i, line in enumerate(f.readlines()):
            add = line.lower().strip().replace(" ", "");
            l.append(add);
            if i % 2 == 1:
                if len(add) >= 8:
                    FILE_SIGNATURES[l[0]] = l[1];
                l = [];

def valid(byte):
    if 'A' <= byte <= 'z':
        return True;
    return False;

def preprocess(data):
    encode = data.encode("hex");
    found = [];
    for f in FILE_SIGNATURES.values():
        flen = len(f)/2;
        for m in re.finditer(f, encode):
            found.append((m.start()/2, m.start()/2+flen));
    return dict(found);

def hexdump(filename):
    with open(filename, "rb") as f:
        b = f.read();

        # find the locations of possible file headers
        color_indexes = preprocess(b);

        print "%08x\t" % 0,
        strrepr = "";
        color = False;
        for i, byte in enumerate(b):
            if i in color_indexes.keys():
                color = True;

            if i in color_indexes.values():
                color = False;

            if color:
                print colored(byte.encode("hex"), 'red'),
            else:
                print byte.encode("hex"),
                
            strrepr += byte if valid(byte) else ".";
            if i % 16 == 15 and i != 0:
                print "\t%s" % strrepr,
                strrepr = "";
                print
                print "%08x\t" % (i+1),

def strdump():
    pass;

def main():
    if len(sys.argv) != 2:
        usage();
    
    filename = sys.argv[1];
    hexdump(filename);

load_file_signatures();
if __name__ == "__main__":
    main();
