#! /usr/bin/env python3

'''
Created on 19 juil. 2023

@author: jcolley

a faire:
 * fichier Atlas pb affichage PLOT_1D

'''
import argparse
import sys
import os
import os.path
import pprint

from appJar import gui
import uproot as ur
import matplotlib.pyplot as plt
import numpy as np

import broot
import ndarray_view.image as v_ima
import ndarray_view.plot1d as v_p1d
import ndarray_view.plot_point as v_point
#
# GLOBAL
#
g_app = gui(handleArgs=False)
g_app.setLogLevel("ERROR")
g_path_file = ""
# file root open with uproot
g_froot = None
g_d_fulltables = {}
g_d_tables = {}


def manage_menu(s_but):
    global g_app, g_froot, g_path_file, g_d_fulltables, g_d_tables
    
    if s_but == "ABOUT":
        g_app.infoBox(f"About BROOT", f"Version: {broot.__version__} Beta\n\nAuthor: Colley Jean-Marc\n\nLab: CNRS/IN2P3/LPNHE\n\nFrance, Paris\n\nBROOT uses: \nUproot, AppJar, Numpy, Matplotlib\n\n    Nov. 2023")
    if s_but == "CLOSE":
        g_froot.close()
        # g_app.removeAllWidgets()
        g_app.removeTabbedFrame("TTreeTabs")
        g_app.setTitle(f"BROOT no file")
        g_d_fulltables = {}
        g_d_tables = {}
    if s_but == "OPEN":
        r_file = g_app.openBox("BROOT open ROOT file", dirName=g_path_file, fileTypes=[('ROOT', '*.root'), ('ROOT', '*.r'), ("all", "*.*")])
        if len(r_file) != 0:
            g_path_file = os.path.dirname(r_file)
            # open_root_file(r_file)
            rootfile_to_tables(r_file)
            create_gui_tables(r_file, g_d_fulltables)
            
    
def rootfile_to_tables(r_file):
    global g_froot, g_d_fulltables
    
    try:
        g_froot.close()
    except:
        pass    
    g_froot = ur.open(r_file)
    t_idx = 0
    ttrees = list(g_froot.keys()).copy()
    ttrees.sort()
    g_d_fulltables = {}
    
    for idx_t, ttree in enumerate(ttrees):
        fttree = ttree.split(';')[0]
        l_branch = list(g_froot[fttree].keys())
        tbl_br = []
        tbl_br.append(['ID', "TBranch", "Value", "Type", "Shape", "Size [Byte]"])
        for idx0, branch in enumerate(l_branch):
            idx1 = idx0 + 1
            s_idx1 = f"{idx1:03}"
            print(t_idx, idx0, branch)
            print("Please wait, reading TBranch ...")
            val_br = g_froot[ttree][branch].array()            
            try:
                # NUMPY array
                np_br = val_br.to_numpy()                
                new_line = [s_idx1, f"{branch}", f"Array! Try Action", f"{np_br.dtype}", f"{np_br.shape}", f"{np_br.nbytes:,}"]
                if np_br.size == 0:
                    new_line[2] = f"Empty !?"
                if np_br.size == 1:
                    print(np_br)
                    if val_br.typestr.find('string') >= 0:
                        new_line[2] = f"'{np_br[0]}'"
                        new_line[3] = 'string'
                    else:
                        new_line[2] = np_br.ravel()[0]
            except:
                # IRREGULAR array
                a_type_s = val_br.typestr.split('*')
                a_shape = '(' + ','.join(a_type_s[:-1]) + ')' 
                a_shape = a_shape.replace(' ', '')
                new_line = [s_idx1, f"{branch}", f"Array ! Try Action", f"{a_type_s[-1].strip()}", f"{a_shape}", f"{val_br.nbytes:,}"]
            tbl_br.append(new_line)
            # if idx > 5: break
            t_idx += 1
        g_d_fulltables[ttree] = tbl_br
    

def create_gui_tables(r_file, d_tables):
    global g_app, g_d_tables
    try:
        # g_app.removeAllWidgets()
        g_app.removeTabbedFrame("TTreeTabs")
        pass
    except:
        pass
    try:
        ret = g_app.startTabbedFrame("TTreeTabs", 4, 0)
    except:
        pass
    g_app.setTitle(f"BROOT {r_file}")
    g_app.setFont(18)
    l_button = [f"Print", f"Plot 1D", f"Plot point", f"Image"]
    for idx_t, ttree in enumerate(d_tables.keys()):
        g_app.startTab(ttree)
        g_app.addTable(f"table{idx_t}", d_tables[ttree], showMenu=True, action=manage_action, actionButton=l_button)    
        g_app.stopTab()
    g_app.stopTabbedFrame()
    g_d_tables = d_tables.copy()


def manage_action(s_but, i_line):
    '''
    cette fonction est appelée quand l'utilisateur appuie sur un des boutons action
    
    :param s_but: name of the buttom
    :param i_line: line number associated with  buttom
    '''
    global g_app 

    ttree_name = g_app.getTabbedFrameSelectedTab("TTreeTabs")
    ttrees = list(g_d_tables.keys())
    print(ttree_name)
    print(ttrees)
    id_t = ttrees.index(ttree_name)
    ttree = ttrees[id_t].split(';')[0]
    pars_line = g_app.getTableRow(f"table{id_t}", i_line)
    branch = pars_line[1]
    print(branch)
    data = g_froot[ttrees[id_t]][branch].array()
    try:
        data = data.to_numpy()
    except:
        pass
    if s_but.find("Print") >= 0:
        if data.nbytes > 1024 * 100:
            g_app.errorBox(f"DATA of {ttree}.{branch}", "Too big, try 'Plot xx' action instead !")
            return
        try:
            str_a = np.array2string(data)
        except:
            str_a = f"{data.tolist()}"
        g_app.infoBox(f"DATA of {ttree}.{branch}", str_a)
    elif s_but.find("Plot 1D") >= 0:
        v_p1d.gui_view_plot1d(g_app, data, f"{ttree}.{branch}")
    elif s_but.find("Plot point") >= 0:
        # g_app.infoBox(f"{ttree}.{branch}", "Not available. Work in progreess")
        v_point.gui_view_point(g_app, data, f"{ttree}.{branch}")
    elif s_but.find("Image") >= 0:
        # g_app.infoBox(f"{ttree}.{branch}", "Not available. Work in progreess")
        v_ima.gui_view_image(g_app, data, f"{ttree}.{branch}")


def main_gui(r_file=None, d_file=None):
    global g_app, g_path_file
    
    def filter_name():
        print("Apply filter")        
        fstr_branch = g_app.getEntry("TBranch").replace(' ', '')
        fstr_tree = g_app.getEntry("TTree  ").replace(' ', '')
        if g_d_fulltables == {} or (fstr_branch == "" and fstr_tree == ""):
            print("Rien à faire ...")
            return        
        d_ftables = {}
        for ttree in g_d_fulltables.keys():
            if ttree.find(fstr_tree) >= 0:
                d_ftables[ttree] = []
                d_ftables[ttree].append(['ID', "TBranch", "Value", "Type", "Shape", "Size [Byte]"])
                for branch in g_d_fulltables[ttree]:
                    if branch[1].find(fstr_branch) >= 0:
                        d_ftables[ttree].append(branch)
                        print("Select ", branch[1])
                if len(d_ftables[ttree]) == 1:
                    del d_ftables[ttree]
                    print(f"del {ttree} empty")
        # pprint.pprint(d_ftables)
        create_gui_tables(r_file, d_ftables)

    def filter_reset():
        print("Reset")
        if g_d_fulltables == {} or g_d_fulltables == g_d_tables:
            print("Rien à faire ...")
            return
        g_app.setEntry("TTree  ", "")
        g_app.setEntry("TBranch", "")
        create_gui_tables(r_file, g_d_fulltables)       
    
    tools = ["OPEN", "CLOSE", "ABOUT"]
    # g_app.setSticky("news")
    g_app.setExpand("both")
    g_app.setStretch("none")
    g_app.setFont(18)
    g_app.setSize(1100, 600)
    g_app.addToolbar(tools, manage_menu, findIcon=True)
    g_app.startFrame("FILTER")
    g_app.addLabelEntry("TTree  ")
    g_app.addLabelEntry("TBranch")
    g_app.addButton("Filter", filter_name, 0, 1, rowspan=2)
    g_app.addButton("Reset", filter_reset, 0, 2, rowspan=2)
    g_app.addLabel("Empty line", "", 2, 0)
    g_app.stopFrame()
    g_app.setStretch("both")   
    if r_file is None:
        if d_file:
            g_path_file = d_file
        else:
            g_path_file = os.getcwd()
        r_file = g_app.openBox("BROOT open ROOT file", dirName=g_path_file, fileTypes=[('ROOT', '*.root'), ('ROOT', '*.r'), ("all", "*.*")])
        if len(r_file) == 0:
            sys.exit(0)
    g_path_file = os.path.dirname(r_file)
    # open_root_file(r_file)
    rootfile_to_tables(r_file)
    create_gui_tables(r_file, g_d_fulltables)
    g_app.go()

#
# MAIN
#


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Browser for ROOT files from CERN collaboration.")
    parser.add_argument(
        "-f",
        "--file",
        help="path to ROOT file or directory",
        required=False
    )
    parser.add_argument(
        "-v",
        "--version",
        help="BROOT version",
        action="store_true",
        required=False
    )
    args = parser.parse_args()
    if args.version:
        print(broot.__version__)
        sys.exit(0)
    if args.file is not None:
        abs_file = os.path.abspath(args.file)
        assert os.path.exists(abs_file), f"'{abs_file}' doesn't exist !!"
        if os.path.isdir(abs_file):
            main_gui(d_file=abs_file)
        else:
            main_gui(r_file=abs_file)
    else:
        main_gui()
