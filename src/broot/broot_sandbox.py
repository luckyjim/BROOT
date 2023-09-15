'''
Created on 19 juil. 2023

@author: jcolley
'''

from appJar import gui
import uproot as ur
import matplotlib.pyplot as plt
import numpy as np

data = [["Homer", "Simpson", "America", 40],
        ["Marge", "Simpson", "America", 38],
        ["Lisa", "Simpson", "America", 12],
        ["Maggie", "Simpson", "America", 4],
        ["Bart", "Simpson", "America", 14]]

def test_scroll():
    g_app = gui()
    if False:
        # BOF
        try:
            g_app.destroySubWindow("SW_PRINT")
        except:
            pass
        g_app.startSubWindow("SW_PRINT", f"DATA ", modal=True)
        g_app.startScrollPane("PRINT_SCROLL", disabled="horizontal")
        g_app.addMessage("D1", "test")
        g_app.stopScrollPane()
        g_app.stopSubWindow()
        g_app.showSubWindow("SW_PRINT")
    
def test_01(): 
    app = gui()
    app.addLabel("title", "Hello World")
    app.go()


def test_02():
    app = gui()
    select_file = app.openBox("BROOT open ROOT file", fileTypes=[('ROOT', '*.root'), ('ROOT', '*.r'), ("all", "*.*")])
    print(select_file)
    print(type(select_file))
    app.go()


def test_03():
    app = gui()
    
    app.startTabbedFrame("TabbedFrame")
    app.startTab("Tab1")
    app.addLabel("l1", "Tab 1 Label")
    app.stopTab()
    
    app.startTab("Tab2")
    app.addLabel("l2", "Tab 2 Label")
    app.stopTab()
    
    app.startTab("Tab3")
    app.addLabel("l3", "Tab 3 Label")
    app.stopTab()
    app.stopTabbedFrame()
    
    app.go()

    
def test_04():
    frt = '/home/jcolley/temp/grand/detector/data/td001234_f0007.root'
    frt = '/home/jcolley/temp/grand/detector/data/ad001234_f0180.root'
    drt = ur.open(frt)
    app = gui(f"Browser ROOT {frt.split('/')[-1]}")
    app.startTabbedFrame("TabbedFrame")
    t_idx = 0
    l_ttree = list(drt.keys()).copy()
    l_ttree.sort()
    for ttree in l_ttree:
        fttree = ttree.split(';')[0]
        app.startTab(fttree)
        app.startScrollPane(f"PANE_{fttree}")
        l_branch = list(drt[fttree].keys())
        l_branch.sort()
        for idx, branch in enumerate(l_branch):
            print(idx, t_idx, branch)
            val_br = drt[ttree][branch].array()
            if isinstance(val_br[0], str):
                app.addLabel(f"{t_idx}", f"{branch} : '{val_br[0]}'")
            else:
                try:
                    np_br = val_br.to_numpy()
                    app.addLabel(f"{t_idx}", f"{branch}: Array {np_br.ndim}D of {np_br.dtype} shape {np_br.shape}")
                except:
                    a_type_s = val_br.typestr.split('*')
                    a_shape = '(' + ','.join(a_type_s[:-1]) + ')'
                    app.addLabel(f"{t_idx}", f"{branch}: Array {val_br.ndim}D of {a_type_s[-1].strip()} shape irregular {a_shape}")
            t_idx += 1
        app.stopScrollPane()    
        app.stopTab()
    app.stopTabbedFrame()
    app.go()

    
def test_05():
    app = gui()
    
    # start initial pane
    app.startPanedFrame("p1")
    app.addLabel("l1", "Inside Pane 1")
    
    # start additional panes inside initial pane
    app.startPanedFrame("p2")
    app.addLabel("l2", "Inside Pane 2")
    app.stopPanedFrame()
    
    app.startPanedFrame("p3")
    app.addLabel("l3", "Inside Pane 3")
    app.stopPanedFrame()
    
    # stop initial pane
    app.stopPanedFrame()
    app.go()
    
    
def test_06():
    with gui("Updating Labels") as app:
        with app.tabbedFrame("Address Book"):
            for pos in range(len(data)):
                with app.tab(data[pos][0]):
                    app.entry(str(pos) + "fName", data[pos][0], label="First Name")
                    app.entry(str(pos) + "lName", data[pos][1], label="Last Name")
                    app.entry(str(pos) + "country", data[pos][2], label="Country")
                    app.entry(str(pos) + "age", data[pos][3], kind='numeric', label="Age")
        app.go()


def test_subwindow():
    
    def launch(win):
        app.showSubWindow(win)
    
    app = gui()
    
    # these go in the main window
    app.addButtons(["one", "two"], launch)
    
    # this is a pop-up
    app.startSubWindow("one", modal=True)
    app.addLabel("l1", "SubWindow One")
    app.stopSubWindow()
    
    # this is another pop-up
    app.startSubWindow("two")
    app.addLabel("l2", "SubWindow Two")
    app.stopSubWindow()
    
    app.go()


def plot_gui(app, data, title=""):

    def press_ok(pars):
        print(app.getRadioButton("PLOT"))
        print(app.getRadioButton("OPTION_0"))
        print(app.getEntry("dim 0"))
        s_idx = ""
        for idx in range(ndim):
            s_rge = app.getEntry(f'dim {idx}')
            s_idx += f"{s_rge},"
        s_idx= s_idx[:-1]
        print(s_idx)
        try:
            slice_ = eval(f'np.s_[{s_idx}]')
            plt.figure()
            plt.title(title+f", range [{s_idx}]")
            plt.plot(data[slice_])
        except:
            app.infoBox("ERROR", f"Slice {s_idx} not valid ?")
            return
        plt.xlabel('Sample')
        plt.grid()
        plt.show()
        
    # def press_cancel(pars):
    #     app.destroySubWindow("one")
    
    app.startSubWindow("one", f"Plot {title}", modal=True, blocking=True)
    app.setSize(600, 300)
    app.setExpand("both")
    ndim = data.ndim
    # Col 0
    app.startFrame("LEFT", row=0, column=0)
    app.addLabel(f"Range {data.shape}", row=0, column=0)
    for idx in range(ndim):
        app.addLabelEntry(f"dim {idx}", row=idx + 1, column=0)
    app.stopFrame()
    # Col 1
    app.startFrame("MIDDLE", row=0, column=1)
    app.addLabel("WIP", row=0, column=0)
    #app.addLabel("Plot", row=0, column=0)
    for idx in range(ndim):
        app.addRadioButton("PLOT",f"{idx}", row=idx + 1, column=0)
    app.stopFrame()
    # Col 2
    app.startFrame("RIGHT", row=0, column=2)
    #app.addLabel("Option (Not used WIP)", row=0, colspan=4)
    app.addLabel("Not used WorkInProgress (WIP)", row=0, colspan=4)
    for idx in range(ndim):
        app.addRadioButton(f"OPTION_{idx}", "Same", row=idx + 1, column=0)
        app.addRadioButton(f"OPTION_{idx}", "Sub", row=idx + 1, column=1)
        app.addRadioButton(f"OPTION_{idx}", "Slide", row=idx + 1, column=3)
        app.addRadioButton(f"OPTION_{idx}", "New", row=idx + 1, column=4)
    app.stopFrame()
    app.addButton("Ok", press_ok, row=ndim + 2, column=0)
    #app.addButton("Cancel", press_cancel, row=ndim + 2, column=1)
    app.stopSubWindow()
    app.showSubWindow("one")
    app.destroySubWindow("one")


def test_plot_gui():
    app = gui("test_plot_gui", "200x100")
    app.addLabel("m1", " MAIN")
    an = np.random.normal(0, 10, 6 * 4 * 20).reshape((6, 4, 1, 20))
    print(an)
    plot_gui(app, an, "test 1")
    plot_gui(app, an, "test 2")
    app.go()   

   
def test_table():
    
    def event_plot(s_but, i_line):
        print(f"Call event_plot() with pars {s_but} {i_line}")
        # for arg in argv:
        #     print("Next argument through *argv :", arg)
        # for key, value in kwargs.items():
        #     print(f"{key}: {value}")
        id_t = int(s_but.split('_')[-1])
        ttree = l_ttree[id_t].split(';')[0]
        branch = all_branch[id_t][i_line]
        print(f"{ttree} {branch}")
        print(type(ttree), type(branch))
        data = drt[l_ttree[id_t]][branch].array()
        data = data.to_numpy()
        print(s_but, s_but.find("Print"), data)
        if s_but.find("Print") >= 0:
            app.infoBox(f"DATA of {ttree}/{branch}", np.array2string(data))
        else:
            plt.figure()
            plt.title(f"DATA of {ttree}/{branch}")
            plt.plot(data.ravel())
            plt.xlabel('Sample')
            plt.grid()
            plt.show()
            app.startSubWindow("one", modal=True, blocking=True)
            app.addLabel("l1", "SubWindow One")
            app.stopSubWindow()
            app.showSubWindow("one")
            app.destroySubWindow("one")
            
    frt = '/home/jcolley/temp/grand/detector/data/td001234_f0007.root'
    # frt = '/home/jcolley/temp/grand/detector/data/ad001234_f0180.root'
    drt = ur.open(frt)
    app = gui(f"Browser ROOT {frt.split('/')[-1]}", "800x200")
    app.startTabbedFrame("TabbedFrame")
    app.setFont(18)
    t_idx = 0
    l_ttree = list(drt.keys()).copy()
    l_ttree.sort()
    all_branch = []
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
            idx = idx0 + 1
            idt = idx
            print(idx, t_idx, branch)
            l_act.append(f"Plot_{ttree}")
            val_br = drt[ttree][branch].array()
            if isinstance(val_br[0], str):
                tbl_br.append([idt, f"{branch}", f"'{val_br[0]}'", "String", "NA", f"{len(val_br[0])}"])
            else:
                try:
                    # NUMPY array
                    np_br = val_br.to_numpy()
                    # new_line = [idt, f"{branch}", f"array {np_br.ndim}D", f"{np_br.dtype}", f"{np_br.shape}", f"{np_br.nbytes:,}"]
                    new_line = [idt, f"{branch}", f"Array! Try Print/plot", f"{np_br.dtype}", f"{np_br.shape}", f"{np_br.nbytes:,}"]
                    print(np_br.size)
                    if np_br.size == 0:
                        new_line[2] = f"Empty !?"
                    elif np_br.size == 1:
                        new_line[2] = np_br.ravel()[0] 
                except:
                    # IRREGULAR array
                    a_type_s = val_br.typestr.split('*')
                    a_shape = '(' + ','.join(a_type_s[:-1]) + ')' 
                    a_shape = a_shape.replace(' ', '')
                    print(a_shape)
                    new_line = [idt, f"{branch}", f"array {val_br.ndim}D", f"{a_type_s[-1].strip()}", f"{a_shape}", f"{val_br.nbytes:,}"]
                tbl_br.append(new_line)
                if idx > 5: break
            t_idx += 1            
        l_button = [f"Print_{idx_t}", f"Plot_{idx_t}"]
        app.addTable(f"table{idx_t}", tbl_br, showMenu=True, action=event_plot, actionButton=l_button)
        app.stopTab()
    app.stopTabbedFrame()
    app.go()


if __name__ == '__main__':
    # test_subwindow()
    # test_table()
    test_plot_gui()
