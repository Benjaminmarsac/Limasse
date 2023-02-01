# Introduction

Limasse (Lambda Ion Mass Explorer) is a python software first developed to help glycobiologists in the mass spectra analysis of permethylated O-glycan mixture.

# Requirements

Limasse has been developed on Python 3.10.6 and needs the following modules:
- pandas
- openpyxl
- seaborn
- pyqt5

# Installation

To use Limasse, open the file "limasse.py" in Python 3.10.

# How does it work
## Ion-filter
### Description
The ion filter takes an xlsx file as entry made out of  mass spectra. To work, it first needs to design an ion library (see Ion library). Because of device accuracy error, the  mass spectra are matched against the ion library with an error of +/-0.05%. Example: ion = 534.2881, Accepted ions are between [534.2881\*0.9995,534.2881\*1.0005] = [534.0209,534.5552].
The script returns an xlsx file as output with:
- the ions (or their compositions depending on how the ion library is built)
- the mass of the ions found
- the intensity of the ions found
- the level of acceptation of the ions (see Data Analysis)
If the script doesn't find any ion, it will indicate which sheets are empty and those sheets will be removed  from the output.

### How to use it
- First, select a file for analysis. This file contains information such as "m/z" and "intens.". It was first designed to take the information format with the flexanalysis software. 
- Then select your ion library (see ion library for its building)
- You can run the script by pressing "run ion analysis"
- If you want to see all your libraries  you can press on "Generate library"
### Ion library
To run, the script needs the ion library format in csv file (with "," as delimiter). You can find an example (OU examples) of such an ion library in the folder "ion library", your new library should be placed into this folder. The column the most on the right must contains your m/z, with requiered adducts. All the columns on the left contain the name of the ion OR its composition.

### Output
The output must be checked in order to remove non-existing ions and checked for duplications. Duplications result in the fact that multiple ions can have the same m/z, therefore put "n" in the "acceptation" column, where n is the number of duplicate, and 0 to remove non-existing ions.
### Common error
Be careful, your excel file must start on A1.

## Data analysis
### Description
It takes the modified output of the Ion-filter as entry (with the acceptation column modified), and gives 3 files as output whose name consensus must be written instead of "Set your file name".
### How to use it
To use it, load your input, select the ouput folder (where the files will be saved), change the file name consensus and press "Mass analysis".
### Output
The three ouputs consist in an alignment file (needed for the 3rd module) and 2 files where you have each  mass spectrum and the percentage of each ion in the spectrum ?
### Common error:
Complete the acceptation column with diligence.
## Alignment analysis
### Introduction
This module takes the "alignment file" of "Data analysis" as input but you can add an "information file" which consists of a file where you have the whole information about the alignment data (see "Information file"). The purpose of this module is to analyze your ions knowing their classes, types or belonging.
### How to use it
- First, select your alignment file and information file (optional, see "information file")
- Choose a class filter (see "class filter") OR check the "all data" box if you want to analyze all ions
- Add which class you want to analyze, or add the m/z of a wanted ion (you must be rather accurate as it takes ions with an error of 0.1%) by writing it and pressing "add". If you made a mistake you can choose to remove the last added item or clear the whole list
- You can choose the deepness of the  analysis you want
- You may also choose to select if you want to sum the different classes or not
- Finally, you can have a preview of your data, or start the analysis consisting of some plotting tools
### Class filter
If you want to analyze your ions knowing their classes, you have to make a csv file and put it in the "ion classes" folder. See the example in the folder. Like previously, the column the most on the right must contains the "code" of your ion. The code is the name you put in the first "ion library". If you put a composition, it will be a/b/c/d.../z with a/b/c/d.../z the number of occurence of each component and the left you can write  its class, type, order, localisation...
### Information file
To work, it needs the same name as in "alignment file" as the first line (example: if the name of sample are "a" "b" "c" in  the alignment file, the first line of information file must contain "c" "b" "a", independently of how  it is sorted. The whole data  without  their peer will be lost. Be careful as the matching is case-sensitive, "John" is different from "john". If a cell of your xslx file is empty, the column where it belongs will be removed, so be sure to have all the whole datas or take in consideration that some can be lost.