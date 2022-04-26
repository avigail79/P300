# import board
# from Marker import Marker
from recording import run_session
import mne
from constants import RECORDINGS_DIR
from g import get_epochs
from use_data import load_raw
import os

raw, rec_params = load_raw("2022-04-25--17-13-06_0")
d = raw.get_data(picks='Stim Markers')
X = [i for i in d[0] if i != 0]
print(len(X))
# raw_csd = mne.preprocessing.compute_current_source_density(raw.load_data())
# raw.plot().savefig(os.path.join(fig_path, "raw.png"))
# raw_csd.plot()
# run_session()
#
# raw = mne.io.read_raw_fif(RECORDINGS_DIR+"/2022-04-20--18-01-54_Avigail/raw.fif")
# events = mne.find_events(raw)

# print(events)
# print(raw.info)
# raw.plot()

# events = mne.find_events(raw, stim_channel='Stim Markers')
# print(events)

# mapping = {1: 'NON Target', 2: 'Target 1', 3: 'Target 2',
#            91: 'start with target 1', 92: 'start with target 2'}
# annot_from_events = mne.annotations_from_events(
#     events=events, event_desc=mapping, sfreq=raw.info['sfreq'],
#     orig_time=raw.info['meas_date'])
#
# raw.set_annotations(annot_from_events)
# events_from_annot, event_dict = mne.events_from_annotations(raw)
# print(event_dict)
# print(events_from_annot[:5])

# epochs, labels = get_epochs(raw, rec_params, markers=[1,2,11,91, 92])
#


