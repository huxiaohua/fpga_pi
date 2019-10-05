from src import *
import os
import shutil


class VCS():

    def __init__(self, src):
        self.src = src

        if not os.path.isfile("vcs.yml"):
            shutil.copyfile(
                "/home/huxiaohua/opt/fpga_pi/config/vcs.yml", "vcs.yml")

        with open('vcs.yml', 'r', encoding='utf-8') as fp:
            opt = yaml.load(fp, Loader=yaml.FullLoader)

        self.vlogan_opt = opt["vlogan_opts"]
        self.vhdlan_opt = opt["vhdlan_opts"]
        self.elab_opt = opt["elab_opts"]
        self.lib = opt["lib"]

        if len(self.src.incdir) > 0:
            self.vlogan_opt += ' +incdir'
            for t in self.src.incdir:
                self.vlogan_opt += '+' + t

    def setup(self):
        if os.path.isfile("synopsys_sim.setup"):
            os.remove("synopsys_sim.setup")

        f = open("synopsys_sim.setup", "w+")

        f.writelines("OTHERS=")
        f.writelines(self.lib)
        f.writelines("/synopsys_sim.setup\n")
        f.writelines("xil_defaultlib : vcs/xil_defaultlib\n")

        f.close()

    def comp(self):
        if(os.path.exists("vcs")):
            shutil.rmtree("vcs")

        os.makedirs("vcs/xil_defaultlib")

        print("synopsys_sim.setup create successful")

        self.ver_src = ''
        self.vhd_src = ''

        if len(self.src.sim) > 0:
            self.src.rtl.extend(self.src.sim)

        for src in self.src.rtl:
            name, ext = os.path.splitext(src)
            if (ext.lower() == '.sv') | (ext.lower() == '.v'):
                self.ver_src += src + ' '
            elif ext.lower() == '.vhd':
                self.vhd_src += src + ' '
            else:
                print("ERROR : Invalid source file")

        if len(self.ver_src) > 0:
            os.system("vlogan %s %s > vlog_comp.log" %
                      (self.vlogan_opt, self.ver_src))

        if len(self.vhd_src) > 0:
            os.system("vhdlan %s %s > vhdl_comp.log" %
                      (self.vhdlan_opt, self.vhd_src))

    def elab(self):
        if len(self.ver_src) > 0:
            os.system("vcs %s xil_defaultlib.%s xil_defaultlib.glbl -o %s > elab.log" %
                      (self.elab_opt, self.src.sim_top, self.src.sim_top))
        else:
            os.system("vcs %s xil_defaultlib.%s -o %s > elab.log" %
                      (self.elab_opt, self.src.sim_top, self.src.sim_top))

    def sim(self):
        pass
