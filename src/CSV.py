import csv
import datetime


class CSV:
    """Class for working with CSV"""

    @classmethod
    def __init__(cls, dict_resource):
        cls.main(dict_resource)

    @classmethod
    def main(cls, list_resource):
        """Writing data to a file"""

        fieldnames = ["Name_VDC",
                      "CPU_Quota",
                      "CPU_Used",
                      "Memory_Quota",
                      "Memory_Used",
                      " Cortel Mgmt  used",
                      " Cortel Mgmt  quota",
                      " VCD SATA  used",
                      " VCD SATA  quota",
                      " VCD SSD HI  used",
                      " VCD SSD HI  quota",
                      " VCD SSD  used",
                      " VCD SSD  quota",
                      " * (Any)  used",
                      " * (Any)  quota",
                      " VCD NVME  used",
                      " VCD NVME  quota"]

        name_file = cls.get_date_for_name_file()

        with open('file accounting.csv', 'a') as file:
            csv.register_dialect('my_dialect', delimiter=';', lineterminator="\r")
            writer = csv.writer(file, delimiter=',', dialect='my_dialect')
            listV = [f'{name_file}.csv']
            writer.writerow(listV)

        with open(f'B:/MonitoringResource54e/Result_resource54e/{name_file}.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore', restval="0", delimiter=';')
            writer.writeheader()
            writer.writerows(list_resource)

    @classmethod
    def get_date_for_name_file(cls):
        """Formation of the file name based on the current date"""
        hour = datetime.datetime.today().hour
        minutes = datetime.datetime.today().minute
        day = datetime.datetime.today().day
        month = datetime.datetime.today().month
        year = datetime.datetime.today().year

        return f'{day}.{month}.{year}_{hour}.{minutes}'

