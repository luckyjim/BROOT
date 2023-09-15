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
import scipy.signal as ssig 

import broot

#
# GLOBAL
#
g_app = gui(handleArgs=False)
g_path_file = ""
g_ttres = []
g_branches = []
# file root open with uproot
g_froot = None


def plot1d_gui(app, data, title=""):
    
    def get_slice_array():
        s_idx = ""
        for idx in range(ndim):
            s_rge = app.getEntry(f'dim {idx}')
            s_idx += f"{s_rge},"
        s_idx = s_idx[:-1]
        slice_ = eval(f'np.s_[{s_idx}]')
        try:
            plot_d = data[slice_]
        except:
            app.errorBox("ERROR", f"Slice {s_idx} not valid ?")
            return False, None, s_idx
        if not isinstance(plot_d, np.ndarray):
            plot_d = plot_d.to_numpy()
        return True, plot_d, s_idx
        
    def press_plot1D(pars):
        f_conv , data_1d , s_idx = get_slice_array()
        if not f_conv: return
        plt.figure()
        plt.title(title + f", range [{s_idx}]")
        plt.plot(data_1d.ravel())
        plt.xlabel('Sample')
        plt.grid()
        plt.show()
        
    def press_spectrum(pars):
        f_conv , data_1d , s_idx = get_slice_array()
        if not f_conv: return
        try:
            freq = float(g_app.getEntry(e_freq))
        except:
            g_app.errorBox("ERROR", f"{e_freq} must be a number.\nFix to 1 Hz")
            freq = 1
        plt.figure()
        plt.title(title + f",PSD for range [{s_idx}]")
        freq, pxx_den = ssig.welch(
                        data_1d.ravel(),
                        freq,
                        window="taylor",
                        scaling="density",
                    )
        plt.semilogy(freq[2:], pxx_den[2:])
        plt.ylabel(rf"(Unit$^2$/Hz")
        plt.xlabel(f"Hz")
        plt.grid()
        plt.show()

    def press_histo(pars):
        f_conv , data_1d , s_idx = get_slice_array()
        if not f_conv: return
        plt.figure()
        plt.title(title + f",histogram for range [{s_idx}]")
        plt.hist(data_1d.ravel(), log=True)
        plt.grid()
        plt.show()
        
    try:
        g_app.destroySubWindow("one")
    except:
        pass
    g_app.startSubWindow("one", f"Plot {title}", modal=True, blocking=True)
    g_app.setSize(1000, 300)
    g_app.setExpand("both")
    ndim = data.ndim
    # Col 0
    g_app.startFrame("LEFT", row=0, column=0)
    try:
        g_app.addLabel(f"Range {data.shape}", row=0, column=0)
    except:
        g_app.addLabel(f"Range irregular", row=0, column=0)
    def_val = 0
    for idx in range(ndim):
        n_entry = f"dim {idx}"
        g_app.addLabelEntry(n_entry, row=idx + 1, column=0)
        if (idx + 1) == ndim:
            def_val = ":"
        g_app.setEntry(n_entry, def_val)
    g_app.stopFrame()
    if False:
        # Col 1
        g_app.startFrame("MIDDLE", row=0, column=1)
        g_app.addLabel("Plot", row=0, column=0)
        for idx in range(ndim):
            g_app.addRadioButton("PLOT", f"{idx}", row=idx + 1, column=0)
        g_app.stopFrame()
        # Col 2
        g_app.startFrame("RIGHT", row=0, column=2)
        g_app.addLabel("Option", row=0, colspan=4)
        for idx in range(ndim):
            g_app.addRadioButton(f"OPTION_{idx}", "Same", row=idx + 1, column=0)
            g_app.addRadioButton(f"OPTION_{idx}", "Sub", row=idx + 1, column=1)
            g_app.addRadioButton(f"OPTION_{idx}", "Slide", row=idx + 1, column=3)
            g_app.addRadioButton(f"OPTION_{idx}", "New", row=idx + 1, column=4)
        g_app.stopFrame()
    e_freq = "Freq. sampling Hz"
    g_app.addLabelEntry(e_freq, column=1)
    g_app.setEntry(e_freq, 1.0)  
    offset_row = 3
    g_app.addButton("Plot1D", press_plot1D, row=ndim + offset_row, column=0)
    g_app.addButton("Spectrum", press_spectrum, row=ndim + offset_row, column=1)
    g_app.addButton("Histogram", press_histo, row=ndim + offset_row, column=2)
    g_app.stopSubWindow()
    g_app.showSubWindow("one")


def func_menu(s_but):
    global g_app, g_froot, g_path_file
    
    if s_but == "ABOUT":
        g_app.infoBox(f"About BROOT", f"Version: {broot.__version__}\n\nAuthor: Colley Jean-Marc")
    if s_but == "CLOSE":
        g_froot.close()
        g_app.removeAllWidgets()
    if s_but == "OPEN":
        r_file = g_app.openBox("BROOT open ROOT file", dirName=g_path_file, fileTypes=[('ROOT', '*.root'), ('ROOT', '*.r'), ("all", "*.*")])
        if len(r_file) != 0:
            g_path_file = os.path.dirname(r_file)
            open_root_file(r_file)
    

def open_root_file(r_file):
    global g_ttres, g_app, g_branches, g_froot
    
    try:
        g_froot.close()
        g_app.removeAllWidgets()
    except:
        pass
    g_froot = ur.open(r_file)
    t_idx = 0
    g_ttres = list(g_froot.keys()).copy()
    g_ttres.sort()
    g_branches = []
    try:
        ret = g_app.startTabbedFrame("TabbedFrame")
    except:
        pass
    g_app.setTitle(f"BROOT {r_file}")
    g_app.setFont(18) 
    for idx_t, ttree in enumerate(g_ttres):
        fttree = ttree.split(';')[0]
        g_app.startTab(ttree)
        l_branch = list(g_froot[fttree].keys())
        g_branches.append(l_branch)
        tbl_br = []
        tbl_br.append(['ID', "Branch", "Value", "Type", "Shape", "Size [Byte]"])
        l_act = []
        l_button = [f"Print", f"Plot1D", f"Plot2D", f"Image"]
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
                new_line = [s_idx1, f"{branch}", f"Array! Try Action", f"{a_type_s[-1].strip()}", f"{a_shape}", f"{val_br.nbytes:,}"]
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

    ttree_name = g_app.getTabbedFrameSelectedTab("TabbedFrame")
    id_t = g_ttres.index(ttree_name)
    ttree = g_ttres[id_t].split(';')[0]
    branch = g_branches[id_t][i_line]
    data = g_froot[g_ttres[id_t]][branch].array()
    try:
        data = data.to_numpy()
    except:
        pass
    if s_but.find("Print") >= 0:
        if data.nbytes > 1024 * 100:
            g_app.errorBox(f"DATA of {ttree}/{branch}", "Too big, try plotxx action instead !")
            return
        try:
            str_a = np.array2string(data)
        except:
            str_a = f"{data.tolist()}"
        g_app.infoBox(f"DATA of {ttree}/{branch}", str_a)
    elif s_but.find("Plot1D") >= 0:
        plot1d_gui(g_app, data, f"{ttree}/{branch}")
    elif s_but.find("Plot2D") >= 0:
        g_app.infoBox(f"{ttree}/{branch}", "Not available. Work in progreess")
    elif s_but.find("Image") >= 0:
        g_app.infoBox(f"{ttree}/{branch}", "Not available. Work in progreess")
    

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
