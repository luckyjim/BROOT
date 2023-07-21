#! /usr/bin/env python3
'''
Created on 19 juil. 2023

@author: jcolley
'''
import argparse
import sys


from appJar import gui
import uproot as ur
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as ssig 

import broot

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
        # print(app.getRadioButton("PLOT"))
        # print(app.getRadioButton("OPTION_0"))
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
            freq = float(app.getEntry(e_freq))
        except:
            app.errorBox("ERROR", f"{e_freq} must be a number.\nFix to 1 Hz")
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
             
    # def press_cancel(pars):
    #     app.destroySubWindow("one")
    
    app.startSubWindow("one", f"Plot {title}", modal=True, blocking=True)
    app.setSize(1000, 300)
    app.setExpand("both")
    ndim = data.ndim
    # Col 0
    app.startFrame("LEFT", row=0, column=0)
    try:
        app.addLabel(f"Range {data.shape}", row=0, column=0)
    except:
        app.addLabel(f"Range irregular", row=0, column=0)
    def_val = 0
    for idx in range(ndim):
        n_entry = f"dim {idx}"
        app.addLabelEntry(n_entry, row=idx + 1, column=0)
        if (idx + 1) == ndim:
            def_val = ":"
        app.setEntry(n_entry, def_val)
    app.stopFrame()
    if False:
        # Col 1
        app.startFrame("MIDDLE", row=0, column=1)
        app.addLabel("Plot", row=0, column=0)
        for idx in range(ndim):
            app.addRadioButton("PLOT", f"{idx}", row=idx + 1, column=0)
        app.stopFrame()
        # Col 2
        app.startFrame("RIGHT", row=0, column=2)
        app.addLabel("Option", row=0, colspan=4)
        for idx in range(ndim):
            app.addRadioButton(f"OPTION_{idx}", "Same", row=idx + 1, column=0)
            app.addRadioButton(f"OPTION_{idx}", "Sub", row=idx + 1, column=1)
            app.addRadioButton(f"OPTION_{idx}", "Slide", row=idx + 1, column=3)
            app.addRadioButton(f"OPTION_{idx}", "New", row=idx + 1, column=4)
        app.stopFrame()
    e_freq = "Freq. sampling Hz"
    app.addLabelEntry(e_freq, column=1)
    app.setEntry(e_freq, 1.0)  
    offset_row = 3
    app.addButton("Plot1D", press_plot1D, row=ndim + offset_row, column=0)
    app.addButton("Spectrum", press_spectrum, row=ndim + offset_row, column=1)
    app.addButton("Histogram", press_histo, row=ndim + offset_row, column=2)
    app.stopSubWindow()
    app.showSubWindow("one")
    app.destroySubWindow("one")


def main_gui():
    
    def main_action(s_but, i_line):
        #print(f"Call event_plot() with pars {s_but} {i_line}")
        # for arg in argv:
        #     print("Next argument through *argv :", arg)
        # for key, value in kwargs.items():
        #     print(f"{key}: {value}")
        id_t = int(s_but.split('_')[-1])
        ttree = l_ttree[id_t].split(';')[0]
        branch = all_branch[id_t][i_line]
        # print(f"{ttree} {branch}")
        # print(type(ttree), type(branch))
        data = drt[l_ttree[id_t]][branch].array()
        try:
            data = data.to_numpy()
        except:
            pass
        if s_but.find("Print") >= 0:
            try:
                str_a = np.array2string(data)
            except:
                if data.nbytes > 1024 ** 2:
                    str_a = f"{data}"
                else:
                    str_a = f"{data.tolist()}"
            app.infoBox(f"DATA of {ttree}/{branch}", str_a)
        elif s_but.find("Plot1D") >= 0:
            plot1d_gui(app, data, f"{ttree}/{branch}")
        elif s_but.find("Plot2D") >= 0:
            app.infoBox(f"{ttree}/{branch}", "Not available. Work in progreess")
        elif s_but.find("Image") >= 0:
            app.infoBox(f"{ttree}/{branch}", "Not available. Work in progreess")
            
    app = gui()
    app.setSize(1000, 600)
    # my_path = "/home/jcolley/temp/projet/grand_wk/data/root"
    # my_path = "/home/jcolley/temp"
    frt = app.openBox("BROOT open ROOT file", dirName=my_path, fileTypes=[('ROOT', '*.root'), ('ROOT', '*.r'), ("all", "*.*")])
    if len(frt) == 0:
        sys.exit(0)
    drt = ur.open(frt)
    t_idx = 0
    l_ttree = list(drt.keys()).copy()
    l_ttree.sort()
    all_branch = []
    app.startTabbedFrame("TabbedFrame")
    app.setTitle(f"BROOT {frt}")
    app.setFont(18) 
    for idx_t, ttree in enumerate(l_ttree):
        fttree = ttree.split(';')[0]
        app.startTab(fttree)
        l_branch = list(drt[fttree].keys())
        l_branch.sort()
        all_branch.append(l_branch)
        tbl_br = []
        tbl_br.append(['ID', "Branch", "Value", "Type", "Shape", "Size [Byte]"])
        l_act = []
        for idx0, branch in enumerate(l_branch):
            idx1 = idx0 + 1
            print(t_idx, idx0, branch)
            print("Please wait, reading TBranch ...")  
            l_act.append(f"Plot_{ttree}")
            val_br = drt[ttree][branch].array()            
            try:
                # NUMPY array
                np_br = val_br.to_numpy()                
                new_line = [idx1, f"{branch}", f"Array! Try Action", f"{np_br.dtype}", f"{np_br.shape}", f"{np_br.nbytes:,}"]
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
                new_line = [idx1, f"{branch}", f"Array! Try Action", f"{a_type_s[-1].strip()}", f"{a_shape}", f"{val_br.nbytes:,}"]
            tbl_br.append(new_line)
            # if idx > 5: break
            t_idx += 1            
        l_button = [f"Print_{idx_t}", f"Plot1D_{idx_t}", f"Plot2D_{idx_t}", f"Image_{idx_t}"]
        app.addTable(f"table{idx_t}", tbl_br, showMenu=True, action=main_action, actionButton=l_button)
        app.stopTab()
    app.stopTabbedFrame()
    app.go()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Browser for ROOT files from CERN collaboration.")
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
    main_gui()
