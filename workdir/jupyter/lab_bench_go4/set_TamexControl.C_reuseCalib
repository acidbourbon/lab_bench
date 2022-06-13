// written by macro saveparam.C at Mon Jun 13 11:24:24 2022
void set_TamexControl()
{
#ifndef __GO4ANAMACRO__
   std::cout << "Macro set_TamexControl can execute only in analysis" << std::endl;
   return;
#endif
   TTamex_FullParam* param0 = (TTamex_FullParam*) go4->GetParameter("TamexControl","TTamex_FullParam");

   if (param0==0) {
      TGo4Log::Error("Could not find parameter TamexControl of class TTamex_FullParam");
      return;
   }

   TGo4Log::Info("Set parameter TamexControl as saved at Mon Jun 13 11:24:24 2022");

   param0->useOldCalibration = kTRUE;
   param0->resetCalibration = kFALSE;

}
