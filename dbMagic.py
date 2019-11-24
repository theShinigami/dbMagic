#!/usr/bin/env python3
import sys
import glob
import argparse
import threading
from tqdm import tqdm

class DBMagic:
    def __init__(self, filename, changeFilename, changeToFilename, stud_id):
        self.file = None
        self.modFile = None
        self.stud_id = str(stud_id)
        self.changeList = []
        self.changeToList = []
        self.filename = str(filename)
        self.changeFilename = str(changeFilename)
        self.changeToFilename = str(changeToFilename)
        self.modFilename = self.filename + ".mod"
        self.line_mod = 0
        self.filename_count = 0
    
    def fileOpen(self):
        if glob.glob(self.filename):
            self.filename_count = sum(1 for line in open(self.filename)) # get count
            self.file = open(self.filename, 'r')
        else:
            print("[-] The filename %s is not found!" % self.filename)
            exit(1)
    
    def fileClose(self, obj):
        if obj is not None: 
            obj.close()
        else:
            print("[!] There is nothing to close! - file")
    
    def createModFile(self):
        if glob.glob(self.modFilename):
            print("[!] The file %s already exists!" % self.modFilename)
            exit(1)
        self.modFile = open(self.modFilename, 'w')


    def loadChangeFile(self):
        if glob.glob(self.changeFilename):
            with open(self.changeFilename, 'r') as f:
                for l in f:
                    self.changeList.append(l.replace('\n', ''))
                f.close() # close the file
        else:
            print("[-] The file %s is not found!" % self.changeFilename)
            exit(1)
    
    def loadChangeToFile(self):
        if glob.glob(self.changeToFilename):
            with open(self.changeToFilename, 'r') as f:
                for l in f:
                    self.changeToList.append(l)
                f.close() # close the file
        else:
            print("[-] The file %s is not found!" % self.changeToFilename)
            exit(1)
    
    def displayChanges(self):
        print("\n[*] Total changes: %d\n" % self.line_mod)

    @staticmethod
    def striper(s):
        return s.replace(' ', '').replace('\n', '')
    
    def extractFields(self, s):
        print("[+] Creating extract.lst...")
        g = open("extract.lst", "w")
        pb = tqdm(total=self.filename_count)
        self.fileOpen()
        
        with self.file as f:
            for line in f:
                pb.update(1) # update the bar everytime we hit a line
                if s in line:
                    g.write(line)
                else: pass
            f.close() # close the file
        pb.close() # close the progress bar...  
        g.close()
        print("[*] Done extracting...")

    def readFile(self):
        pb = tqdm(total=self.filename_count)
        with self.modFile as wable:
            with self.file as f:
                for line in f:
                    pb.update(1) # update the bar everytime we hit a line
                    if self.stud_id in line:
                        for chg in self.changeList:
                            if self.striper(chg) == self.striper(line):
                                wable.write(self.changeToList[0])
                                self.changeToList.pop(0) # remove the first index
                                self.line_mod += 1
                            else: pass
                    else:
                        wable.write(line)  
                f.close() # close the file
            wable.close() # close wable
        pb.close() # close the progress bar...           
    
    def start(self):
        print("[*] Starting DBMagic...\n")
        self.fileOpen()
        self.createModFile()
        self.loadChangeFile()
        self.loadChangeToFile()
        self.readFile()
        self.displayChanges()
        print("[*] Done.")



def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--sql', help='to set the sql data', required=True)
    parser.add_argument('-c', '--changelist', help='to set the change list')
    parser.add_argument('-t', '--tochangelist', help='to set the to-change list')
    parser.add_argument('-m', '--match', help='to match the list of data with this string', required=True)
    parser.add_argument('-e', '--extract', help='this option is for extracting line with -m string', action='store_true')

    args = parser.parse_args()

    sql = args.sql
    changelist = args.changelist
    tochangelist = args.tochangelist
    match = args.match
    extract = args.extract

    if extract:
        DBMagic(filename=sql, changeFilename=changelist, changeToFilename=tochangelist, stud_id=match).extractFields(match)
    else:
        DBMagic(filename=sql, changeFilename=changelist, changeToFilename=tochangelist, stud_id=match).start()





if __name__ == "__main__":
    main()
