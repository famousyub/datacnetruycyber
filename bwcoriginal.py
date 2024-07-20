
__version__ ='Py_V1.0.1'
print(__version__)
import re



import  os 
import sys 
import threading
import argparse
import tkinter as  tk 
import  sqlite3 as sq 

import datetime


import  sys 
import  re 


import logging as log 




min_  = -999 

max_  = 999



class LoggingOrion :
    
    
    def __init__(self , filenme):
        self.filename = filename 
        
    
    
    def writelog(self ,data) :
        
        
        with open (self.filename, "w+")     as  f :
            f.write(data)
            
            
            log.info(data)
            
            
    def writelog2(self, _o,  _n):
        
        log.info(_n)
        log.debug(_o)
        
         





tags_   ={}



def  extractTags (filename , t) :
    
    index_ = 0
    with open(filename , 'r')   as f :
        line  =  f.readline()
        
        
        while line  :
            
            
            tags_[f'tagname-{index_}'] = line 
        
            line  = f.readline()
    
    return   tags_
    
    


def  checkterminalOk(rr) :
    
    
    if rr.find("----->TEST Ok")!=-1 and "----->TEST Ok" in rr.split() :
        os.system("color 0a")
    elif rr.find("TEST KO") !=-1   and  "----->TEST KO" in rr.split() :
        os.system("color 0C")
        os.system("color 0c")
    elif rr.find("PASSAGE KO") != -1 : 
        os.system("color 0C")
    elif rr.find("PASSAGE OK") != -1 :
        os.system("color 0a")











x = datetime.datetime.now()
date_time = x.strftime("%m_%d_%Y_%H_%M_%S")




tags = [
    "VIOLATION_PERCENTAGE_VSA1" ,
    "OBW_PERCENTAGE_VSA1",
   # PK_EVM_DB_AVG_S1                                  :       -16.89 dB     (, -9.1)
   #POWER_DBM_RMS_AVG_S1
#g.write(f"Nom  : {nom}  Measurement : {power_} Unit : {unity_} LowerLimit : {min_} HigherLimit : {max_} Description : {step_} \n")  
]
dctnadra = {
    1: "Nom ",
    2: "Measurement",
    3: "Unit",
    4: "LowerLimit",
    5: "HigherLimit"
}


# Define functions to extract PER and POWER data
def extract_PER(line):
    matches = re.search(r'PER\s+:\s+(\d+\.\d+)\s+', line)
    if matches:
        return float(matches.group(1))
    return None

def extract_POWER(line):
    matches = re.search(r'POWER_\s+_\s+_\s+_\s+\s+:\s+(\d+\.\d+)\s+dBm\s+\(\s*(-?\d+\.\d+),\s*(-?\d+\.\d+)\)', line)
    #matches = re.search(r'POWER_DBM_RMS_AVG_S1\s+:\s+(\d+\.\d+)\s+dBm\s+\(\s*(-?\d+\.\d+),\s*(-?\d+\.\d+)\)', line)
    #matches = re.search(r'POWER_DBM_RMS_AVG_S1\s+:\s+(-?\d+\.\d+)\s+', line)
    if matches:
        return float(matches.group(1))
    return None



def extractmesurestags(line):
    parts  =  line .split()
    
    
    nom =""
    for tg in tags:
        if tg in parts :
            idx = parts.index(f"{tg}")
            nom = f"{parts[0]}_{parts[idx+1]}_{parts[idx+2]}_{parts[-2]}_{parts[-1]}"
            nom = nom.replace('.', '_')
            
    return nom    
    



def generate_nom(line):
    parts = line.split()
    print(parts)
    
    if set(['ANT1', 'ANT2', 'ANT3', 'ANT4']).intersection(set(parts)) == set(['ANT1', 'ANT2', 'ANT3', 'ANT4']):
        idx = parts.index("PER")
        nom = f"{parts[0]}_{parts[idx+1]}_{parts[idx+3]}"
        print(nom)
    elif "SPECTRUM" in parts:
        idx = parts.index("SPECTRUM")
        nom = f"{parts[0]}_{parts[idx+1]}_{parts[idx+2]}_{parts[-2]}_{parts[-1]}"
        nom = nom.replace('.', '_')
        nom = nom.replace("_VERIFY", "")
        pattern = r'_VERIFY'
        pattern2 = r'_EVM'

        # Replace "verify" and any preceding underscores with an empty string
        nom = re.sub(pattern, '', nom)
        nom = re.sub(pattern2, '', nom)
        print(nom)
        

    elif "PER" in parts:
        idx = parts.index("PER")
        
        print(parts)
        
        nom = f"{parts[0]}_{parts[idx+1]}_{parts[idx+2]}_{parts[-2]}_{parts[-1]}"
        nom = nom.replace('.', '_')
        nom = nom.replace("_VERIFY", "")
        pattern = r'_VERIFY'
        pattern2 = r'_EVM'

        # Replace "verify" and any preceding underscores with an empty string
        nom = re.sub(pattern, '', nom)
        nom = re.sub(pattern2, '', nom)
        p2=parts[0].replace(".","_")
        nom = f"{p2}_{parts[idx+1]}_{parts[idx+2]}_{parts[-2]}_{parts[-1]}"
        nom.replace(".","_")
    else:
        try :
            nom = parts[0].replace(".","_")
        except :
            nom ="RSSI"
    return nom


class Extractor:
    def __init__(self, filename, path):
        self.filename = filename
        self.path = path
        self.data = {"database": "mesure"}
        self.st = ''
        #extractTags(filename,'m')
        #print(tags_)

    def extractSteps(self, line):
        x = re.findall("\(\s", line)
        y = re.findall("\,\s\d", line)
        z = re.findall("\_\_", line)
        mm = ''
        if z:
            ch = line
            self.st = ''
            for i in range(len(ch)):
                if ch[i] == '_' and ch[i + 1] == '_':
                    break
                else:
                    if line.find('_VERIFY') != -1:
                        self.st = self.st + ch[i]
                        x = re.findall("\(\s", line)
                        y = re.findall("\,\s\d", line)
                        if x or y:
                            ch = line
                    
                    elif line.find('IMPLICIT_BEAMFORMING_') != - 1:
                        
                        print(line.split(" "))
                        self.st = self.st + ch[i]
                        x1 = re.findall("\(\s", line)
                        y1 = re.findall("\,\s\d", line)
                        if x1 or y1:
                            ch = line
                        
                        
                        print(self.st)
                    elif line.find("Verify_RSSI") != - 1:
                        self.st = self.st + ch[i]
                        x2 = re.findall("\(\s", line)
                        y2 = re.findall("\,\s\d", line)
                        if x2 or y2:
                            ch = line

    def extract(self, filesave):
        with open(self.filename, 'r') as f:
            line = f.readline()
            with open(f'{filesave}', 'w+') as g:
                while line:
                    line = str(line)
                    line = line.rstrip()
                    line = line.strip()
                    line = line.lstrip()
                    self.extractSteps(line)
                    if line.find('_VERIFY') != -1:
                        if self.st != "":
                            g.write(f"step : {self.st}")
                            g.write("\n")
                    elif line.find("IMPLICIT_BEAMFORMING_")!= - 1:
                        if self.st != "":
                            g.write(f"step : {self.st}")
                            print(self.st)
                            g.write("\n")
                    elif line.find("Verify_RSSI") != -1 :
                        if self.st != "":
                            g.write(f"step : {self.st}")
                            g.write("\n")
                        
                        
                            
                    
                    
                    for tg in tags:
                        if line.find(tg) != -1 and tg in line.split():
                            print(f"{tg} ++++++0")
                            splmespower = line.split()
                            unity_ = splmespower[3]
                            print("********" * 9)
                            
                            if unity_ == '%' :
                                max_ = 100 
                                min_  = 0
                           
                            if len(splmespower) > 6 :
                                min_ = splmespower[5]
                                max_= splmespower[6][:-1]
                            else :
                                if unity_ == '%' :
                                    max_ = 100 
                                    min_  = 0
                                
                            nom = generate_nom(self.st)
                            power_ =splmespower[2]
                            unity_ = splmespower[3]
                            step_= splmespower[0]
                            if unity_ == '%' :
                                max_ = 100 
                                min_ = 0
                                   
                            g.write(f"Nom  : {nom}  Measurement : {power_} Unit : {unity_} LowerLimit : {min_} HigherLimit : {max_} Description : {step_} \n")
                            print("POWER:", power_)
                            
                            
                    #POWER_DBM_RMS_AVG_S1
                    
                    # POWER_RMS_AVG_VSA1
                    #OBW_MHZ_VSA1
                    #Test Time = 2.539 s
                    
                    if line.find("OBW_MHZ_VSA1")!= -1 and  "OBW_MHZ_VSA1" in line.split():
                        print("********")
                        print(line.split())
                        import time 
                        #time.sleep(10)
                        print("okiiiiii" )
                        splmespower = line.split()
                        #print(splmespower)
                        print("********" * 9)
                        min_= -999
                        max = 999
                        if len(splmespower) > 6 :
                            min_ = splmespower[5]
                            max_= splmespower[6][:-1]
                        
                        else :
                            min_= -999
                            max = 999 
                        nom = generate_nom(self.st)
                        power_ =splmespower[2]
                        unity_ = splmespower[3]
                        step_= splmespower[0]
                        if unity_ == '%' :
                            max_ = 100 
                            min_  = 0
                        
                        g.write(f"Nom  : {nom}  Measurement : {power_} Unit : {unity_} LowerLimit : {min_} HigherLimit : {max_} Description : {step_} \n")
                        print("OBW_MHZ_VSA1:", power_)
                    
                    
                    if line.find("POWER_DBM_RMS_AVG_S1")!= -1 and  "POWER_DBM_RMS_AVG_S1" in line.split():
                        print("********")
                        print(line.split())
                        import time 
                        #time.sleep(10)
                        print("okiiiiii" )
                        splmespower = line.split()
                        #print(splmespower)
                        print("********" * 9)
                        min_= -999
                        max = 999
                        if len(splmespower) > 6 :
                            min_ = splmespower[5]
                            max_= splmespower[6][:-1]
                        
                        else :
                            min_= -999
                            max = 999 
                        nom = generate_nom(self.st)
                        power_ =splmespower[2]
                        unity_ = splmespower[3]
                        step_= splmespower[0]
                        if unity_ == '%' :
                            max_ = 100 
                            min_  = 0
                        g.write(f"Nom  : {nom}  Measurement : {power_} Unit : {unity_} LowerLimit : {min_} HigherLimit : {max_} Description : {step_} \n")
                        print("POWER:", power_)
                        
                    if line .find("RSSI_") != -1 and "RSSI_"  in line.split() :
                        print("********")
                        print(line.split())
                        import time 
                        #time.sleep(10)
                        print("okiiiiii" )
                        splmespower = line.split()
                        #print(splmespower)
                        print("********" * 9)
                        min_= -999
                        max = 999
                        if len(splmespower) > 6 :
                            min_ = splmespower[5]
                            max_= splmespower[6][:-1]
                        
                        else :
                            min_= -999
                            max = 999 
                        nom = generate_nom(self.st)
                        power_ =splmespower[2]
                        unity_ = splmespower[3]
                        step_= splmespower[0]
                        if unity_ == '%' :
                            max_ = 100 
                            min_  = 0
                        g.write(f"Nom  : {nom}  Measurement : {power_} Unit : {unity_} LowerLimit : {min_} HigherLimit : {max_} Description : {step_} \n")
                        print("RSSI:", power_)
                        
                    if line.find("POWER_RMS_AVG_VSA1")!= -1 and  "POWER_RMS_AVG_VSA1" in line.split():
                        print("********")
                        print(line.split())
                        import time 
                        #time.sleep(10)
                        print("okiiiiii" )
                        splmespower = line.split()
                        #print(splmespower)
                        print("********" * 9)
                        min_= -999
                        max = 999
                        if len(splmespower) > 6 :
                            min_ = splmespower[5]
                            max_= splmespower[6][:-1]
                        
                        else :
                            min_= -999
                            max = 999 
                        nom = generate_nom(self.st)
                        power_ =splmespower[2]
                        unity_ = splmespower[3]
                        step_= splmespower[0]
                        if unity_ == '%' :
                            max_ = 100 
                            min_  = 0
                        g.write(f"Nom  : {nom}  Measurement : {power_} Unit : {unity_} LowerLimit : {min_} HigherLimit : {max_} Description : {step_} \n")
                        print("POWER_DBM_RMS_AVG_S1:", power_)
                    
                    
                    
                    
                    
                    if line.find("EVM_DB_ALL") != -1 and "EVM_DB_ALL"  in line.split():
                        
                        print("********")
                        print(line.split())
                        import time 
                        #time.sleep(10)
                        print("okiiiiii" )
                        splmespower = line.split()
                        #print(splmespower)
                        print("********" * 9)
                        min_= -999
                        max_= 999
                        
                        if len(splmespower) > 6 :
                            try : 
                                min_ = splmespower[5]
                                max_= splmespower[6][:-1]
                            except :
                                min_ = -999 
                                max_ = 999
                        
                        else :
                            min_= -999
                            max = 999 
                        nom = generate_nom(self.st)
                        power_ =splmespower[2]
                        unity_ = splmespower[3]
                        step_= splmespower[0]
                        if unity_ == '%' :
                            max_ = 100 
                            min_  = 0
                        g.write(f"Nom  : {nom}  Measurement : {power_} Unit : {unity_} LowerLimit : {min_} HigherLimit : {max_} Description : {step_} \n")
                        print("EVM_DB_ALL:", power_)
                        
                    
                    if line.find("OBW_MHZ_VSA_1") != -1 and "OBW_MHZ_VSA_1" in line.split():
                        print("********")
                        print(line.split())
                        import time 
                        #time.sleep(10)
                        print("okiiiiii" )
                        splmespower = line.split()
                        #print(splmespower)
                        print("********" * 9)
                        min_= -999
                        max_= 999
                        
                        if len(splmespower) > 6 :
                            try : 
                                min_ = splmespower[5]
                                max_= splmespower[6][:-1]
                            except :
                                min_ = -999 
                                max_ = 999
                        
                        else :
                            min_= -999
                            max = 999 
                        nom = generate_nom(self.st)
                        power_ =splmespower[2]
                        unity_ = splmespower[3]
                        step_= splmespower[0]
                        if unity_ == '%' :
                            max_ = 100 
                            min_  = 0
                        g.write(f"Nom  : {nom}  Measurement : {power_} Unit : {unity_} LowerLimit : {min_} HigherLimit : {max_} Description : {step_} \n")
                        print("OBW_MHZ_VSA_1:", power_)
                    
                    checkterminalOk(line)
                    
                    if line.find("PK_EVM_DB_AVG_S1")!= -1 and  "PK_EVM_DB_AVG_S1" in line.split():
                        print("********")
                        print(line.split())
                        import time 
                        #time.sleep(10)
                        print("okiiiiii" )
                        splmespower = line.split()
                        #print(splmespower)
                        print("********" * 9)
                        min_= -999
                        max_= 999
                        
                        if len(splmespower) > 6 :
                            try : 
                                min_ = splmespower[5]
                                max_= splmespower[6][:-1]
                            except :
                                min_ = -999 
                                max_ = 999
                        
                        else :
                            min_= -999
                            max = 999 
                        nom = generate_nom(self.st)
                        power_ =splmespower[2]
                        unity_ = splmespower[3]
                        step_= splmespower[0]
                        if unity_ == '%' :
                            max_ = 100 
                            min_  = 0
                        g.write(f"Nom  : {nom}  Measurement : {power_} Unit : {unity_} LowerLimit : {min_} HigherLimit : {max_} Description : {step_} \n")
                        print("PK_EVM_DB_AVG_S1:", power_)
                    
                    
                    
                    z = re.findall("\_\_", line)
                    z = re.findall("\_\_", line)
          
                    if z:
                        ret = ''
                        time = ''
                        ch = line
                        st = ''
                        for i in range(len(ch)):
                            if ch[i] == '_' and ch[i + 1] == '_':
                                break
                            else:
                                st = st + ch[i]
                    x = re.findall("\-\-\>", line)
                    if x:
                        print("**************************")
                        m = line.split()
                        print(m)

                    matches1 = re.search(r'(\w+)\s+:\s+(-?\d+\.\d+)\s+(\w+)\s+\(,\s+(-?\d+)\)', line) # val1 = -999 ,
                    matches2 = re.search(r'(\w+)\s+:\s+(-?\d+\.\d+)\s+(\w+)\s+\(\s+(-?\d+),\)', line) # val2 = 999
                    pattern3 = r'(\w+)\s+:\s+(\s+(-?\w+).\s+(-?\w+))\s*,\s*(\s+(-?\w+).\s+(-?\w+))\)'
                    #r'(\w+)\s+:\s+(-?\d+\.\d+)\s+(\w+)\s+\(,\)'
                    matches3 = re.search(pattern3, line)
                    matches4 = re.search(r'(\w+)\s+:\s+(-?\d+\.\d+)\s+(\w+)\s+\(\s+(-?\w+),\s+(-?\w+)\)', line)
                    
                    # Call the extraction functions from within your main script
                    
                        
                        
                    
                  
                    per = extract_PER(line)
                    if per is not None:
                        print(line)
                        
                        spl = line.split()
                        #print(spl)
                        step = spl[0]
                        unite = spl[3]
                        min_= 0
                        max = 100
                        
                        nom = generate_nom(self.st)
                        
                        print(nom)
                        if len(spl) > 6 :
                            min_ = spl[5]
                            max_= spl[6][:-1]
                        else :
                            min_= 0
                            max = 100 
                        
                        
                        
                        print("PER:", per)
                        print(nom)
                        #'21.TEST_VERIFY', 'PER', '5500', 'MCS0', 'HE_SU', 'BW-20', 'ANT1
                        
                        try:
                            if max_ is not  None or max_ !=  ""   and   min_ is not  None or min_ !=  ""  :
                                
                                g.write(f"Nom  : {nom}  Measurement : {per} Unit : {unite} LowerLimit : {min_} HigherLimit : {max_} Description : {step} \n")
                            elif max_  is not  None or max_ !=  "" :
                                min_ = 0
                                g.write(f"Nom  : {nom}  Measurement : {per} Unit : {unite} LowerLimit : {min_} HigherLimit : {max_} Description : {step} \n")
                            elif  min_ is not  None or min_ !=  "":
                                min_ = 0 
                                g.write(f"Nom  : {nom}  Measurement : {per} Unit : {unite} LowerLimit : {min_} HigherLimit : {max_} Description : {step} \n")
                                 
                        except Exception as ex :
                            min_ = 0
                            max_ = 100
                            g.write(f"Nom  : {nom}  Measurement : {per} Unit : {unite} LowerLimit : {min_} HigherLimit : {max_} Description : {step} \n")
                            
                            
                    power = extract_POWER(line)
                    if power is not None:
                        print (line)
                        spl = line.split()
                        print(spl)
                        step = spl[0]
                        unite = spl[3]
                        min_= -999
                        max = 999
                        if len(spl) > 6 :
                            min_ = spl[5]
                            max_= spl[6][:-1]
                        else :
                            min_= -999
                            max = 999 
                        nom = generate_nom(self.st)
                        if unity_ == '%' :
                            max_ = 100 
                            min_  = 0
                        g.write(f"Nom  : {nom}  Measurement : {power_} Unit : {unity_} LowerLimit : {min_} HigherLimit : {max_} Description : {step} \n")
                        print("POWER:", power)
                        
                        #import time 
                        #time.sleep(4)

                    if matches1:
                        for groupNum in range(0, len(matches1.groups())):
                            
                            groupNum = groupNum + 1
                            #print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = matches1.start(groupNum), end = matches1.end(groupNum), group = matches1.group(groupNum)))
                            desc = matches1.group(1)
                            if groupNum == 1:
                                nom = generate_nom(self.st)
                                
                                nom = nom.replace(".", "_")
                                g.write(f"{dctnadra.get(groupNum)} : {nom} ")
                             
                                
                            
                            else:
                                
                                
                                
                                
                                g.write(f"{dctnadra.get(groupNum)} : {matches1.group(groupNum)} ")
                        g.write("val2 : -999 ") 
                        g.write(f"Description : {desc}")
                        g.write("\n")

                    if matches3:
                        for groupNum in range(0, len(matches3.groups())):
                            groupNum = groupNum + 1
                            desc = matches3.group(1)
                            if groupNum == 1:
                                nom = generate_nom(self.st)
                                nom = nom.replace(".", "_")
                                g.write(f"{dctnadra.get(groupNum)} : {nom} ")
                            else:
                                g.write(f"{dctnadra.get(groupNum)} : {matches3.group(groupNum)} ")
                        g.write(f"Description : {desc}")
                        g.write("\n")

                    if matches4:
                        desc = matches4.group()
                        for groupNum in range(0, len(matches4.groups())):
                            groupNum = groupNum + 1
                            desc = matches4.group(1)
                            if groupNum == 1:
                                nom = generate_nom(self.st)
                                nom = nom.replace(".", "_")
                                g.write(f"{dctnadra.get(groupNum)} : {nom} ")
                            else:
                                g.write(f"{dctnadra.get(groupNum)} : {matches4.group(groupNum)} ")
                        g.write(f"Description : {desc}")
                        g.write("\n")

                    if matches2:
                        desc = matches2.group()
                        for groupNum in range(0, len(matches2.groups())):
                            groupNum = groupNum + 1
                            desc = matches2.group(1)
                            if groupNum == 1:
                                nom = generate_nom(self.st)
                                nom = nom.replace(".", "_")
                                g.write(f"{dctnadra.get(groupNum)} : {nom} ")
                            
                            
                            
                            else:
                                
                                g.write(f"{dctnadra.get(groupNum)} : {matches2.group(groupNum)} ")
                        g.write("HigherLimit : 999 ")      
                        g.write(f"Description : {desc}")
                        g.write("\n")

                    line = f.readline()




 
def Check_failed(section_name, sections):
    error=''
    index = 0
    for section, name in zip(sections,section_name):
        lines = section.splitlines()
        index = index+1
        for line in lines:
            failed1 = line.find('--- [Failed]  :')
            failed2 = line.find(')  --- [Failed]')
            if failed1 >= 0:
                error = str(line.split(':')[1] + ' : ' + name)
                break
            if failed2 >= 0:
                error = str(line.split(':')[0].strip() + ' : ' + name)
                break
        if error != '':
             break
    return error

 
 
def Check_Passed(filename):
    with open(filename, 'r') as file:
        for line in file:
            if line.find('*  P A S S  *')!=-1:   
                return 1
        return -1
 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process log file and extract measurements.')
    parser.add_argument('--input', type=str, required=True, help='Input log file')
    parser.add_argument('--output', type=str, required=True, help='Output results file')
    args = parser.parse_args()
 
    filename = args.input
    output_filename = args.output
    
    
    version_file  = "version-app.txt"
    with open(version_file, "w+") as v :
        v.write(__version__)
 
    
        
        
        
    passed  = int(Check_Passed(filename=filename))

    if passed :
         os.system("echo extract mesure fini  ")
         os.system('color 0B')
        

    
    
        
       
   
    
    ex = Extractor(filename, "log")
    ex.extract(f"{output_filename}")
    
    
        
    
    
    os.system("color 0E")
    
    
    
    #import time 
    #time.sleep(4)
