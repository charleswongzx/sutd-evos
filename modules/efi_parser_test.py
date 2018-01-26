import serial
import time

serialport=serial.Serial(
    port="/dev/ttyS0",
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=read_freq
)

#Global Var
read_freq=0.1 #seconds
update_freq=0.1


efi_parser_dict = {'type': 'efi_parser',
                'rpm': '0',#engine rpm
                'maps': '0', #manifold intake pressure
                'tps': '0', #Throttle position sensor
                'ect': '0', #engine coolant temperature 
                'ias': '0', #intake air temperature
                'o2s': '0', #oxygen exhaust
                'spark': False, #spark ignition on or no
                'fuelpw1': False, #hell if i fucking know
                'fuelpw2': False, #hell if i fucking know
                'ubadc1': '0', #battery voltage from ADC
                'fuellvl': '0', #fuel level in %
                'baro': '0', #outside kpa
                'fuelconsum': '0',#fuel makan
                }
                
def readinfo():
    ls=""
    ls=serialport.read(31)
    if len(serialport.read(31))>1:
        for key,val in efi_parser_dict:
            if key in efi_parser_dict =='rpm':
                val=ls[6]+ls[7]
            elif key in efi_parser_dict=='maps':
                val=ls[8]+ls[9]
            elif key in efi_parser_dict=='tps':
                val=ls[10]+ls[11]                  
            elif key in efi_parser_dict=='ect':
                val=ls[12]+ls[13]                    
            elif key in efi_parser_dict=='iat':
                val=ls[14]+ls[15]                
            elif key in efi_parser_dict=='o2s':
                val=ls[16]+ls[17]
            elif key in efi_parser_dict=='spark':
                val=ls[18]+ls[19]
            elif key in efi_parser_dict=='fuelpw1':
                val=ls[20]+ls[21]
            elif key in efi_parser_dict=='fuelpw1':    
                val=ls[22]+ls[23]            
            elif key in efi_parser_dict=='ubadc':
                val=ls[24]+ls[25]
            elif key in efi_parser_dict=='fuellvl':
                val=ls[26]
            elif key in efi_parser_dict=='baro':
                val=ls[27]+ls[28]
            elif key in efi_parser_dict=='fuelconsum':
                val=ls[29]+ls[30]
        else:
            print "Error: Unrecognised parameter"
    else:
        print "Tears, no data from EFI"

def calc(raw):
    if len(raw)>=2:
        highbyte=thingy[0]
        lowbyte=thingy[1]
        pros=((highbyte*factor)+lowbyte)*factor+offset
    elif len(raw)==1:
        highbyte=thingy[0]
        lowbyte=0
        pros=((highbyte*factor)+lowbyte)*factor+offset
    else:
        print "Tears no value to calculate"
        pass
    return pros

def infoparse():
    for key,val in efi_parser_dict:
        if key in efi_parser_dict =='rpm':
            factor=0.25
            offset=0
            val=calc(val) 
        elif key in efi_parser_dict=='maps':
            factor=0.039
            offset=0
            val=calc(val) 
        elif key in efi_parser_dict=='tps':
            factor=0.0015
            offset=0
            val=calc(val) 
        elif key in efi_parser_dict=='ect':
            factor=1.25
            offset=-40
            val=calc(val) 
        elif key in efi_parser_dict=='iat':                
            factor=1.25
            offset=-40
            val=calc(val)            
        elif key in efi_parser_dict=='o2s':
            factor=0.0012
            offset=0
            val=calc(val) 
        elif key in efi_parser_dict=='spark':
            factor=0.75
            offset=0
            val=calc(val) 
        elif key in efi_parser_dict=='fuelpw1':
            factor=0.001
            offset=0
            val=calc(val) 
        elif key in efi_parser_dict=='fuelpw1':
            factor=0.001
            offset=0
            val=calc(val) 
        elif key in efi_parser_dict=='ubadc':
            factor=0.00625
            offset=0
            val=calc(val) 
        elif key in efi_parser_dict=='fuellvl':
            factor=0.4
            offset=0
            val=calc(val) 
        elif key in efi_parser_dict=='baro':
            factor=0.0039
            offset=0
            val=calc(val) 
        elif key in efi_parser_dict=='fuelconsum':
            factor=0.0116
            offset=0
            val=calc(val)
    else:
        pass

def run():
    efi_parser_dict = {'type': 'efi_parser',
                   'rpm': '0',#engine rpm
                   'maps': '0', #manifold intake pressure
                   'tps': '0', #Throttle position sensor
                   'ect': '0', #engine coolant temperature 
                   'ias': '0', #intake air temperature
                   'o2s': '0', #oxygen exhaust
                   'spark': '0', #spark voltage
                   'fuelpw1': False, #hell if i fucking know
                   'fuelpw2': False, #hell if i fucking know
                   'ubadc1': '0', #battery voltage from ADC
                   'fuellvl': '0', #fuel level in %
                   'baro': '0', #outside kpa
                   'fuelconsum': '0',#fuel makan
                   }
    while True:
        check=serialport.read(31)
        if len(check)>1:
            readinfo()
            infoparse()
        else:
            print "Tears, no data from EFI"
#####################TEST######################
        for key,val in efi_parser_dict:
            print (key,' ', val)
        time.sleep(update_freq)
    except KeyboardInterrupt:
        pass
        
run()