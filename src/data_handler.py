import pandas as pd


class AppData():

    filename_raw: str = "data/data_raw.csv"
    filename_filtered: str = "data/data_filtered.csv"
    filename_inverted: str = "data/data_inverted.csv"

    def __init__(self):
        self.raw = pd.read_csv(self.filename_raw, )
        self.filtered = pd.read_csv(self.filename_filtered)
        self.inverted = pd.read_csv(self.filename_inverted)

def read_data() -> AppData:
    return AppData()