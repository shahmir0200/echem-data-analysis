#I made some catalysts in a lab and tested their performance using a Potentiostat
#This code reads the raw data from the Potentiostat and makes graphs that compare their performance
#The graphs are called LSV graphs (left) and Tafel plots (right). Both are used in electrochemistry to test catalyst performance

#1. importing pre-written code. Numpy does calculations, pandas reads tables, matplotlib plots graphs.
import numpy 
import pandas 
import matplotlib.pyplot as matplt

#2. this pre-assigns names and colours to each file that needs to be read, so I can make one line of code that reads them all simultaneously
samples = {
    "Co-HCN": (r"C:\Users\muham\OneDrive\Desktop\EChem raw data\CoCoP MIH Project\Co_HNC\her 1.txt", "cyan"), 
    "Co/CoP-HCN 1:1": (r"C:\Users\muham\OneDrive\Desktop\EChem raw data\CoCoP MIH Project\Co_CoP_HNC 1to1\HER 1.txt", "red"), 
    "Co/CoP-HCN 1:5": (r"C:\Users\muham\OneDrive\Desktop\EChem raw data\CoCoP MIH Project\Co_CoP_HNC 1to5\her 1.txt", "green"), 
    "Co/CoP-HCN 1:10": (r"C:\Users\muham\OneDrive\Desktop\EChem raw data\CoCoP MIH Project\Co_CoP_HNC 1to10\her 1.txt", "purple")
}
# if I didn't write this line I would have to make a separate code that reads each file 
# {} instead of [] creates a 'dictionary'. This allows you to store 'values' eg. colours, names and files to MULTIPLE 'keys'.
# here a 'key' would be Co/CoP, and you can store a 'value' like colour, name and file to it
# {} lets you do this^ for multiple different 'keys', such as Co/CoP-HNC and Co-HNC, making storing info for them easier.
# must use : instead of = for dictionary definitions 
# r tells python to ignore the backslashes inside brackets

#3. this line makes 2 blank graphs side by side. It calls on the plt.subplots function. 1 row and 2 columns make 2 adjacent graphs (duh!)
figure, (graph1, graph2) = matplt.subplots(nrows=1, ncols=2, figsize=(12, 5))
# 'fig, (g1, g2) =' on the left- this is called tuple unpacking. It lets you plot graph 1 and graph 2 separately later on in the code
# If you just called it 'figure' (one variable) instead of tuple unpacking, it would be a lot harder to talk directly to each graph
# (remember function(parameters))
# plt.subplots() is a matplotlib function that plots 2 graphs side-by-side
# need to put nrows and ncolumns parameters in plt.subplots so that it makes 2 graphs (ncols=2)

area = 1
reference_potential =  +0.927

#4. this line loops through each file and does what the code below it says.
for label, (file_path, color) in samples.items():
# it runs a 'for' loop for each of the samples (eg. Co/CoP)
# 'in samples' is the variable we made earlier, containing the labels for each file
# 'label' would be "Co-HCN", for example. Also 'file_path' would be her1.txt, and 'color' would be cyan 
#.items() makes python loop through the file_path and color too for each file name

    #5. this loads my data into a pandas table, I called it table
    table = pandas.read_csv(file_path, skiprows=26, sep=",", names=["Potential","Current"])
    #pd.read_csv() is the function that actually does the reading
    #it names the two colums from my raw data so I can refer to them in the future code.
    #inside the brackets are just the paramaters specific to my raw data files

    #6. converts current from A (in the text) to mA/cm^2. creates a new variable that is equal to current (alr made variable) times 1000.
    table ["Current_mA"] = table ["Current"]*1000/area

    #7. shifts potential with added reference potential
    table ["Corrected Potential"] = table ["Potential"] + reference_potential

    #8. makes current positive for log calculation
    table ["Current_abs"] = table ["Current_mA"].abs()

    #9. section of table that limits the current between 0 and -20 for kinetic region (the region we are focusing on)
    tafel_table = table[(table["Current_mA"] < 0) & (table["Current_mA"] >= -20)].copy()

    #10. using numpy to find the first derivative
    dY_dX = numpy.gradient(tafel_table["Current_mA"], tafel_table["Corrected Potential"])

    #11. finds which row in my raw data set has the highest derivative/ rate of change
    inflection_row = numpy.argmax(numpy.abs(dY_dX))

    #12. finds the actual voltage value where the highest rate of change is
    inflection_voltage = tafel_table ["Corrected Potential"].iloc[inflection_row]
    #iloc means Integer LOCation

    #13. plots graph 1 (LSV graph)
    graph1.plot(table["Corrected Potential"], table["Current_mA"], color=color, label=label, linewidth=1.5)

    #14. marks the point on graph 1 that has the highest rate of change
    graph1.plot(inflection_voltage, tafel_table["Current_mA"].iloc[inflection_row], "o", color=color, markersize=7)

    #15. setting limits around the inflection point (+/- 0.1V)
    v_min = inflection_voltage - 0.1
    v_max = inflection_voltage + 0.1

    #16. made a variable extracts raw data within +/- 0.1V of inflection point, and makes a copy of that data
    kinetic_region = tafel_table[(tafel_table["Corrected Potential"]>= v_min) & (tafel_table["Corrected Potential"]<= v_max)].copy()
    #.copy() creates a copy of the raw data so that it doesn't change the original data (which i need for graph 1)

    #17. calculates log of current in kinetic region (for Tafel plot)
    kinetic_region ["log_Current_mA"] = numpy.log10(kinetic_region["Current_abs"])
    #uses numpy

    #18. adding a linear regression line to each tafel value and performance in mV/decade (standard for electrochemistry tafel plots)
    slope, intercept = numpy.polyfit(kinetic_region["log_Current_mA"], kinetic_region["Corrected Potential"], 1)
    #numpy.polyfit(X,Y,1)- this tells numpy to make a straight line using my data points. 
    #1 means straight line (1st degree polynomial)
    #slope, intercept- another example of tuple unpacking, it returns 2 values (slope and intercept!)

    #19. converting gradient from V to mV, storing them as a variable
    tafel_slope = abs(slope) * 1000  

    #20. calculates y values using y=mx+c
    fit_line = slope * kinetic_region["log_Current_mA"] + intercept

    #21. plots graph 2 (tafel plot)
    graph2.plot(kinetic_region["log_Current_mA"], kinetic_region["Corrected Potential"], color=color, linewidth=1.5)

    #22. displays the linear regression lines and performances of each material in mV/decade
    graph2.plot(kinetic_region["log_Current_mA"], fit_line, "--", color=color, label=f"{label} ({tafel_slope:.1f} mV/dec)", linewidth=2)
    #.1f displays the values to 1 decimal place

#23. formatting graph 1 (LSV graph)
graph1.set_title("LSV graph")
graph1.set_xlabel("Potential (V)")
graph1.set_ylabel("Current density, j (mA/cm$^2$)")
graph1.legend()
#need to use set_ when making subplots (like graph1 and graph2)

#24. formatting graph 2 (Tafel plot)
graph2.set_title("Tafel plot")
graph2.set_xlabel("log j")
graph2.set_ylabel("Overpotential (V)")
graph2.legend()

#25. displays my graphs (finally!)
matplt.tight_layout()
matplt.show()