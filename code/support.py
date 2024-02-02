from csv import reader


def import_csv_layout(path):
    layout = []
    with open(path) as file:
        parsed = reader(file, delimiter=',')
        for row in parsed:
            layout.append(list(row))

        return layout
