"""
Created on 29 sept. 2023

@author: jcolley
"""

from appJar import gui
import matplotlib.pyplot as plt
import numpy as np

import matplotlib
matplotlib.use('TkAgg')

def gui_view_image(a_gui, data, title=""):
    def get_slice_array():
        s_idx = ""
        f_transp = None
        f_nodef_x = True
        f_nodef_y = True
        for idx in range(ndim):
            s_rge = a_gui.getEntry(f"ima_dim {idx}").replace(" ", "")
            s_rge = s_rge.lower()
            print(s_rge)
            if s_rge[0] == "x":
                s_rge = s_rge.replace("x=", "x")
                if s_rge[1:] == "":
                    s_idx += f":,"
                else:
                    s_idx += f"{s_rge[1:]},"
                f_transp = False
                f_nodef_x = False
            elif s_rge[0] == "y":
                s_rge = s_rge.replace("y=", "y")
                if s_rge[1:] == "":
                    s_idx += f":,"
                else:
                    s_idx += f"{s_rge[1:]},"
                f_transp = True
                f_nodef_y = False
            else:
                s_idx += f"{s_rge},"
            print(s_idx)
        # remove last ,
        if f_nodef_x or f_nodef_y:
            print(f_nodef_x, f_nodef_y)
            a_gui.errorBox(title, "You must define x and y")
            return False, None, None, None
        s_idx = s_idx[:-1]
        try:
            slice_ = eval(f"np.s_[{s_idx}]")
            a_image = data[slice_]
        except:
            a_gui.errorBox("ERROR", f"Slice {s_idx} not valid ?")
            return False, None, s_idx, f_transp
        if not isinstance(a_image, np.ndarray):
            try:
                a_image = a_image.to_numpy()
            except:
                a_gui.errorBox(title, "Can't convert in regular array")
                return False, a_image, s_idx, f_transp
        return True, a_image, s_idx, f_transp

    def press_image():
        f_conv, data_2d, s_idx, f_transp = get_slice_array()
        if not f_conv:
            return
        if f_transp:
            data_2d = data_2d.transpose()
        plt.figure()
        plt.title(title + f", range [{s_idx}]")
        plt.imshow(data_2d)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid()
        plt.show()

    try:
        a_gui.destroySubWindow("image")
    except:
        pass
    a_gui.startSubWindow("image", f"BROOT image: {title}", modal=True, blocking=True)
    a_gui.setSize(1000, 300)
    a_gui.setExpand("both")
    ndim = data.ndim
    if ndim <= 1:
        a_gui.errorBox(title, "Dimension of array must be => 2.")
        return
    # Col 0
    a_gui.startFrame("ima_LEFT", row=0, column=0)
    try:
        str_range = f"Shape {data.shape}"
    except:
        str_range = "Range irregular"
    a_gui.addLabel("ima_range", str_range, row=0, column=0)

    for idx in range(ndim):
        n_entry = f"ima_dim {idx}"
        a_gui.addLabelEntry(n_entry, row=idx + 1, column=0, label=f"axis {idx}")
        if idx == 0:
            a_gui.setEntry(n_entry, "x")
        elif idx == 1:
            a_gui.setEntry(n_entry, "y")
        else:
            a_gui.setEntry(n_entry, "0")
    a_gui.stopFrame()
    a_gui.addButton("Image", press_image, row=ndim, column=0)
    a_gui.stopSubWindow()
    a_gui.showSubWindow("image")
    a_gui.remove
