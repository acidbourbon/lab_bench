//   The GSI Online Offline Object Oriented (Go4) Project
//   Experiment Data Processing at EE department, GSI
//---------------------------------------------------------------
//
//Copyright (C) 2000- Gesellschaft f. Schwerionenforschung, GSI
//                    Planckstr. 1, 64291 Darmstadt, Germany
//Contact:            http://go4.gsi.de
//----------------------------------------------------------------
//This software can be used under the license agreements as stated
//in Go4License.txt file which is part of the distribution.
//----------------------------------------------------------------

--------------------------------------------
TTamex_Full Go4 analysis for Tamex lab setup
--------------------------------------------
original version by N.Kurz (n.kurz@gsi.de)

Changes:
08-July-2020: Added output event class JAM(j.adamczewski@gsi.de)
08-July-2020: Add switch to use old calibration from autosave file JAM(j.adamczewski@gsi.de)
19-Aug-2020: Bugfix for old calibration from file JAM
...

Classes:

** TTamex_FullProc: ****************************
contains unpacker and actual histograming/analysis code.


** TTamex_FullParam: ***************************
Go4 Parameter container with following members:
 
 Bool_t   useOldCalibration; 
 	if true, use fine time calibration histograms from autosave file. 
 	Otherwise, at least 100000 Events need to be processed until calibration starts
 
 Bool_t   resetCalibration;  
 	if true, discard existing fine time calibration and accumulate new histograms.
 	note: this flag is automatically reset after it invokes the calibration action

** TTamex_FullEvent: ****************************
Output event class to use for tree storage in Go4
NOTE: to use this class in the go4analysis runtime environment, 
it is necessary to pass the -class name by option "-outevt-class" explicitely on startup:

A) batch mode example:
go4analysis -stream x86l-126 -outevt-class TTamex_FullEvent -enable-store -store test.root -rate

B) go4 gui mode: the parameter "-outevt-class TTamex_FullEvent" must be put into the Args field 
of the "Launch Analysis" window. This argument is also kept when generating a go4 hotstart file!

The event structue of TTamex_FullEvent can be written to a root tree by command line option (batchmode), or
by turning on the EventStore in the go4 gui configuration.



_________________________________________________
                                   08-07-2020 JAM



