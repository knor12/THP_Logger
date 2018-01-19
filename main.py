__author__ = "Noreddine Kessa "
__license__ = "GPL"

from chart import *
from random import randint
from perpetualTimer import perpetualTimer
import os.path
from  MS8607_02BA import *
from Envirenmental_data_logger import Envirenmental_data_logger


#this is the main class in the app. 
#It extends the ktinker Frame.
#It manages unser interface, timer, logging data to file, and it reads data from sensors over I2C
class THP_Logger(Frame):

    def __init__(self, title, master=None):
        Frame.__init__(self, master )
        self.grid(row = 50, column = 50, sticky = W)
        self.master.title(title)
        self.label = Label(self, text='Hello')
        self.createWidgets()
        self.Measurment_number =0
        self.isLogToFile=False
        self.LogIntervalSconds=10
        self.form_base_title = "NKessa THP Logger"
        self.winfo_toplevel().title(self.form_base_title)
        self.data_logger = Envirenmental_data_logger(file_path="log.csv")


    def createWidgets(self):
        padding =5
        
        #Instantiation of the temepature chart on the main form 
        self.chrtTemperature = Chart(self,bg="white" , width=1000, height=200)
        self.chrtTemperature.set_title("Temperature (C)")
        self.chrtTemperature.set_number_of_data_point(1000)
        self.chrtTemperature.grid(row=1, column=1, columnspan=10 ,padx=padding , pady=padding)
        self.chrtTemperature.draw()

        #Instantiation of the humidity chart on the main form
        self.chrtHumidity = Chart(self, bg="white", width=1000, height=200)
        self.chrtHumidity.set_title("Relative Humidity (%)")
        self.chrtHumidity.set_number_of_data_point(1000)
        self.chrtHumidity.grid(row=3, column=1,columnspan=10 ,padx=padding , pady=padding)
        self.chrtHumidity.draw()

        #Instantiation of the pressure chart on the main form
        self.chrtPressure = Chart(self, bg="white", width=1000, height=200)
        self.chrtPressure.set_title("Atmospheric Pressure (mBar)")
        self.chrtPressure.set_number_of_data_point(1000)
        self.chrtPressure.grid(row=5, column=1 , columnspan=10 ,padx=padding , pady=padding)
        self.chrtPressure.draw()

        #Instantiation of the start/stop button
        self.btnStartStop = Button(self , text="Start" , command=self.__btnStartStop_clicked)
        self.btnStartStop.grid(row=0, column=1)

        #Instantiation of the exit button 
        self.btnExit = Button(self, text="Exit" )
        self.btnExit.bind("<Button-1>", self.__btnExit_clicked)
        self.btnExit.grid(row=0, column=2)

        #Instantiation of the clear button 
        self.btnClear = Button(self, text="Clear" )
        self.btnClear.bind("<Button-1>", self.__btnClear_clicked)
        self.btnClear.grid(row=0, column=3)

        #Instantiation of the log to file button, it is also use to disable looging to file
        self.btnLogToFile = Button(self, text="Enable Logging")
        self.btnLogToFile.bind("<Button-1>", self.__btnLogToFile_clicked)
        self.btnLogToFile.grid(row=0, column=4)

        #Instantiation Label 
        self.lblLogInterval= Label(self, text="Interval(S)")
        self.lblLogInterval.grid(row=0, column=5)

        #Instantiation of the spinbox that provides a selection of measurment intervals in seconds
        self.spnLogInterval = Spinbox(self, values=(5,10,20,40,60,90,120,300,600))
        self.spnLogInterval.grid(row=0, column=6)


    def __btnLogToFile_clicked(self, event):
        print("log to file clicked")
        if self.btnLogToFile['text'] == "Enable Logging":
            self.btnLogToFile['text'] = "Disale Logging"
            self.isLogToFile= True
        else:
            self.isLogToFile = False
            self.btnLogToFile['text'] = "Enable Logging"


    def __btnClear_clicked(self , event):

        #clear all the charts from data
        self.chrtTemperature.clear_data()
        self.chrtHumidity.clear_data()
        self.chrtPressure.clear_data()


    def __btnStartStop_clicked(self):
        if self.btnStartStop['text']=="Start":
            self.btnStartStop['text']="Stop"
            self.__start_acquiring()

        else:
            self.btnStartStop['text']="Start"
            self.__stop_acquiring()


    def __start_acquiring(self):
        self.log_entry_index =0
        self.LogIntervalSconds = int(self.spnLogInterval.get())
        self.__t = perpetualTimer(self.LogIntervalSconds , self.timer_call_back)
        self.__t.start()
        self.btnLogToFile.config(state=DISABLED)
        self.spnLogInterval.config(state=DISABLED)
        if self.isLogToFile == True:
            self.log_file_path = self.get_log_file_name()
            self.data_logger = Envirenmental_data_logger( file_path = self.log_file_path)
            title = "%s , logging data into file: %s" %( self.form_base_title , self.log_file_path)
            self.winfo_toplevel().title(title)
        #run the call back function once, it will later on be called by the timer.
        self.timer_call_back()

    def __stop_acquiring(self):
        self.__t.cancel()
        self.btnLogToFile.config(state=NORMAL)
        self.spnLogInterval.config(state=NORMAL)
        self.winfo_toplevel().title(self.form_base_title)

    def __btnExit_clicked(self , event):
        try:
            self.__t.cancel()
        except:
            print("exiting")

        print("exiting")
        self.destroy()
        exit()


    #this function is executed by a timer, repeatably, it reads data displays it and log it to file is needed
    def timer_call_back(self):

        #incremenat the index
        self.Measurment_number+=1
        x=self.Measurment_number

        #get the data from rando number generator if you are debugging the program
        #_temperature =randint(27, 31)
        #_humidity =randint(31, 42)
        #_pressure =randint(31, 32)

        #get real data from the sensors over I2C bus
        (_temperature , _humidity , _pressure ) = get_THP_from_MS8607()

        #update user interface
        self.chrtTemperature.add_point(x,_temperature )
        self.chrtHumidity.add_point(x, _humidity)
        self.chrtPressure.add_point(x, _pressure)

        #log data to csv file if logging is enabled
        if self.isLogToFile:
            _index = self.log_entry_index
            self.data_logger.log(entry_index=_index, temperature=_temperature, humidity=_humidity, pressure=_pressure)

        # increments the index to reflect seconds since start of acquisition
        self.log_entry_index+=self.LogIntervalSconds

    
    #this function gererates the csv log file name, it finds a file name that doesn't already exist. 
    def get_log_file_name(self):

        i = 1
        file_path_stem = "log_file"
        file_path = "%s_%s_.csv" %( file_path_stem , str(i))
        while os.path.isfile(str(file_path)):
            i+=1
            file_path = "%s_%s_.csv" % (file_path_stem, str(i))

        return file_path


#running the program starts here, main entry point
if __name__ == '__main__':
    root = THP_Logger(title="Main Form" )
    root.createWidgets()
    root.mainloop()