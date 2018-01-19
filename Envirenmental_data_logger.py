import os.path
from pathlib import Path


class Envirenmental_data_logger(object):

    def __init__(self, file_path):
        self.file_path = file_path

    def log(self, entry_index, temperature, humidity, pressure):
        # check if the file exists, if so open it for appending, otherwire open it for write
        # file_path = Path(self.file_path)
        try:

            # if file_path.exists():
            if os.path.isfile(self.file_path):
                # if the file already exists open it appending
                self.fo = open(self.file_path, "a")
            else:
                # open/create a new file and add the field names
                self.fo = open(self.file_path, "w")
                self.fo.writelines("Index, Temperature(C), Relative Humidity (%), Atmospheric Pressure (mBar)" + " \n")

            self.fo.writelines(
                str(entry_index) + ", " + str(temperature) + ", " + str(humidity) + "," + str(pressure) + " \n")

            self.fo.close()
        except IOError:
            print(IOError)
            return False

        return True


print("before  Envirenmental_data_logger_unit_test()")

if __name__ == '__main__':
    print("before  Envirenmental_data_logger_unit_test()")
    # Envirenmental_data_logger_unit_test()
    obj_data_logger = Envirenmental_data_logger("log.txt")
    i = 0
    while i < 1000:
        i += 1
        print("writing index=" + str(1))
        if obj_data_logger.log(i, 2 + i, 3 + i, 4 + i):
            print("OK")
        else:
            print("NOT OK")

    fh = open("log.txt", "r")
    list_of_lines = fh.read()
    print(list_of_lines)












