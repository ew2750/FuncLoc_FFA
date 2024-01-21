# FuncLoc_FFA localizer task for TRAITS_HIGHDIM fMRI scan
This is a psychopy coding version of FFA_localizer, part of the Functional localizer for fMRI scan, this python version is more stable to run during the fMRI scan than the MatLab version. 

For the original FuncLoc repository, please see https://github.com/jmtyszka/FuncLoc 

All parameters remain unchanged. 

## Command Line Input

<ins>conda activate psychopy</ins> (if you are on scanning laptop)

<ins>python FunLoc.py {subj_id} {# runs}</ins>

In the command line:
- sys.argv[1]=subj_id 
- sys.argv[2]=how many runs

Example:
> python FunLoc_FFA.py 005 2

You will run participant 005 for 2 runs. After the first run ends, it will wait for scanner. 

## Scanner trigger/button box configuration

Scanner trigger = **5**

The button box **Blue Button = 1**

MacOS system used to develop the code. 


