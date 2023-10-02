'''
Created on 29 sept. 2023

@author: jcolley
'''

from appJar import gui
import uproot as ur
import matplotlib.pyplot as plt
import numpy as np


def gui_view_image(a_gui, data, title=""):
    
    def get_slice_array():
        s_idx = ""
        for idx in range(ndim):
            s_rge = a_gui.getEntry(f'dim {idx}')
            s_idx += f"{s_rge},"
        s_idx = s_idx[:-1]
        slice_ = eval(f'np.s_[{s_idx}]')
        try:
            plot_d = data[slice_]
        except:
            a_gui.errorBox("ERROR", f"Slice {s_idx} not valid ?")
            return False, None, s_idx
        if not isinstance(plot_d, np.ndarray):
            plot_d = plot_d.to_numpy()
        return True, plot_d, s_idx
        
    def press_image(pars):
        f_conv , data_2d , s_idx = get_slice_array()
        if not f_conv: return
        plt.figure()
        plt.title(title + f", range [{s_idx}]")
        plt.imshow(data_2d)
        plt.xlabel('Sample')
        plt.grid()
        plt.show()

    try:
        a_gui.destroySubWindow("image")
    except:
        pass
    a_gui.startSubWindow("image", f"BROOT Image {title}", modal=True, blocking=True)
    a_gui.setSize(1000, 300)
    a_gui.setExpand("both")
    ndim = data.ndim
    # Col 0
    a_gui.startFrame("LEFT_IMA", row=0, column=0)
    try:
        a_gui.addLabel(f"Range {data.shape}", row=0, column=0)
    except:
        a_gui.addLabel(f"Range irregular", row=0, column=0)
    for idx in range(ndim):
        n_entry = f"dim {idx}"
        a_gui.addLabelEntry(n_entry, row=idx + 1, column=0)
        if idx == 0:
            a_gui.setEntry(n_entry, 'x')
        elif idx ==1:
            a_gui.setEntry(n_entry, 'y')
        else:
            a_gui.setEntry(n_entry, '0')
    a_gui.stopFrame()
    a_gui.addButton("Image", press_image, row=ndim, column=0)
    a_gui.stopSubWindow()
    a_gui.showSubWindow("image")
