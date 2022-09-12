from .TelegramBot import TelegramBot
from .CSV import CSV
from .interfaceSelenium import InterfaceSelenium
import csv
from .billing import Analysis


class Service:
    """Class on managing the main logic of the program"""

    @classmethod
    def __init__(cls):
        cls.main()

    @classmethod
    def main(cls):
        """Main logic program"""
        try:
            TelegramBot.send_status_start()
            InterfaceSelenium.vcloud_connections()
            dict_url_vdc = InterfaceSelenium.get_dict_ord_vdc_url()
            data = InterfaceSelenium.get_list_resource_vdces(dict_url_vdc)
            CSV(data)
            TelegramBot.send_status_200()

            try:
                with open('file accounting.csv') as file:
                    file = csv.reader(file, delimiter=',')
                    file = list(file)
                    file1 = file[-2][0]
                    print(file1)
                    file2 = file[-1][0]
                    print(file2)
                    f = Analysis(f'B:/MonitoringResource54e/Result_resource54e/{file1}', f'B:/MonitoringResource54e/Result_resource54e/{file2}')
                    f.main()
                    TelegramBot.send_status_billding()

            except EOFError:
                TelegramBot.send_status_billding_400()

        except Exception as error:
            print(error)
            TelegramBot.send_status_400()
        finally:
            InterfaceSelenium.close_connection()




