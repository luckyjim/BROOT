'''
Created on 29 sept. 2023

@author: jcolley
'''

from appJar import gui
import matplotlib.pyplot as plt
import numpy as np


def gui_view_point(a_gui, data, title=""):
    
    def get_slice_array():
        s_idx = ""
        f_def_sample_dim = True
        f_nodef_dim = [True, True, True]
        d_dim_char = {"x":0, "y":1, "z":2}
        d_dim_idx = {"x":0, "y":0, "z":0}
        l_data = [0, 0, 0]
        s_xyz= ""
        nb_dim = 0
        for idx in range(ndim):
            s_ori_rge = a_gui.getEntry(f'point_dim {idx}').replace(" ", "")
            s_rge = s_ori_rge.lower()
            print(s_rge)
            if s_rge.find('x') >= 0:
                s_rge = s_rge.replace(',', ';')
                s_xyz = s_rge
                # s_rge example: x=0;y=2;z=1
                s_rge = s_rge.replace('x=', 'x')
                s_rge = s_rge.replace('y=', 'y')
                s_rge = s_rge.replace('z=', 'z')
                print(f"'{s_rge}' {type(s_rge)} ")
                items = s_rge.split( ';')
                nb_dim = len(items)
                s_idx += f"<DIM>,"
                for item in items:
                    for dim_char, idx in d_dim_char.items():
                        if item.find(dim_char) >= 0:
                            if f_nodef_dim[idx]:
                                # ok you can store value
                                try:
                                    d_dim_idx[dim_char] = int(item[1:])
                                    f_nodef_dim[idx] = False
                                except:
                                    a_gui.errorBox(title, f"Can't convert '{item}' in integer type, index string: {s_ori_rge}")
                                    return False, None, None, None
                            else:
                                a_gui.errorBox(title, f"{dim_char} appears two times ! {s_ori_rge}")
                                return False, None, None, None
                if f_nodef_dim[0] or f_nodef_dim[1]:
                    a_gui.errorBox(title, f"You must define 2 dimensions with x=?,y=?")
                    return False, None, None, None                   
            elif s_rge.find(':') >= 0: 
                s_idx += f"{s_rge},"
                f_def_sample_dim = False
            elif len(s_rge) == 0:
                s_idx += f"0,"
            else:
                s_idx += f"{s_rge},"
        print(s_idx)
        if f_def_sample_dim:
            a_gui.errorBox(title, "You must define the sample dimension with ':' or '10:'")
            return False, None, None, None
        # remove last ,
        s_idx = s_idx[:-1]
        for dim_char, idx in d_dim_char.items():
            s_temp_idx = s_idx.replace('<DIM>', str(d_dim_idx[dim_char]))
            try:
                slice_ = eval(f'np.s_[{s_temp_idx}]')
                l_data[idx] = data[slice_]
            except:
                a_gui.errorBox("ERROR", f"Slice {s_idx} not valid ?")
                return False, None, None, None
            if not isinstance(l_data[idx], np.ndarray):
                try:
                    l_data[idx] = l_data[idx].to_numpy()
                except:
                    a_gui.errorBox(title, "Can't convert in regular array")
                    return False, None, None, None
        s_slice = s_idx.replace('<DIM>', ' ('+s_xyz+') ')
        return True, l_data, s_slice , nb_dim
        
    def press_image():
        f_conv , data_xd , s_idx, nb_dim = get_slice_array()
        if not f_conv:
            return
        fig = plt.figure()
        if nb_dim == 2:
            plt.scatter(data_xd[0], data_xd[1])
        else:
            ax = fig.add_subplot(projection='3d')
            ax.scatter(data_xd[0], data_xd[1], data_xd[2])
        plt.title(title + f", range [{s_idx}]")
        plt.grid()
        plt.show()

    try:
        a_gui.destroySubWindow("point")
    except:
        pass
    a_gui.startSubWindow("point", f"BROOT plot point: {title}", modal=True, blocking=True)
    a_gui.setSize(1000, 300)
    a_gui.setExpand("both")
    ndim = data.ndim
    if ndim <= 1: 
        a_gui.errorBox(title, "Dimension of array must be => 2.")
        return 
    # Col 0
    a_gui.startFrame("point_LEFT", row=0, column=0)
    try:
        str_range = f"Shape {data.shape}"
    except:
        str_range = "Shape irregular"
    a_gui.addLabel("point_range", str_range, row=0, column=0)   

    for idx in range(ndim):
        n_entry = f"point_dim {idx}"
        a_gui.addLabelEntry(n_entry, row=idx + 1, column=0, label=f"dim {idx}")
        if idx == 0:
            a_gui.setEntry(n_entry, 'x=0;y=1')
        elif idx == 1:
            a_gui.setEntry(n_entry, ':')
        else:
            a_gui.setEntry(n_entry, '')
    a_gui.stopFrame()
    a_gui.addButton("Plot", press_image, row=ndim, column=0)
    a_gui.stopSubWindow()
    a_gui.showSubWindow("point")
    a_gui.remove
