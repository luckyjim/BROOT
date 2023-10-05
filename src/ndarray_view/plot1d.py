'''
Created on 29 sept. 2023

@author: jcolley
'''

from appJar import gui
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as ssig 

def gui_view_plot1d(a_gui, data, title=""):
    
    def get_slice_array():
        s_idx = ""
        for idx in range(ndim):
            s_rge = a_gui.getEntry(f'dim {idx}')
            s_idx += f"{s_rge},"
        s_idx = s_idx[:-1]
        try:
            slice_ = eval(f'np.s_[{s_idx}]')
            plot_d = data[slice_]
        except:
            a_gui.errorBox("ERROR", f"Slice {s_idx} not valid ?")
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
            freq = float(a_gui.getEntry(e_freq))
        except:
            a_gui.errorBox("ERROR", f"{e_freq} must be a number.\nFix to 1 Hz")
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
        a_gui.destroySubWindow("plot1d")
    except:
        pass
    a_gui.startSubWindow("plot1d", f"BROOT plot sample: {title}", modal=True, blocking=True)
    a_gui.setSize(1000, 300)
    a_gui.setExpand("both")
    ndim = data.ndim
    # Col 0
    a_gui.startFrame("LEFT", row=0, column=0)
    try:
        str_range = f"Shape {data.shape}"
    except:
        str_range = "Shape irregular"
    a_gui.addLabel("p1d_range",str_range, row=0, column=0)   
    # 0 est la valeur par defaut pour les premieres dimension
    # la derniere dimension est :
    def_val = 0
    for idx in range(ndim):
        n_entry = f"dim {idx}"
        a_gui.addLabelEntry(n_entry, row=idx + 1, column=0)
        if (idx + 1) == ndim:
            def_val = ":"
        a_gui.setEntry(n_entry, def_val)
    a_gui.stopFrame()
    if False:
        # Col 1
        a_gui.startFrame("MIDDLE", row=0, column=1)
        a_gui.addLabel("Plot", row=0, column=0)
        for idx in range(ndim):
            a_gui.addRadioButton("PLOT", f"{idx}", row=idx + 1, column=0)
        a_gui.stopFrame()
        # Col 2
        a_gui.startFrame("RIGHT", row=0, column=2)
        a_gui.addLabel("Option", row=0, colspan=4)
        for idx in range(ndim):
            a_gui.addRadioButton(f"OPTION_{idx}", "Same", row=idx + 1, column=0)
            a_gui.addRadioButton(f"OPTION_{idx}", "Sub", row=idx + 1, column=1)
            a_gui.addRadioButton(f"OPTION_{idx}", "Slide", row=idx + 1, column=3)
            a_gui.addRadioButton(f"OPTION_{idx}", "New", row=idx + 1, column=4)
        a_gui.stopFrame()
    e_freq = "Freq. sampling Hz"
    a_gui.addLabelEntry(e_freq, column=1)
    a_gui.setEntry(e_freq, 1.0)  
    offset_row = 3
    a_gui.addButton("Plot1D", press_plot1D, row=ndim + offset_row, column=0)
    a_gui.addButton("Spectrum", press_spectrum, row=ndim + offset_row, column=1)
    a_gui.addButton("Histogram", press_histo, row=ndim + offset_row, column=2)
    a_gui.stopSubWindow()
    a_gui.showSubWindow("plot1d")
