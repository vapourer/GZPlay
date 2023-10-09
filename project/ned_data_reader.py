import csv


class NedDataReader:

    def __init__(self, ned: str):
        self.ned = ned

    def extract(self) -> list[list[str]]:
        ned_rows = []

        with open(self.ned, newline='') as csvfile:
            ned_reader = csv.reader(csvfile, delimiter=',')

            for row in ned_reader:
                ned_rows.append(row)

        return ned_rows
