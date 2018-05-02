﻿#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Explorer K96 Functions
### Author : Martin C Lim
### Date   : 2018.04.27
import VSE_Common
import time         #EVM Wait

class VSE(VSE_Common.VSE):
   def __init__(self):
      pass
      
   #####################################################################
   ### VSE General Settings
   #####################################################################
   def Set_Init_K96(self):
      self.Set_Channel('OFDMVSA')
      
   def Set_Autolevel(self,sState):
      self.write('CONF:POW:AUTO %s;*WAI'%sState);  #ON|OFF|1|0

   def Set_BurstSearch(self,sState):
      self.write('DEM:FORM:BURS %s;*WAI'%sState);  #ON|OFF|1|0
      
   def Set_ConfigFile(self,sFile):
      self.write('MMEM:LOAD:CFGF "%s";*WAI'%sFile);
   
   def Set_FilterAdjustable(self,sState):
      self.write('INP:FILT:CHAN:STAT %s'%sState);  #ON|OFF|1|0

   def Set_FSWIPAdd(self,sIP):                     #For FS-K96
      self.write('CONF:ADDR "TCPIP::%s"'%sIP);     #FSW IP Address
 
   def Set_Input(self,sType):
      self.write('INP:SEL %s'%sType);              #RF|AIQ|DIQ|FILE

   def Get_EVM(self):
      EVM = self.query('FETC:SUMM:EVM?;*WAI',0)
      try:
         EVM = float(EVM.strip())
      except:
         EVM = -9999
      return EVM

   def Get_EVM_Params(self):
      MAttn   = self.Get_AttnMech()
      RefLvl  = self.Get_RefLevel()
      Power   = self.Get_ChPwr()
      EVM     = self.Get_EVM()
      return ("%.2f,%.2f,%6.2f,%.2f"%(MAttn,RefLvl,Power,EVM))
      
   #####################################################################
   ### Helper Functions
   #####################################################################
   def EVM_Wait(self):
      EVM = '';                           #init EVM read value
      t0 = time.time()
      self.write('INIT:IMM');             #Start Measurement
      while (EVM == ''):                  #Loop until EVM present
         delta = (time.time() - t0)
         try:
            EVM = self.Get_EVM()
         except:
            pass
         if delta > 10:                   #EVM_Wait Timeout
            break
      print("K96_EVM_Wait: %.3f sec"%(delta))
      asdf = self.Get_EVM()               #Flush buffer of NaN
     
   def EVM_AutoCal(self):
      #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      #%%%% Code Settings
      #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      debug=0;
      Backoff = 0;
      EVM_Wind = -0.1;                    #EVM can degrade by this amount.
                                          #EVM Repeatability indicator
      #autostart = tic;
      #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      #%%%% Code Start
      #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      if debug==1: print('   Autolvl EVM: ');
      self.Set_Autolevel("ON")
      EVM_Curr = self.Get_EVM();          #Set initial RefLvl & Attn
      RefLvl = self.Get_RefLevel()
      MAttn  = self.Get_AttnMech()
      if debug==1: print ("      Ref:%.2f MAttn:%.0f EVM:%.2f"%(RefLvl, MAttn, EVM_Curr))
      
      #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      #%%%% Attn Sweep
      #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      if debug==1: print('   Attenu Swp: ');
      EVM_Prev = 1.00; 
      i=0;
      self.Set_Autolevel("OFF")            #Manually Set RefLvl & Attn
      while (i <= MAttn) & (i < 30):
         MechAttn = MAttn - i;
         self.Set_AttnMech(MAttn - i)
         EVM_Curr = self.Get_EVM();
         if debug==1: print ("      Ref:%.2f MAttn:%.0f EVM:%.2f"%(RefLvl, MechAttn, EVM_Curr))
         if EVM_Curr =='NAN':
            print "EVM NAN"
            break

         Diff = EVM_Prev - EVM_Curr;      #Positive = improvedEVM
         if (Diff > EVM_Wind):
            EVM_Prev = EVM_Curr;
            i = i + 1;
         else:
            if debug==1: print("      Break")
            i = i - 1;                    #Previous value
            break
      MechAttn = MAttn - i + Backoff;     #MechAttn Used for next step
      if (MechAttn < 0):
         MechAttn= 0
      self.Set_AttnMech(MechAttn)
         
      #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      #%%%% Ref Sweep
      #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      #print('   RefLvl Swp: ');
      EVM_Prev = 1.00; 
      i=0;
      Set_Autolevel("OFF")                #Manually Set RefLvl & Attn
      for x in range(0):
         Set_RefLevel(RefLvl - i)
         EVM_Curr = self.Get_EVM();
         if debug==1: print ("      Ref:%.2f MAttn:%.0f EVM:%.2f"%(RefLvl-i, MechAttn, EVM_Curr))
         if EVM_Curr =='NAN':
            print "EVM NAN"
            break

         Diff = EVM_Prev - EVM_Curr;   #Positive = improvedEVM
         if (Diff > EVM_Wind):
            EVM_Prev = EVM_Curr;
            i = i + 1;
         else:
            i = i - 1;                 #Previous value
            self.Set_RefLevel(RefLvl - i)
            break
      self.EVM_Wait()

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   ### this won't be run when imported
   if 0:
      import sys
      print(sys.version)
   VSE = VSE()
   VSE.VISA_Open("127.0.0.1")
   VSE.Set_DisplayUpdate('ON')
   VSE.Get_EVM_Params()
   VSE.Set_InitImm()
 
