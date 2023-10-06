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
g_path_file = ""
g_ttrees = []
g_branches = []
# file root open with uproot
g_froot = None


def func_menu(s_but):
    global g_app, g_froot, g_path_file
    
    if s_but == "ABOUT":
        g_app.infoBox(f"About BROOT", f"Version: {broot.__version__} Beta\n\nAuthor: Colley Jean-Marc\n\nLab: CNRS/IN2P3/LPNHE\n\nFrance, Paris\n\nBROOT uses: \nUproot, AppJar, Numpy, Matplotlib\n\n    Oct. 2023")
    if s_but == "CLOSE":
        g_froot.close()
        g_app.removeAllWidgets()
        g_app.setTitle(f"BROOT no file")
    if s_but == "OPEN":
        r_file = g_app.openBox("BROOT open ROOT file", dirName=g_path_file, fileTypes=[('ROOT', '*.root'), ('ROOT', '*.r'), ("all", "*.*")])
        if len(r_file) != 0:
            g_path_file = os.path.dirname(r_file)
            open_root_file(r_file)
    

def open_root_file(r_file):
    global g_ttrees, g_app, g_branches, g_froot
    
    try:
        g_froot.close()
        g_app.removeAllWidgets()
    except:
        pass
    g_froot = ur.open(r_file)
    t_idx = 0
    g_ttrees = list(g_froot.keys()).copy()
    g_ttrees.sort()
    g_branches = []
    try:
        ret = g_app.startTabbedFrame("TTreeTabs")
    except:
        pass
    g_app.setTitle(f"BROOT {r_file}")
    g_app.setFont(18) 
    for idx_t, ttree in enumerate(g_ttrees):
        fttree = ttree.split(';')[0]
        g_app.startTab(ttree)
        l_branch = list(g_froot[fttree].keys())
        g_branches.append(l_branch)
        tbl_br = []
        tbl_br.append(['ID', "Branch", "Value", "Type", "Shape", "Size [Byte]"])
        l_act = []
        l_button = [f"Print", f"Plot 1D", f"Plot point", f"Image"]
        for idx0, branch in enumerate(l_branch):
            idx1 = idx0 + 1
            s_idx1 = f"{idx1:03}"
            print(t_idx, idx0, branch)
            print("Please wait, reading TBranch ...")  
            l_act.append(f"Plot_{ttree}")
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
        g_app.addTable(f"table{idx_t}", tbl_br, showMenu=True, action=main_action, actionButton=l_button)    
        g_app.stopTab()
    g_app.stopTabbedFrame()


def main_action(s_but, i_line):
    '''
    cette fonction est appelée quand l'utilisateur appuie sur un des boutons action
    
    :param s_but: name of the buttom
    :param i_line: line number associated with  buttom
    '''
    global g_app 

    ttree_name = g_app.getTabbedFrameSelectedTab("TTreeTabs")
    id_t = g_ttrees.index(ttree_name)
    ttree = g_ttrees[id_t].split(';')[0]
    # branch = g_branches[id_t][i_line]
    pars_line = g_app.getTableRow(f"table{id_t}", i_line)
    branch = pars_line[1]
    print(branch)
    data = g_froot[g_ttrees[id_t]][branch].array()
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
    
    tools = ["OPEN", "CLOSE", "ABOUT"]
    g_app.addToolbar(tools, func_menu, findIcon=True)
    g_app.setSize(1100, 600)   
    if r_file is None:
        if d_file:
            g_path_file = d_file
        else:
            g_path_file = os.getcwd()
        r_file = g_app.openBox("BROOT open ROOT file", dirName=g_path_file, fileTypes=[('ROOT', '*.root'), ('ROOT', '*.r'), ("all", "*.*")])
        if len(r_file) == 0:
            sys.exit(0)
    g_path_file = os.path.dirname(r_file)
    open_root_file(r_file)
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
