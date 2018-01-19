#!/usr/bin/python

__author__ = "Noreddine Kessa "
__license__ = "GPL"

import tkinter
from tkinter import *
import time

#
#This widget visualise a steam of data
#It extends the Canvas tkinter package
#It uses a FIFO to store the stream of data,a fixed number of data points is retained and displayed, 
#when the FIFO is full, the newest entry deletes the oldest.

class Chart(Canvas):

    #definition of color
    color_background = "black"
    color_data= "green2"
    color_text = "white"
    color_xy_axis = "RoyalBlue1"

    #padding for the xy axis
    padding_x_axis_left = 10
    padding_x_axis_right = 95
    padding_x_axis_bottom=7

    padding_y_axis_bottom = padding_x_axis_bottom
    padding_y_axis_top = 95
    padding_y_axis_left = padding_x_axis_left

    #Class constructor
    def __init__(self,master,*args,**kwargs):
        super(Chart,self).__init__(master=master,*args,**kwargs)
        self.number_of_points = 5
        self.title = "title"
        self.list_of_emlements = []
        self.configure(background='black')


    #call this function and pass a string that will be displayed as the title for the chart
    def set_title(self , title):
        self.title = title

    #pass an interget to this function to set the number of data points to be displayed
    def set_number_of_data_point(self , number_of_data_points):
        self.number_of_points = number_of_data_points

    #private function
    #To simplify calculation a scheme of 0 to 100 is used for both height and width
    #This function scales any number between 0 and 100 to width and height of the chart
    def __convert_x_y_to_pixel(self , x,y):

        w =float(self.cget("width"))
        h = float(self.cget("height"))

        #print (str(w)+ "====" + str(h))
        pxl_x =x*w/100
        pxl_y=-y*(h/100)+h

        return (pxl_x, pxl_y)
        # pixel


    #call this function to update the chart on the user interface
    def draw(self):
        self.delete('all')
        self.select_clear()
        self.__draw_x_y_axis()
        self.__draw_title()
        self.__draw_data()

    #private
    #draws a line the coordinates are from 0 to 100
    def __draw_p_line(self ,x1 ,y1 ,x2 ,y2,color):
        (px1,py1)= self.__convert_x_y_to_pixel(x1,y1)
        (px2, py2) = self.__convert_x_y_to_pixel(x2,y2)
        self.create_line(px1, py1,px2,py2 , fill=color)


    #private
    #draw a string any where on the Chart, the coordinates are from 0 to 100
    def __draw_p_text(self , x, y ,text  ):
        (px, py) = self.__convert_x_y_to_pixel(x, y)
        self.create_text(px, py ,text=text , fill=Chart.color_text)

    #private
    #draws the title on the chart
    def __draw_title(self):
        self.__draw_p_text(50 , Chart.padding_y_axis_top , text=self.title)

    #private
    #draws x y axis mark them
    def __draw_x_y_axis(self):

        #get the optimal min and max of the xy axis for the data to be displayed
        (axis_min_x, axis_min_y , axis_max_x , axis_max_y)=self.__find_axis_min_x_y_max_x_y()


        #draw x axis
        self.__draw_p_line(Chart.padding_x_axis_left , Chart.padding_x_axis_bottom
                         ,Chart.padding_x_axis_right,Chart.padding_x_axis_bottom ,color=Chart.color_xy_axis )

        #place the graticule line on the x axis
        i =0
        number_of_lines=5
        x_val_increments = (axis_max_x-axis_min_x)/number_of_lines
        x_val = axis_min_x
        x_increments=Chart.padding_x_axis_right-Chart.padding_y_axis_left
        x_increments/=number_of_lines
        x1=x2=Chart.padding_y_axis_left
        y1=Chart.padding_x_axis_bottom -1
        y2 = Chart.padding_x_axis_bottom + 1
        while i <number_of_lines+1 :
            self.__draw_p_line(x1,y1,x2,y2 , color=Chart.color_xy_axis )
            self.__draw_p_text(x1, y1 - 3, text=str(x_val)) #label the graticules
            x1+=x_increments
            x2=x1
            x_val+=x_val_increments
            i+=1

        #draw y axis
        self.__draw_p_line(Chart.padding_y_axis_left, Chart.padding_y_axis_bottom \
                     , Chart.padding_y_axis_left, Chart.padding_y_axis_top,color=Chart.color_xy_axis )

        #place on the graticule lines on the y axis
        i=0
        y_val_increments = (axis_max_y - axis_min_y) / number_of_lines
        y_val = axis_min_y
        y_increments = Chart.padding_y_axis_top-Chart.padding_y_axis_bottom
        y_increments/=number_of_lines
        y1=y2=Chart.padding_y_axis_bottom
        x1 = Chart.padding_y_axis_left-1
        x2 = Chart.padding_y_axis_left + 1
        while i < number_of_lines + 1:
            self.__draw_p_line(x1, y1, x2, y2,color=Chart.color_xy_axis )
            self.__draw_p_text(4, y1 , text=str(y_val)) #label the graticule
            y_val += y_val_increments
            y1+=y_increments
            y2=y1
            i+=1

    #clears all the data curently available in the FIFO
    def clear_data(self):
        self.list_of_emlements.clear()
        self.draw()


    #add a data point
    #this is how you stream data into
    #the value of x doesn't matter
    # y is the actual value of the parameter you want to visualize
    #This function also updates the user interface, no need to call self.draw()
    def add_point(self, x, y):

        if len(self.list_of_emlements) >= self.number_of_points:
            self.list_of_emlements.pop(0)
            self.list_of_emlements.append((x, y))
        else:
            self.list_of_emlements.append((x, y))

        i = 0
        while i < len(self.list_of_emlements):
            (x,y)=self.list_of_emlements[i]
            self.list_of_emlements[i]=(i+1, y)
            i+=1
        self.draw()

    #for debugging purposes, don't worry about it
    def __print_points(self):
        print("printing elements in the list:")
        for (x, y) in self.list_of_emlements:
            print("x=" + str(x) + ", y=" + str(y))

    #private
    #loops thru the list of data and finds min and max
    def __find_min_x_y_max_x_y(self):

        if len(self.list_of_emlements) == 0:
            return (0, 0, 0, 0)

        (min_x , min_y)=self.list_of_emlements[0]
        (max_x, max_y) = self.list_of_emlements[0]

        
        for (x, y) in self.list_of_emlements:
            if min_x > x :
                min_x =x

            if min_y > y:
                min_y =y

            if max_x < x :
                max_x =x

            if max_y < y:
                max_y =y

        return (min_x, min_y, max_x , max_y)


    #private
    #is called to render data on the chart
    def __draw_data(self):

        #do nothing if there is no data to render
        if len(self.list_of_emlements)==0:
            return

        # figure out a scheme from data to in the list to chart point

        #check if there is data to be processed
        if len(self.list_of_emlements)==0:
            return


        (axis_min_x, axis_min_y, axis_max_x, axis_max_y) = self.__find_axis_min_x_y_max_x_y()

        #do avoid divition by zero
        if (axis_max_x - axis_min_x)==0:
            axis_max_x+=5

        if (axis_max_y - axis_min_y)==0:
            axis_max_y+=5

        #calculate all the constants to conversions
        x_coef = (Chart.padding_x_axis_right - Chart.padding_x_axis_left) / (axis_max_x - axis_min_x)
        x_constant = Chart.padding_x_axis_left- x_coef*axis_min_x

        y_coef = (Chart.padding_y_axis_top - Chart.padding_y_axis_bottom) / (axis_max_y - axis_min_y)
        y_constant = Chart.padding_y_axis_bottom -y_coef*axis_min_y

        ##calculate data point for the first element
        (x,y)=self.list_of_emlements[0]
        px1= x * x_coef + x_constant
        py1= y * y_coef + y_constant

        #draw line by line
        for (x, y) in self.list_of_emlements:
           # print("px1="+ str(px1) + ", py1=" + str(py1))
            px2 = x * x_coef + x_constant
            py2 = y * y_coef + y_constant
            self.__draw_p_line(px1,py1,px2,py2,color=Chart.color_data)
            px1=px2
            py1=py2

        #write the data of the last element
        (x,y)=self.list_of_emlements[len(self.list_of_emlements) -1]
        px1 = x * x_coef + x_constant
        py1 = y * y_coef + y_constant
        #determine if you need to draw above or below the data point
        if py1 > 50 :
            py1-=5
        else :
            py1+=5
        px1+=1

        self.__draw_p_text(px1, py1 , text=str(y))

    # private
    # Find the bounds of the X y axis so all the data is displayed optimally
    def  __find_axis_min_x_y_max_x_y(self):
        if len(self.list_of_emlements) == 0:
            return (0, 0, 5, 5)

        (min_x, min_y, max_x, max_y) = self.__find_min_x_y_max_x_y()

        #find the x axis lowest value divisible by 5
        remander = min_x%5
        axis_min_x=min_x - remander

        #find the y axis lowest value divisible by 5
        remander = min_y % 5
        axis_min_y = min_y - remander


        #find the optimal x axis highest value divisible by 5
        remander = max_x % 5
        if remander==0:
            axis_max_x = max_x
        else:
            axis_max_x = max_x + (5-remander)

        # find the optimal y axis highest value divisible by 5
        remander = max_y % 5
        if remander==0:
            axis_max_y = max_y
        else:
            axis_max_y = max_y + (5 - remander)

        return (axis_min_x, axis_min_y, axis_max_x, axis_max_y)




#this is a test bench for the Chart class
if __name__ == '__main__':
    print("this is main.")
    root = Tk()
    chart = Chart(root, width=600, height=200, bg="white" )
    chart.draw()
    chart.pack()
    num = 0
    while num < 10:
        chart.add_point(x=num + 1000, y=num + 2000)
        (min_x, min_y, max_x, max_y) = chart.__find_min_x_y_max_x_y()
        chart.__print_points()
        print("min x=" + str(min_x) + ", min y=" + str(min_y) + ", max x =" + str(max_x) + ", max y=" + str(max_y))
        (axis_min_x, axis_min_y, axis_max_x, axis_max_y) = chart.__find_axis_min_x_y_max_x_y()
        print("axis_min x=" + str(axis_min_x) + ", axis_min y=" + str(axis_min_y) + ", axis_max x =" + str(
            axis_max_x) + ", axis_max y=" + str(axis_max_y))

        num += 1
    chart.draw()
    root.mainloop()