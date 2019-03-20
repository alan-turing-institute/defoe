import os
from datetime import datetime
filepath = 'bl_data.txt'  
date_start= datetime.strptime('18500101' ,'%Y%m%d')
date_end= datetime.strptime('19150101','%Y%m%d')
with open(filepath) as fp:  
   line = fp.readline()
   while line:
       path=line.split()
       file_name=os.path.basename(line)
       filen=file_name.split("_")[1]
       filename=filen.split(".xml")[0]
       date_filename= datetime.strptime(filename,'%Y%m%d')
       if date_start <= date_filename < date_end:
           print("{}".format(line.strip()))
       line = fp.readline()
