#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Explorer Common Functions
### Author : Martin C Lim
### Date   : 2018.03.28
### Descrip: Add VSE functionality to FSW_Common base code
### Strctr : pyvisa-->yavisa-->FSW_Common-->VSE_Common.py
#####################################################################
import FSW_Common

class VSE(FSW_Common.VSA):
   def __init__(self):
      pass
      
   #####################################################################
   ### VSE Display
   #####################################################################
   def Set_Group(self,sGroup):
      GroupList = self.query('INST:BLOC:LIST?').split(',')
      print("Grup:%s"%GroupList)
      if ("'" + sGroup + "'") in GroupList:
         pass
      else:
         self.write(":INST:BLOC:CRE '%s'"%(sGroup))
      self.write("INST:BLOC:USE 1, '%s'"%sGroup)

   #####################################################################
   ### VSE Input
   #####################################################################
   def Set_Input(self,sType):
      self.write('INP:SEL %s'%sType);              #RF|FILE

   def Set_InputFile(self,sFilename):
      self.write("*IDN?");
   #####################################################################
   ### VSE Attenuation
   #####################################################################

   #####################################################################
   ### VSE Frequency
   #####################################################################

   #####################################################################
   ### VSE Time/Sweep
   #####################################################################
   def Set_SweepCont(self,iON):
      if iON > 0:
         self.write('INIT:SEQ:MODE CONT');            #Continuous Sweep
      else:
         self.write('INIT:SEQ:MODE SING');           #Single Sweep

   #####################################################################
   ### VSE IQ Analyzer
   #####################################################################

   #####################################################################
   ### VSE Common Query
   #####################################################################

   #####################################################################
   ### VSE marker
   #####################################################################

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   ### this won't be run when imported
   VSE = VSE()
   VSE.VISA_Open("127.0.0.1")       #Prints IDN String
   print(VSE.Get_Channels())
