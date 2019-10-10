print("--SCRIPT DE RENOMBRAMIENTO DE FOTOGRAFIAS--")
#script por pablo.lopez
#version 1.1
#07-10-2019
#area: operaciones

from tkinter import Tk
from tkinter.filedialog import askdirectory
#path = askdirectory(title='Select Folder') # shows dialog box and return the path
#print(path)  

import glob, os
import pandas as pd
df = []
dfn = []
ruta = askdirectory(title='Select Folder')

my_file = export_file.split("/")[3]
os.chdir(ruta)

print("recovering file names...")

for file in glob.glob("*.jpg"):  
    dfn.append(file)
    data = file.split("_")[0:1] #split string into a list
    for temp in data:
        df.append(temp)
        
dfObj_sbjnum = pd.DataFrame(dfn) 
dfObj_sbjnum2 = pd.DataFrame(df) 

print("enter period")

periodo = str(input("enter period: "))

dfObj_sbjnum.rename(columns={0: 'NombreOriginal'}, inplace=True)

print("generating columns")

dfObj_sbjnum['Period'] = periodo
dfObj_sbjnum['Carpeta'] = ruta

dfObj_sbjnum['SbjNum'] = dfObj_sbjnum2
dfObj_sbjnum['Id'] = dfObj_sbjnum.groupby(['Period','SbjNum']).cumcount()+1
dfObj_sbjnum.applymap(str)


Formula = "ren "+ dfObj_sbjnum['NombreOriginal'].map(str) +" "+ dfObj_sbjnum['Period'].map(str) + '_' + dfObj_sbjnum['SbjNum'].map(str) + '_' + dfObj_sbjnum['Id'].map(str)+ '.jpg'
NewName = dfObj_sbjnum['Period'].map(str) + '_' + dfObj_sbjnum['SbjNum'].map(str) + '_' + dfObj_sbjnum['Id'].map(str)+ '.jpg'

dfObj_sbjnum['NewName']=NewName
dfObj_sbjnum['Formula'] = Formula

print("Generando script")

new_row = pd.DataFrame({'NombreOriginal':'', 'Period':'', 'Carpeta':'', 
                        'SbjNum':'', 'Id':'', 'NewName':'', 
                        'Formula':'cd/'+ruta}, index =[0]) 
  
df = pd.concat([new_row, dfObj_sbjnum.loc[:]]).reset_index(drop = True) 

new_row2 = pd.DataFrame({'NombreOriginal':'', 'Period':'', 'Carpeta':'', 
                        'SbjNum':'', 'Id':'', 'NewName':'', 
                        'Formula':'@echo off'}, index =[0]) 
  
df2 = pd.concat([new_row2, df.loc[:]]).reset_index(drop = True) 



#guarda la columna formula en archivo de texto que temina en .bat
with open('rename.bat', 'w') as f:
    for text in df['Formula'].tolist():
        f.write(text + '\n')
        
print("script created")
print("executing script")
import subprocess
subprocess.call([r'C:/Publica/Test\renombrar.bat'])
print("renamed images on route: "+ruta)