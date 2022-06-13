
//-------------------------------------------------------------
//        Go4 Release Package v3.03-05 (build 30305)
//                      05-June-2008
//---------------------------------------------------------------
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
#ifndef TUNPACKPROCESSOR_H
#define TUNPACKPROCESSOR_H

//#define WR_TIME_STAMP     1   // white rabbit time stamp is head of data

#define MAX_SPEZIAL 1000000000

#ifdef WR_TIME_STAMP
 #define SUB_SYSTEM_ID      0x400
 #define TS__ID_L16         0x3e1
 #define TS__ID_M16         0x4e1
 #define TS__ID_H16         0x5e1
 #define TS__ID_X16         0x6e1
#endif // WR_TIME_STAMP

#define STATISTIC 200000

#define DUMP_BAD_EVENT 1

#define COARSE_CT_RANGE  0x800  // 11 bits

#define MAX_SSY        1                // maximum number of sub-systems (readout pcs in nxm system)
#define MAX_SFP        4
#define MAX_TAM       10                // maximum febex/tamex per sfp
#define MAX_CHA_INPUT 33                // A) maximum physical input channels per module. must be modulo 4
#define MAX_CHA       MAX_CHA_INPUT * 2 // B) leading egdes + trailing edges + qtc trailing edges
//////////////
//#define MAX_CHA_INPUT  32                // A) maximum physical input channels per module. must be modulo 4
//#define MAX_CHA        MAX_CHA_INPUT * 2 // B) leading egdes + trailing edges + qtc trailing edges

                             // it seems that only "leading" edge bit is set for 0-47 channels
                             // therefore "MAX_CHA_INPUT 48" and only "MAX_CHA_INPUT * 1"   
                             // this has changed to previous version and comments A) and B) are wrong
                             // so called 17th channel should would appear according to chahit as
                             // channel nr 48, therefore 49 channels in total

//#define N_DEEP_AN      4                // deep analysis for first N_DEEP_AN channels specified below.
                                        // must be even nr.

#define N_DEEP_AN      0  // JAM 7-june-2022: no deep correlations when we use tree output

#define MAX_CHA_AN    64                // total nr. of channels analyzed. must be modulo 4
#define MAX_HITS       1                // max. number of hits per channel accepted
//#define MAX_HITS      10                // max. number of hits per channel accepted

// select 64 channels to be analyzed
// test index:   0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
//               |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
//#define SSY_ID { 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5 }
//JAM above original example

//#define SSY_ID { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 } 

#define SSY_ID { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }


#define SFP_ID { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 } 
//#define SFP_ID { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 }
//#define SFP_ID { 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2 } 
//#define SFP_ID { 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1 }

//#define TAM_ID { 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
// JAM above original setup

#define TAM_ID { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }



//#define TAM_ID { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 } 
//#define TAM_ID { 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2 } 
//#define TAM_ID { 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 } 
//#define TAM_ID { 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3 } 

// test index:   0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
//               |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
//#define CHA_ID { 1, 2, 5, 6,99,99, 1, 1, 1, 5, 1, 2, 5, 6, 1, 5, 9,42,10,43,11,44,12,45,13,46,14,47,15,48,16,49,17,50,18,51,19,52,20,53,21,54,22,55,23,56,24,57,25,58,26,59,27,60,28,61,29,62,30,63,31,64,32,65 } // time generator
// JAM above the original

//#define CHA_ID { 1, 3, 5, 7, 9,11,13,15,17,19,21,23,25,27,29,31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32 } // 16 ch input
//#define CHA_ID { 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 } // 32 ch input led
//#define CHA_ID { 1,34, 2,35, 3,36, 4,37, 5,38, 6,39, 7,40, 8,41, 9,42,10,43,11,44,12,45,13,46,14,47,15,48,16,49,17,50,18,51,19,52,20,53,21,54,22,55,23,56,24,57,25,58,26,59,27,60,28,61,29,62,30,63,31,64,32,65 } // 32 ch input tot
//#define CHA_ID { 5, 7, 9,11, 3,36, 4,37, 5,38, 6,39, 7,40, 8,41, 9,42,10,43,11,44,12,45,13,46,14,47,15,48,16,49,17,50,18,51,19,52,20,53,21,54,22,55,23,56,24,57,25,58,26,59,27,60,28,61,29,62,30,63,31,64,32,65 } // time generator

// JAM 7-june-22: try to setup most generic deltat: use channel 0 as reference for first 16 chans, then subsequent pairs for ToT
#define CHA_ID { 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 0, 7, 0, 8, 0, 9, 0, 10, 0 , 11, 0, 12, 0, 13, 0 , 14, 0, 15 , 0, 16, 1, 34, 2, 35, 3, 36, 4, 37, 5, 38, 6, 39, 7,40,8,41,9,42,10,43,11,44,12,45,13,46,14,47,15,48,16,49} // time generator



//#define N_CAL_EVT               (ULong64_t) 100000
#define N_CAL_EVT               (ULong64_t) 200000

#define N_PHY_TREND_PRINT       (ULong64_t) 1000000

//#define N_DELTA_T   400000
#define N_DELTA_T   100000
#define N_BIN       100000
#define N_TIM       10000

#define N_TR_BINS   100000  
#define N_COARSE    30

#define CYCLE_TIME    (Double_t) 5000

//#define TRIG_WIN_SIZE      200     // in clock cycles 
#define HITPAT_CT_RANGE    20

#define N_BIN_T    600
#define RESET_VAL -100000

#include "TGo4EventProcessor.h"

//#include "TTamex_FullEvent.h"

class TTamex_FullParam;
class TTamex_FullEvent;
class TGo4Fitter;

class TTamex_FullProc : public TGo4EventProcessor {
   public:
      TTamex_FullProc() ;
      TTamex_FullProc(const char* name);
      virtual ~TTamex_FullProc() ;

      Bool_t BuildEvent(TGo4EventElement* target); // event processing function

 private:
      TGo4MbsEvent  *fInput; //!
      TTamex_FullEvent* fOutput; //!

      TTamex_FullParam* fPar;

      Bool_t fCalibrationDone;// flag if calibration is ready

      TH1   *h_box[MAX_SSY][MAX_SFP][MAX_TAM][MAX_CHA];  // box histogram in SFP id / TAMEX id / CHANNEL nr coordinates

      TH1   *h_err_box[MAX_SSY][MAX_SFP][MAX_TAM][MAX_CHA];  // box histogram in SFP id / TAMEX id / CHANNEL nr coordinates
 
      TH1   *h_tim[MAX_CHA_AN];                          // box histogram in test channel coordinates

      TH1   *h_sum[MAX_CHA_AN];                          // sum histogram in test channel coordinates

      TH2   *h_raw_tim_corr[N_DEEP_AN>>1];               // raw time correlatian ch1-ch0, ch3-ch2, ...

      TH1   *h_cal_tim_diff[MAX_CHA_AN][MAX_CHA_AN];     // calibrated channel time differences

      TH1   *h_cal_tim_diff_wic[MAX_CHA_AN][MAX_CHA_AN]; // calibrated chan. time diff. 
      TH1   *h_cal_tim_diff_woc[MAX_CHA_AN][MAX_CHA_AN]; // with a (wic) and without (woc)
                                                         // clock 
      TH1   *h_coarse_diff[MAX_CHA_AN][MAX_CHA_AN];      // coarse ctr differences

      TH1   *h_hitpat[MAX_CHA_AN];                       // test channel hit pattern

      TH1   *h_coarse[MAX_CHA_AN];                       // coarse ctr distribution

      TH1   *h_cal_tim_diff_te[MAX_CHA_AN][MAX_CHA_AN]; // calibrated channel time differences

      TH1   *h_cal_tim_diff_tr_av[MAX_CHA_AN][MAX_CHA_AN]; //

      TH1   *h_cal_tim_diff_tr_av_bc[MAX_CHA_AN][MAX_CHA_AN]; // ... base line corrected      

      TH1   *h_cal_tim_diff_tr_rms[MAX_CHA_AN][MAX_CHA_AN]; //

      TH2   *h_7_5_vs_11_9; 

      TH1   *h_p_sum_ab;
      TH2   *h_p_tota_vs_a;
      TH2   *h_p_totb_vs_b;
      TH2   *h_p_diff_ba_sum_ab;                
      
      TGo4Picture      *fPicture;

   ClassDef(TTamex_FullProc,1)
};

static  UInt_t l_err_catch = 0;
static  UInt_t l_prev_err_catch = 0;
static  UInt_t l_err_ssy [MAX_CHA];
static  UInt_t l_err_sfp [MAX_CHA];
static  UInt_t l_err_tam [MAX_CHA];
static  UInt_t l_err_cha [MAX_CHA];
static  UInt_t l_prev_err_ssy [MAX_CHA];
static  UInt_t l_prev_err_sfp [MAX_CHA];
static  UInt_t l_prev_err_tam [MAX_CHA];
static  UInt_t l_prev_err_cha [MAX_CHA];
static  UInt_t l_num_err;
static  UInt_t l_prev_num_err;

#endif //TUNPACKPROCESSOR_H


//----------------------------END OF GO4 SOURCE FILE ---------------------
