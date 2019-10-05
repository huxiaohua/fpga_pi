import os
import shutil
import yaml
import sys


class Src():

    def __init__(self, src_file):
        self.rtl = []
        self.sim = []
        self.xdc = []
        self.ip = []
        self.sim_top = []
        self.incdir = []
        self.dpilib = []
        self.simulator = []
        print(src_file)
        self.read_src_file(src_file)

    def read_elem(self, elem_set, cur_dir, elem, dst_elem):
        if(elem) in elem_set:
            for index in elem_set[elem]:
                tmp = os.path.realpath(os.path.join(cur_dir, index))
                if tmp not in dst_elem:
                    dst_elem.extend(tmp.split())
                else:
                    print("ERROR")
                    print(tmp.split())
                    print("redefined\n")

    def read_src_file(self, src_file):

        cur_dir = os.path.split(os.path.realpath(src_file))[0]

        with open(src_file, 'r', encoding='utf-8') as fp:
            file_list = yaml.load(fp, Loader=yaml.FullLoader)

        self.read_elem(file_list, cur_dir, 'rtl',  self.rtl)
        self.read_elem(file_list, cur_dir, 'sim',  self.sim)
        self.read_elem(file_list, cur_dir, 'xdc',  self.xdc)
        self.read_elem(file_list, cur_dir, 'ip',  self.ip)
        self.read_elem(file_list, cur_dir, 'sim_top',  self.sim_top)
        self.read_elem(file_list, cur_dir, 'incdir',  self.incdir)
        self.read_elem(file_list, cur_dir, 'dpilib',  self.dpilib)
        self.read_elem(file_list, cur_dir, 'simulator',  self.simulator)

        if('file_list') in file_list:
            for index in file_list['file_list']:
                self.read_src_file(index)

        fp.close()

    def disp(self):
        if len(self.rtl) > 0:
            print("*********** RTL ** ****************")
            print(self.rtl)
            print('\n')

        if len(self.sim) > 0:
            print("*********** SIM ** ****************")
            print(self.sim)
            print('\n')

        if len(self.xdc) > 0:
            print("*********** XDC ** ****************")
            print(self.xdc)
            print('\n')

        if len(self.ip) > 0:
            print("*********** IP ** ****************")
            print(self.ip)
            print('\n')

        if len(self.sim_top) > 0:
            print("*********** SIM_TOP ** ****************")
            print(self.sim_top)
            print('\n')

        if len(self.incdir) > 0:
            print("*********** INCDIR ** ****************")
            print(self.incdir)
            print('\n')

        if len(self.dpilib) > 0:
            print("*********** DPILIB ** ****************")
            print(self.dpilib)
            print('\n')

        if len(self.simulator) > 0:
            print("*********** SIMULATOR ** ****************")
            print(self.simulator)
            print('\n')
