// $Id: TTamex_FullParam.h 557 2010-01-27 15:11:43Z linev $
//-----------------------------------------------------------------------
//       The GSI Online Offline Object Oriented (Go4) Project
//         Experiment Data Processing at EE department, GSI
//-----------------------------------------------------------------------
// Copyright (C) 2000- GSI Helmholtzzentrum f�r Schwerionenforschung GmbH
//                     Planckstr. 1, 64291 Darmstadt, Germany
// Contact:            http://go4.gsi.de
//-----------------------------------------------------------------------
// This software can be used under the license agreements as stated
// in Go4License.txt file which is part of the distribution.
//-----------------------------------------------------------------------

#ifndef TTamex_FullParam_H
#define TTamex_FullParam_H

#include "TGo4Parameter.h"

class TTamex_FullParam : public TGo4Parameter {
   public:
      TTamex_FullParam(const char* name = 0);
      Bool_t   useOldCalibration; // if true, use calibration from autosave file, do not wait until N_CAL_EVT
      Bool_t   resetCalibration;  // control starting new calibration

   ClassDef(TTamex_FullParam,1)
};

#endif // TTamex_FullParam_H
