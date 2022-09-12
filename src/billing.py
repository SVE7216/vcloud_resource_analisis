import csv
from datetime import date, timedelta


class Analysis:
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2

    def main(self):
        with open(self.file1) as file1, open(self.file2) as file2:
            file1 = csv.reader(file1, delimiter=';')
            file2 = csv.reader(file2, delimiter=';')
            file1 = list(file1)
            file2 = list(file2)

            list_krit = [1, 3, 6, 8, 10, 12, 14, 16]
            dict_krit = {
                1: 'CPU',
                3: 'Memory',
                6: 'Cortel Mgmt',
                8: 'VCD SATA',
                10: 'VCD SSD HI',
                12: 'VCD SSD',
                14: '* (Any)',
                16: 'VCD NVME'
            }
            print('1')
            count_row1=0
            for row2 in file2:
                for row1 in file1:
                    if count_row1 == 0:
                        count_row1 = count_row1 + 1
                        continue
                    if row2[0] == row1[0]:
                        for item in list_krit:
                            if row1[item] == "Unlimited" or row2[item] == "Unlimited":
                                continue
                            else:
                                flag = float(row2[item].replace(',', '.'))-float(row1[item].replace(',', '.'))

                                if flag > 1:
                                    value = float(row2[item].replace(',', '.')) - float(row1[item].replace(',', '.'))
                                    day = date.today() - timedelta(days=1)
                                    list_billing = [day, row1[0], "Increase", dict_krit[item], value]
                                    self.writer_billing(list_billing)
                                elif flag < 0:
                                    value = float(row2[item].replace(',', '.')) - float(row1[item].replace(',', '.'))
                                    day = date.today() - timedelta(days=1)
                                    list_billing = [day, row1[0], "Decrease", dict_krit[item], value]
                                    self.writer_billing(list_billing)

    def writer_billing(self, row_billing):
        csv.register_dialect('my_dialect', delimiter=';', lineterminator="\r")
        with open('B:/MonitoringResource54e/billing.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, 'my_dialect')
            writer.writerow(row_billing)

