# this code reads multiple sets of raw data and turns it into a graph, with curves that represent the data (called a LSV graph).
# it then finds the region of each curve where the rate of change is highest (inflection point), 
# then it takes log of that data and plots it on another graph (called a Tafel graph).

import numpy 
import pandas 
import matplotlib.pyplot as matplt

samples = {
    "Co-HCN": (r"C:\Users\muham\OneDrive\Desktop\EChem raw data\CoCoP MIH Project\Co_HNC\her 1.txt", "cyan"), 
    "Co/CoP-HCN 1:1": (r"C:\Users\muham\OneDrive\Desktop\EChem raw data\CoCoP MIH Project\Co_CoP_HNC 1to1\HER 1.txt", "red"), 
    "Co/CoP-HCN 1:5": (r"C:\Users\muham\OneDrive\Desktop\EChem raw data\CoCoP MIH Project\Co_CoP_HNC 1to5\her 1.txt", "green"), 
    "Co/CoP-HCN 1:10": (r"C:\Users\muham\OneDrive\Desktop\EChem raw data\CoCoP MIH Project\Co_CoP_HNC 1to10\her 1.txt", "purple")
}
# this line pre-assigns names and colours to each file that needs to be read, so I can make one line of code that reads them all simultaneously
# if I didn't write this line I would have to make a separate code that reads each file 
# {} instead of [] creates a 'dictionary'. This allows you to store 'values' eg. colours, names and files to MULTIPLE 'keys'.
# here a 'key' would be Co/CoP, and you can store a 'value' like colour, name and file to it
# {} lets you do this^ for multiple different 'keys', such as Co/CoP-HNC and Co-HNC, making storing info for them easier.
# must use : instead of = for dictionary definitions 
# r tells python to ignore the backslashes inside brackets

figure, (graph1, graph2) = matplt.subplots(nrows=1, ncols=2, figsize=(12, 5))
# this line makes 2 blank graphs side by side. It calls on the plt.subplots function. 1 row and 2 columns make 2 adjacent graphs (duh!)
# 'fig, (g1, g2) =' on the left- this is called tuple unpacking. It lets you plot graph 1 and graph 2 separately later on in the code
# If you just called it 'figure' (one variable) instead of tuple unpacking, it would be a lot harder to talk directly to each graph
# (remember function(parameters))
# plt.subplots() is a matplotlib function that plots 2 graphs side-by-side
# need to put nrows and ncolumns parameters in plt.subplots so that it makes 2 graphs (ncols=2)

area = 1
reference_potential =  +0.927

for label, (file_path, color) in samples.items():
# this line loops through each file and does what the code below it says.
# it runs a 'for' loop for each of the samples (eg. Co/CoP)
# 'in samples' is the variable we made earlier, containing the labels for each file
# 'label' would be "Co-HCN", for example. Also 'file_path' would be her1.txt, and 'color' would be cyan 
#.items() makes python loop through the file_path and color too for each file name

    table = pandas.read_csv(file_path, skiprows=26, sep=",", names=["Potential","Current"])
    #this loads my data into a pandas table, I called it table, and pd.read_csv() is the function that actually does the reading
    #it names the two colums from my raw data so I can refer to them in the future code.
    #inside the brackets are just the paramaters specific to my raw data files

    table ["Current_mA"] = table ["Current"]*1000/area
    #converts current from A (in the text) to mA/cm^2. creates a new variable that is equal to current (alr made variable) times 1000.

    table ["Corrected Potential"] = table ["Potential"] + reference_potential
    #shifts potential with added reference potential

    table ["Current_abs"] = table ["Current_mA"].abs()
    #makes current positive for log calculation

    tafel_table = table[(table["Current_mA"] < 0) & (table["Current_mA"] >= -20)].copy()
    #section of table that limits the current between 0 and -20 for kinetic region (the region we are focusing on)

    dY_dX = numpy.gradient(tafel_table["Current_mA"], tafel_table["Corrected Potential"])
    #using numpy to find the first derivative

    inflection_row = numpy.argmax(numpy.abs(dY_dX))
    #finds which row in my raw data set has the highest derivative/ rate of change

    inflection_voltage = tafel_table ["Corrected Potential"].iloc[inflection_row]
    #finds the actual voltage value where the highest rate of change is
    #iloc means Integer LOCation

    graph1.plot(table["Corrected Potential"], table["Current_mA"], color=color, label=label, linewidth=1.5)
    #plots graph 1 (LSV graph)

    graph1.plot(inflection_voltage, tafel_table["Current_mA"].iloc[inflection_row], "o", color=color, markersize=7)
    #marks the point on graph 1 that has the highest rate of change

    v_min = inflection_voltage - 0.1
    v_max = inflection_voltage + 0.1
    #setting limits around the inflection point (+/- 0.1V)

    kinetic_region = tafel_table[(tafel_table["Corrected Potential"]>= v_min) & (tafel_table["Corrected Potential"]<= v_max)].copy()
    #made a variable extracts raw data within +/- 0.1V of inflection point, and makes a copy of that data
    #.copy() creates a copy of the raw data so that it doesn't change the original data (which i need for graph 1)

    kinetic_region ["log_Current_mA"] = numpy.log10(kinetic_region["Current_abs"])
    #calculates log of current in kinetic region (for Tafel plot)
    #uses numpy

    graph2.plot(kinetic_region["log_Current_mA"], kinetic_region["Corrected Potential"], color=color, label=label, linewidth=1.5)
    #plots graph 2 (tafel plot)
    #why is ["Corrected Potential"] needed after kinetic_region?

graph1.set_title("LSV graph")
graph1.set_xlabel("Potential (V)")
graph1.set_ylabel("Current density, j (mA/cm$^2$)")
graph1.legend()
#formatting graph 1 (LSV graph)
#need to use set_ when making subplots (like graph1 and graph2)

graph2.set_title("Tafel plot")
graph2.set_xlabel("log j")
graph2.set_ylabel("Overpotential (V)")
graph2.legend()
#formatting graph 2 (Tafel plot)

matplt.show()