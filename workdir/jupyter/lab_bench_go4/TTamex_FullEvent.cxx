// $Id: TTamex_FullEvent.cxx 2627 2019-10-01 08:02:45Z linev $
//-----------------------------------------------------------------------
//       The GSI Online Offline Object Oriented (Go4) Project
//         Experiment Data Processing at EE department, GSI
//-----------------------------------------------------------------------
// Copyright (C) 2000- GSI Helmholtzzentrum fuer Schwerionenforschung GmbH
//                     Planckstr. 1, 64291 Darmstadt, Germany
// Contact:            http://go4.gsi.de
//-----------------------------------------------------------------------
// This software can be used under the license agreements as stated
// in Go4License.txt file which is part of the distribution.
//-----------------------------------------------------------------------

#include "TTamex_FullEvent.h"

#include "TGo4Log.h"


//***********************************************************
TTamex_FullEvent::TTamex_FullEvent() :
   TGo4EventElement()
{
   TGo4Log::Info("TTamex_FullEvent: Create instance");
}
//***********************************************************
TTamex_FullEvent::TTamex_FullEvent(const char* name) :
   TGo4EventElement(name)
{
   TGo4Log::Info("TTamex_FullEvent: Create instance %s", name);
}
//***********************************************************
TTamex_FullEvent::~TTamex_FullEvent()
{
   TGo4Log::Info("TTamex_FullEvent: Delete instance");
}

//-----------------------------------------------------------

void TTamex_FullEvent::Clear(Option_t *t)
{
      for (Int_t l_k = 0; l_k < MAX_CHA_AN_DIFF; l_k++)
      {
        //fTimeStamp[l_k].clear();
        fTimeDiff[l_k]= 30 * (l_k+1) * RESET_VAL; // JAM should be out of bounce for regular data
      }

}
