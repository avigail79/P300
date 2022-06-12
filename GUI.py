from tkinter import *
from tkinter.messagebox import showinfo
from data_folder import create_session_folder, json_save


class GUI:
    def __init__(self):
        # window parameters
        self.win = Tk()
        self.win.geometry('500x300')
        self.Name = None
        self.entry_place = .4
        self.label_place = .1
        Label(self.win, text="Before we will start the session, enter here your details:", font=('Helvetica 13')) \
            .place(relx=.1, rely=.0)
        self.rec_params: dict = {}

        # name
        self.entry_name = Entry(self.win)
        self.entry_name.place(relx=self.entry_place, rely=.1)
        Label(self.win, text="Name:").place(relx=self.label_place, rely=.1)

        # synthtic
        self.use_synthetic = StringVar(self.win)
        synthetic_spin = Spinbox(self.win, values=['True', 'False'], textvariable=self.use_synthetic, width=20)
        self.use_synthetic.set('False')
        Label(self.win, text='Use synthetic board:').place(relx=self.label_place, rely=.2)
        synthetic_spin.place(relx=self.entry_place, rely=.2)

        # stimulus type
        self.stim = StringVar(self.win)
        stimulus_type_spin = Spinbox(self.win, values=['black_shapes', 'blue_shapes'], textvariable=self.stim, width=20)
        stimulus_type_spin.place(relx=self.entry_place, rely=.3)
        Label(self.win, text='Stimulus Type:').place(relx=self.label_place, rely=.3)

        # blocks
        self.entry_blocks = Entry(self.win)
        self.entry_blocks.place(relx=self.entry_place, rely=.4)
        Label(self.win, text="Number of blocks:").place(relx=self.label_place, rely=.4)

        # trials
        self.entry_trials = Entry(self.win)
        self.entry_trials.place(relx=self.entry_place, rely=.5)
        Label(self.win, text="Number of trials per block:").place(relx=self.label_place, rely=.5)


    def submit_button(self):
        # def check_validity():  # todo: add validation

        def get_valid_data():
            # check_validty()
            self.rec_params = {
                'Use synthetic': self.use_synthetic.get(),
                'Subject name': self.entry_name.get(),
                'Stimulus Type': self.find_stim_dict(),
                'trials_N': int(self.entry_trials.get()),
                'blocks_N': int(self.entry_blocks.get()),
                "odd percent": 0.14285714285714285,
                "get ready duration": 5,
                "calibration duration": 1,
                "StimOnset": 0.2,
                "interTime": 0.1
            }
            # save to json
            folder_path = create_session_folder(self.entry_name.get())
            json_save(folder_path, "params.json", self.rec_params)
            estimated_time = self.rec_params['blocks_N'] * self.rec_params['trials_N'] * self.rec_params['StimOnset'] \
                             * self.rec_params['interTime']
            showinfo("Inforamtion", f"The session will open in a few seconds. \nEstimated time for "
                                    f"{self.rec_params['blocks_N']} blocks:\n{float('{0:.2f}'.format(estimated_time))}")
            self.win.destroy()  # close the window

        Button(self.win, text="submit", command=get_valid_data).place(relx=.5, rely=.8)

    def find_stim_dict(self):
        stim_dict = {}
        if self.stim.get() == 'black_shapes':
            stim_dict = {"NON_TARGET": "black circle",
                         "TARGET_1": "black square",
                         "TARGET_2": "black triangle"
                        }
        elif self.stim.get() == 'blue_shpaes':
            stim_dict = { "NON_TARGET": "circle",
                          "TARGET_1": "square",
                          "TARGET_2": "triangular"
                        }
        return stim_dict

    def run_gui(self):
        self.submit_button()
        self.win.mainloop()
        return self.rec_params