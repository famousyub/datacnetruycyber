

import  os 

from subprocess import check_output
import subprocess
# linux
#out = check_output(['ping', '-c', '4', 'google.com'])

 

class RunBat :
    
    def __init__(self,path , cmd) :
        # Windows
        self.path =path 
        self.cmd =cmd 
    
    
    def excute(self) :
        #out = check_output(['ping', '8.8.8.8'])
        out = check_output(['Extractor.exe', '--input' , 'input.log' ,'--output' ,'testproces.txt'])
        
        #print(out.decode('utf-8').strip())
        data  = out.decode('utf-8').strip()
        return data
    def excutecmd (self,cmd):
        try :
            out  = check_output (['echo'  , f'{cmd}',' >> ' ,'testproces.txt'])
            data  = out.decode('utl-8').strip()
            return data
        except :
            process = subprocess.Popen(f"echo {cmd} > result.txt", stdout=subprocess.PIPE, shell=True)
            output = process.stdout.read()
            output_lines = output.split(b'\n')
            lines = [] 
            return output_lines[0].decode('utf-8')
    
        
    



class Bav :
    def __init__(self,filename ='bn.txt') :
        
        self.filename =filename 
        
    def readfile(self):
        
        with open( self.filename, 'r') as f: 
            line = f.readline()
            
            while line :
                #print(line)
                
                
                if line.strip() == 'PASSED' :
                    return "PASSED" 
                elif line.strip() =='FAILED'.strip() :
                    return 'FAILED'
                else :
                    line =f.readline()
        return ""
        
            
if __name__ =='__main__' :
    cur  =os.getcwd()    
    lst = os.listdir(cur)
    #print(lst)
    #print(cur)
    runbat_conf = 1
    
    for l in lst :
        if l.endswith('.txt')  and   l.startswith('bn') :
            #print(l)
            _tx = l    
            bav =Bav (_tx)
            print(f"data is {bav.readfile()} \n")
            if runbat_conf != 0:
                runbat =RunBat(".","ls")
                m =runbat.excutecmd(f"data is {bav.readfile()} \n")
                #runbat.excute()
                print(m)
            
        