import os
import sys
import shutil
import random
import subprocess
import zipfile
from threading import Thread as t
options=sys.argv

class mainc():
    def __init__(self):
        config=self.gen_config([("execute",self.run),("-e",self.run),("generate",self.generate),("-g",self.generate)])
        self.config=config

        def helpf():
            for c in self.config:
                print()
                print(c)

        try:
            if options[1] == "-h":
                helpf()

            elif options[1] in config:
                config[options[1]]()

            else:
                options[options.index(options[-1])+1]

        except IndexError:
            print("command unknow")
            print("command list:")
            helpf()

    def run(self):
        file=options[2]
        zipf=zipfile.ZipFile(file)
        os.rename(file,file.split("/")[-1].replace(".pyexe",".zip"))
        fname=file.split("/")[-1].replace(".pyexe","")
        zipf.extractall("running/")
        os.rename(file.replace(".pyexe",".zip"),file.split("/")[-1].replace(".zip",".pyexe"))
        main=subprocess.run([sys.executable,"running/"+fname+"/main.py"])
        if os.path.isfile("running/"+fname+"/require"):
            for i in open("running/"+fname+"/require").readlines():	
                subprocess.call(f'pip install {i}',shell=True)
        for file1 in self.tree("running/"+fname):
            if os.path.isfile(file1):
                os.remove(file1)

            if os.path.isdir(file1):
                shutil.rmtree(file1)

            shutil.rmtree("running/"+fname)
               
    def help(self):
        print(config)

    def generate(self):
        file=options[2]
        if os.path.isdir(file):
            zipf=zipfile.ZipFile(file+".zip","w")
            for file1 in self.tree(file):
                zipf.write(file1,compress_type=zipfile.ZIP_DEFLATED)

            zipf.close()
            file+=".zip"
            os.rename(file,file.split("/")[-1].replace(".zip",".pyexe"))

    def tree(self,dir):
        tree=[]
        for dirn,l,files in os.walk(dir):
            for file in files:
                tree.append(os.path.join(dirn,file))

        return tree

    def execute(self,a1):
        t(target=a1).start()

    def gen_config(self,list=list):
        return dict(list)

mainc()

    
