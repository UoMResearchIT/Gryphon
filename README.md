# Gryphon
Outlier removal algorithm written in Python.

## Release Notes
v1.0.0 -- Initial release.

## Prerequisites
 - [Python 3](https://www.python.org/downloads/) must be installed to run this script.
 - You will need to have the `numpy` library installed which you can install using `pip` which comes with most Python installers.
 - Your input file must be prepared so it conforms with the [Input File Format](#input-format).
 - The input file directory must also be writable by the script to allow creation of the output file.

## Usage
The script can be run from the command line. You must supply a single command line argument indicating the path of the input file to use. The example commands below assume that the Python executables are on the current path. You may need to manually add the Python directory to the PATH environment variable if it wasn't added automatically during the installation of Python.

Linux (bash):
```bash
python3 gryphon.py <path_to_input_file>
```

Windows (cmd):
```batch
python gryphon.py <path_to_input_file>
```

By default, the script generates the output file in the same directory as the input file. It has the same name and extensions but appends `_filtered` to the end of the input file name.

## Input Format
The input file must contain each set of measurements as separate rows. All measurements in a set must be pipe-separated (`|`). The subject to which the measurements are attached (known as the _Set ID_ must be pre-pended to the measurements on the row. It is expected that each subject will have multiple sets of measurements and hence the same _Set ID_ must be used for each set. An example input file is included in the repository and is shown below for reference. Note that `A` and `B` are the _Set IDs_ and each _column_ of data represents a particular measurement. Each _row_ represents a particular set of measurements.

```
A|10.0|13.2|12.5    <-- Measurements for subject A, set 1, measurement 1 = 10.0, measurement 2 = 13.2, measurement 3 = 12.5
A|11.0|14.2|13.5    <-- Measurements for subject A, set 2, measurement 1 = 11.0, measurement 2 = 14.2, measurement 3 = 13.5
A|12.0|15.2|14.5
A|13.0|16.2|15.5
A|14.0|17.2|16.5
B|15.0|18.2|17.5    <-- Measurements for subject B, set 1, measurement 1 = 15.0, measurement 2 = 18.2, measurement 3 = 17.5
B|16.0|19.2|18.5
B|17.0|10.2|19.5
B|18.0|11.2|10.5
B|19.0|12.2|11.5
```

## Output Format
The output format is essentially the same as the input format but with some additions. After processing, some measurements will be marked as retained (`R`) by the algorithm and the two most extreme values will be excluded (`X`). Furthermore, the algorithm will recompute the mean (`M`) and the variance (`V`) of the retained measurements. Each measurement written to the output file will be suffixed with an appropriate letter indicating whether it has been excluded or retained. Two extra lines will be added to the end of each group of measurement sets indicating the mean (suffixed `M`) and the variance (suffixed `V`) of the retained measurements. An example output file is included in the repository and is shown below for reference.

```
A|10.0X|13.2X|12.5X     <-- Measurements for subject A, set 1, all measurements excluded as outliers
A|11.0R|14.2R|13.5R     <-- Measurements for subject A, set 2, all measurements retained
A|12.0R|15.2R|14.5R
A|13.0R|16.2R|15.5R
A|14.0X|17.2X|16.5X
A|12.00M|15.20M|14.50M  <-- Measurements for subject A, mean values after processing
A|1.00V|1.00V|1.00V     <-- Measurements for subject A, variance values after processing
B|15.0X|18.2X|17.5R
B|16.0R|19.2X|18.5R
B|17.0R|10.2R|19.5R
B|18.0R|11.2R|10.5X
B|19.0X|12.2R|11.5X
B|17.00M|11.20M|18.50M
B|1.00V|1.00V|1.00V
```
