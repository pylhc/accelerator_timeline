# Accelerator Timeline

In this package, the main parameters of major historical, modern and possible future accelerators are 
collected, including references to the origin of the collected data, into a single csv:

 -  [accelerator-parameters.csv](accelerator-parameters.csv).

## Installation 

This package is mostly for collecting and sharing the data of the accelerators within
the CSV file. 


To get the data, either download the [accelerator-parameters.csv](accelerator-parameters.csv) directly, 
or clone the repository via `git`, e.g.::

```
git clone https://github.com/pylhc/accelerator_timeline.git
```

## Example Scripts

In addition, small python scripts are provided to explore the data via and create Livingston-like plots plotly:
[interactive_charts.py](interactive_charts.py)
<br>
as well as for publication export to pdf via matplotlib:
[export_charts.py](export_charts.py) .


The requirements for the scripts can be found in the respective `requirements_*.txt` file.

![Center of Mass](images/energy.png)
![Luminosity](images/luminosity.png)
![LuminosityVsEnergy](images/luminosity-vs-energy.png)