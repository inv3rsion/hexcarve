import sys;
import argparse;
import subprocess;

def usage():
    print "Usage: carver.py <file>"
    quit();

def valid(byte):
    if 'A' <= byte <= 'z':
        return True;
    return False;

def hexdump(filename):
    with open(filename, "rb") as f:
        b = f.read();
        print "%08x\t" % 0,
        strrepr = "";
        for i, byte in enumerate(b):
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


if __name__ == "__main__":
    main();
