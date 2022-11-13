# Introduction

Limasse (Lambda Ion Mass Explorer) is a python software first developed to help glycobiologists in the analysis of mass mpecter of permethylated O-glycan mix.

# Requirements

Limasse has been developed on Python 3.10.6 and need the following modules:
- pandas
- openpyxl
- seaborn
- pyqt5

# Installation

To use Limasse, open the file "limasse.py" in Python 3.10.

# How does it work
## Ion-filter
### Description
The ion filter takes an xlsx file as entry made out of mass specter. To work, it first needs to design ion library (see Ion library). Because of devices accuracy error, the mass specter are match against the ion library with an error of +/-0.05%. Example: ion = 534.2881, Accepted ions are between [534.2881\*0.9995,534.2881\*1.0005] = [534.0209,534.5552].
The script return as output an xlsx file with:
- the ions (or their compositions depending on how you built the ion library)
- the mass of the found ions
- the intensity of found ion
- the level of acceptation of ions (see Data Analysis)
If the script doesn't find any ion, it will indicate which sheets are empty and those sheets will be remove of the output.

### How using it
- First, select a file for analysis. This file contains information such as "m/z" and "intens.". It was first designed to take information format by flexanalysis software. 
- Then select your ion library (see ion library for it's building)
- You can run the script by pressing "run ion analysis"
- If you want to see all your library, you can press on "Generate library"
### Ion library
To run, the script needs ion library format in csv file (with "," as delimiter). You can find example of such ion library in the folder "ion library", folder where you must put your new library. The column the most on the right must contains your m/z, with requiered adducts. All the columns on the left contains the name of the ion OR its composition.
### Output
The output must be check in order to remove non-existing ions and check for duplications. Duplications result in the fact that multiple ion can have the same m/z, therefore put "n" in the "acceptation" column, where n is the number of duplicate, and 0 to remove non-existing ions.
### Common error
Be careful to put the index "m/z" on A1 in your excel file

## Data analysis
### Description
It takes as entry the modified output of the Ion-filter (with acceptation column modified), and gives as output 3 files witch name consensus must be written in place of "Set your file name".
### How to use it
To use it, load your input, select the ouput folder (where the files will be save), change the file name consensus and press "Mass analysis".
### Output
The three ouputs consist in an aligment file (needed for the 3rd module) and 2 files where you have each mass specter and the percentage of each ion in the specter.
### Common error:
Complete the acceptation column with diligence
## Alignment analysis
### Introduction
This module takes as input the "alignment file" of "Data analysis", but you can add an "information file" which consist of a file where you have all the information about the alignment data (see "Information file"). The purpose of this module is to analyze you're ions knowing their classes, types or belonging.
### How to use it
- First, select you're alignment file and information file (optionnal, see "information file")
- Choose a class filter (see "class filter") OR check "all data" box if you want to analyze all ions
- Add which class you want to analyze, or add the m/z of a wanted ions (you must be rather accurate, it takes ions with an error of 0.1%) by writting it and pressing "add". If you made a mistake you can choose to remove the last add item, or clear the whole list.
- You can choose the deepness of the analyze you want
- You may also choose to select if you want to sum the different class or not.
- Finally, you can have a preview of your data, or start the analysis, consisting of some plotting tools.
### Class filter
If you want to analyze your ion knowing their classes, you have to make a csv file and pu it in the "ion classes" folder. See the example in the folder. Like previously, the column the most on the right must contains the "code" of your ion. The code is the name you put in the first "ion library". If you put a composition, it will be a/b/c/d.../z with a/b/c/d.../z the number of occurence of each components. and the left you can write it's class,type,order,localisation...
### Information file
To work, it needs as first line the same name as in "alignment file" (example: if in alignment file, the name of sample are "a" "b" "c", the first line of information file must countain "c" "b" "a", independently of how it's sorted. All data without it's peer will be lose. Be careful the matching is sensitive, "John" is different from "john". If a cell of your xslx is empty, the column where it belongs will be remove, be sure to have all the datas or take in consideration that some can be lose