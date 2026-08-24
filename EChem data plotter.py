import numpy 
import pandas 
import matplotlib.pyplot as matplt

samples = {
    "Co-HCN": (r"C:\Users\muham\OneDrive\Desktop\EChem raw data\CoCoP MIH Project\Co_HNC\her 1.txt", "cyan"), 
    "Co/CoP-HCN 1:1": (r"C:\Users\muham\OneDrive\Desktop\EChem raw data\CoCoP MIH Project\Co_CoP_HNC 1to1\HER 1.txt", "red"), 
    "Co/CoP-HCN 1:5": (r"C:\Users\muham\OneDrive\Desktop\EChem raw data\CoCoP MIH Project\Co_CoP_HNC 1to5\her 1.txt", "green"), 
    "Co/CoP-HCN 1:10": (r"C:\Users\muham\OneDrive\Desktop\EChem raw data\CoCoP MIH Project\Co_CoP_HNC 1to10\her 1.txt", "purple")
}

figure, (graph1, graph2) = matplt.subplots(nrows=1, ncols=2, figsize=(12, 5))

area = 1
reference_potential =  +0.927

for label, (file_path, color) in samples.items():

    table = pandas.read_csv(file_path, skiprows=26, sep=",", names=["Potential","Current"])

    table ["Current_mA"] = table ["Current"]*1000/area

    table ["Corrected Potential"] = table ["Potential"] + reference_potential

    table ["Current_abs"] = table ["Current_mA"].abs()

    tafel_table = table[(table["Current_mA"] < 0) & (table["Current_mA"] >= -20)].copy()

    dY_dX = numpy.gradient(tafel_table["Current_mA"], tafel_table["Corrected Potential"])

    inflection_row = numpy.argmax(numpy.abs(dY_dX))

    inflection_voltage = tafel_table ["Corrected Potential"].iloc[inflection_row]

    graph1.plot(table["Corrected Potential"], table["Current_mA"], color=color, label=label, linewidth=1.5)

    graph1.plot(inflection_voltage, tafel_table["Current_mA"].iloc[inflection_row], "o", color=color, markersize=7)

    v_min = inflection_voltage - 0.1
    v_max = inflection_voltage + 0.1

    kinetic_region = tafel_table[(tafel_table["Corrected Potential"]>= v_min) & (tafel_table["Corrected Potential"]<= v_max)].copy()

    kinetic_region ["log_Current_mA"] = numpy.log10(kinetic_region["Current_abs"])

    slope, intercept = numpy.polyfit(kinetic_region["log_Current_mA"], kinetic_region["Corrected Potential"], 1)
    tafel_slope = abs(slope) * 1000  
    fit_line = slope * kinetic_region["log_Current_mA"] + intercept

    graph2.plot(kinetic_region["log_Current_mA"], kinetic_region["Corrected Potential"], color=color, linewidth=1.5)

    graph2.plot(kinetic_region["log_Current_mA"], fit_line, "--", color=color, label=f"{label} ({tafel_slope:.1f} mV/dec)", linewidth=2)

graph1.set_title("LSV graph")
graph1.set_xlabel("Potential (V)")
graph1.set_ylabel("Current density, j (mA/cm$^2$)")
graph1.legend()

graph2.set_title("Tafel plot")
graph2.set_xlabel("log j")
graph2.set_ylabel("Overpotential (V)")
graph2.legend()

matplt.tight_layout()
matplt.show()