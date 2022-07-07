#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 16:10:35 2022

@author: keith
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


To generate splitting curves for hydrogen

Based on paper 2014ApJS..212...26S

Data downloaded from  https://doi.org/10.18419/darus-2118


Initial version  keith Inight  3 July 2022



"""
import os
import sys
import pkgutil
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt

Rydberg_constant= 1.09677583e7

Gauss=4.70103e9
Halpha=1e10/(6564*Rydberg_constant)

"""
The following is extracted from table 1 in 2014ApJS..212...26S. For Halpha we need to know the 
quantum states (ni, m and pi) associated with level 2 and 3. For Hbeta we also need level 4

{Updated to include additional levels using data provided by Chris Manser }

"""

levels=[
        ['2','2p0','1','0' ,'-1'], 
        ['2','2p1','1','+1','+1'], 
        ['2','2p1','1','-1','+1'],         
        ['2','2s0','2','0' ,'+1'],  
        ['3','3d1','1','+1','-1'],
        ['3','3d1','1','-1','-1'],  
        ['3','3d2','1','+2','+1'],
        ['3','3d2','1','-2','+1'],  
        ['3','3p0','2','0' ,'-1'],
        ['3','3p1','2','+1','+1'],
        ['3','3p1','2','-1','+1'],  
        ['3','3d0','3','0' ,'+1'],
        ['3','3s0','4','0' ,'+1'],  
        ['4','4f2','1','+2','-1'],   
        ['4','4f2','1','-2','-1'],          
        ['4','4d1','2','+1','-1'],          
        ['4','4d1','2','-1','-1'], 
        ['4','4d2','2','+2','+1'],     
        ['4','4d2','2','-2','+1'], 
        ['4','4f0','3','0' ,'-1'], 
        ['4','4f1','3','+1','+1'], 
        ['4','4f1','3','-1','+1'], 
        ['4','4p0','4','0' ,'-1'], 
        ['4','4p1','4','+1','+1'], 
        ['4','4p1','4','-1','+1'], 
        ['4','4d0','5','0' ,'+1'],
        ['4','4s0','6','0' ,'+1'],
        ['5','5f2','2','2' ,'-1'],
        ['5','5f2','2','-2','-1'],
        ['5','5g1','3','1' ,'-1'],
        ['5','5g1','3','-1','-1'],
        ['5','5g2','3','2' ,'+1'],
        ['5','5g2','3','-2','+1'],
        ['5','5d1','4','1' ,'-1'],
        ['5','5d1','4','-1','-1'],
        ['5','5d2','4','2' ,'+1'],
        ['5','5d2','4','-2','+1'],
        ['5','5f0','5','0' ,'-1'],
        ['5','5f1','5','1' ,'+1'],
        ['5','5f1','5','-1','+1'],
        ['5','5p0','6','0' ,'-1'],
        ['5','5p1','6','1' ,'+1'],
        ['5','5p1','6','-1','+1'],
        ['5','5g0','7','0' ,'+1'],
        ['5','5d0','8','0' ,'+1'],
        ['5','5s0','9','0' ,'+1'],
        ['6','6h2','3','2' ,'-1'],
        ['6','6h2','3','-2','-1'],
        ['6','6f2','4','2' ,'-1'],
        ['6','6f2','4','-2','-1'],
        ['6','6g1','5','1' ,'-1'],
        ['6','6g1','5','-1','-1'],
        ['6','6g2','5','2' ,'+1'],
        ['6','6g2','5','-2','+1'],
        ['6','6d1','6','1' ,'-1'],
        ['6','6d1','6','-1','-1'],
        ['6','6d2','6','2' ,'+1'],
        ['6','6d2','6','-2','+1'],
        ['6','6h0','7','0' ,'-1'],
        ['6','6h1','7','1' ,'+1'],
        ['6','6h1','7','-1','+1'],
        ['6','6f0','8','0' ,'-1'],
        ['6','6f1','8','1' ,'+1'],
        ['6','6f1','8','-1','+1'],
        ['6','6p0','9','0' ,'-1'],
        ['6','6p1','9','1' ,'+1'],
        ['6','6p1','9','-1','+1'],
        ['6','6g0','10','0' ,'+1']
       ]



level_set=pd.DataFrame.from_records(levels)
level_set.columns=['level','name','nu','m','pi']

def get_Zeeman(level1,level2):
    """
    

    Parameters
    ----------
    level1 : TYPE integer
        The hydrogen energy level prior to transition
    level2 : TYPE integer
        The hydrogen energy level after transition

    Returns
    -------
    results : pandas dataframe
        Three columns - 
            An index to the line
            The wavelength (in Angstrom)
            The magnetic field (in MG)

    """

    Level1=str(level1)
    Level2=str(level2)
    results=pd.DataFrame([])
    counter=0
    for l1 in level_set.query('level==@Level1').itertuples():
        for l2 in level_set.query('level==@Level2').itertuples():
    
            try:
                m_transition="m_"+l1.m+'_to_'+l2.m
                pi_transition='pi_z_'+l1.pi+'_to_'+l2.pi
                nu_transition='nu_'+l1.nu+'_to_'+l2.nu+'.tsv'
               
                filename=os.sep.join([os.path.dirname(__file__),'transitions',m_transition,pi_transition,nu_transition])
                df1=pd.read_csv(filename,delim_whitespace=True,skiprows=1)
                # The following approach is to allow for the case where this package
                # is zipped or otherwise compressed. A simple file open would then not work. 
                # The pkgutil utility is specifically designed to get round this and 
                #delivers a file as a byte string. BytesIO then presents this byte string as a file.                

                #data=pkgutil.get_data("Snippet_Zeeman_splitting",\
                 #                     os.sep.join(['transitions',m_transition,pi_transition,nu_transition]))
                #df1=pd.read_csv(BytesIO(data),delim_whitespace=True,skiprows=1)
                df1.columns=['beta', 'transition_energy_[Ry]', 'dipole_strength',
                       'initial_state_energy_[Ry]']  
                df1['wave']=1e10/(df1['transition_energy_[Ry]']*Rydberg_constant)
                df1['B']= df1['beta']*Gauss*1e-6
                df1['line']=counter

                results=pd.concat([results,df1[['line','wave','B']]])
            except:
    
                pass
            counter+=1
    return results





if (__name__ == '__main__'):
    # Example plot of Halpha
    dfx=get_Zeeman(2,3)

    lines= set(dfx['line'])
    for line in lines:
        dfy=dfx.query('line==@line')

        plt.plot(dfy['wave'],dfy['B'],'-',color='green') 
        plt.xlim(5500,7500)
        plt.ylim(0,50)
        plt.ylabel('B (MG)')
    plt.show()

