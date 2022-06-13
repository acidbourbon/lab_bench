// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME G__Tamex_Full
#define R__NO_DEPRECATION

/*******************************************************************/
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#define G__DICTIONARY
#include "RConfig.h"
#include "TClass.h"
#include "TDictAttributeMap.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TBuffer.h"
#include "TMemberInspector.h"
#include "TInterpreter.h"
#include "TVirtualMutex.h"
#include "TError.h"

#ifndef G__ROOT
#define G__ROOT
#endif

#include "RtypesImp.h"
#include "TIsAProxy.h"
#include "TFileMergeInfo.h"
#include <algorithm>
#include "TCollectionProxyInfo.h"
/*******************************************************************/

#include "TDataMember.h"

// The generated code does not explicitly qualifies STL entities
namespace std {} using namespace std;

// Header files passed as explicit arguments
#include "./TTamex_FullParam.h"
#include "./TTamex_FullProc.h"
#include "./TTamex_FullEvent.h"

// Header files passed via #pragma extra_include

namespace ROOT {
   static void *new_TTamex_FullParam(void *p = 0);
   static void *newArray_TTamex_FullParam(Long_t size, void *p);
   static void delete_TTamex_FullParam(void *p);
   static void deleteArray_TTamex_FullParam(void *p);
   static void destruct_TTamex_FullParam(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TTamex_FullParam*)
   {
      ::TTamex_FullParam *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::TTamex_FullParam >(0);
      static ::ROOT::TGenericClassInfo 
         instance("TTamex_FullParam", ::TTamex_FullParam::Class_Version(), "TTamex_FullParam.h", 19,
                  typeid(::TTamex_FullParam), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::TTamex_FullParam::Dictionary, isa_proxy, 4,
                  sizeof(::TTamex_FullParam) );
      instance.SetNew(&new_TTamex_FullParam);
      instance.SetNewArray(&newArray_TTamex_FullParam);
      instance.SetDelete(&delete_TTamex_FullParam);
      instance.SetDeleteArray(&deleteArray_TTamex_FullParam);
      instance.SetDestructor(&destruct_TTamex_FullParam);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TTamex_FullParam*)
   {
      return GenerateInitInstanceLocal((::TTamex_FullParam*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::TTamex_FullParam*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_TTamex_FullProc(void *p = 0);
   static void *newArray_TTamex_FullProc(Long_t size, void *p);
   static void delete_TTamex_FullProc(void *p);
   static void deleteArray_TTamex_FullProc(void *p);
   static void destruct_TTamex_FullProc(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TTamex_FullProc*)
   {
      ::TTamex_FullProc *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::TTamex_FullProc >(0);
      static ::ROOT::TGenericClassInfo 
         instance("TTamex_FullProc", ::TTamex_FullProc::Class_Version(), "TTamex_FullProc.h", 134,
                  typeid(::TTamex_FullProc), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::TTamex_FullProc::Dictionary, isa_proxy, 4,
                  sizeof(::TTamex_FullProc) );
      instance.SetNew(&new_TTamex_FullProc);
      instance.SetNewArray(&newArray_TTamex_FullProc);
      instance.SetDelete(&delete_TTamex_FullProc);
      instance.SetDeleteArray(&deleteArray_TTamex_FullProc);
      instance.SetDestructor(&destruct_TTamex_FullProc);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TTamex_FullProc*)
   {
      return GenerateInitInstanceLocal((::TTamex_FullProc*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::TTamex_FullProc*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_TTamex_FullEvent(void *p = 0);
   static void *newArray_TTamex_FullEvent(Long_t size, void *p);
   static void delete_TTamex_FullEvent(void *p);
   static void deleteArray_TTamex_FullEvent(void *p);
   static void destruct_TTamex_FullEvent(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TTamex_FullEvent*)
   {
      ::TTamex_FullEvent *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::TTamex_FullEvent >(0);
      static ::ROOT::TGenericClassInfo 
         instance("TTamex_FullEvent", ::TTamex_FullEvent::Class_Version(), "TTamex_FullEvent.h", 29,
                  typeid(::TTamex_FullEvent), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::TTamex_FullEvent::Dictionary, isa_proxy, 4,
                  sizeof(::TTamex_FullEvent) );
      instance.SetNew(&new_TTamex_FullEvent);
      instance.SetNewArray(&newArray_TTamex_FullEvent);
      instance.SetDelete(&delete_TTamex_FullEvent);
      instance.SetDeleteArray(&deleteArray_TTamex_FullEvent);
      instance.SetDestructor(&destruct_TTamex_FullEvent);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TTamex_FullEvent*)
   {
      return GenerateInitInstanceLocal((::TTamex_FullEvent*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::TTamex_FullEvent*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

//______________________________________________________________________________
atomic_TClass_ptr TTamex_FullParam::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *TTamex_FullParam::Class_Name()
{
   return "TTamex_FullParam";
}

//______________________________________________________________________________
const char *TTamex_FullParam::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TTamex_FullParam*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int TTamex_FullParam::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TTamex_FullParam*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *TTamex_FullParam::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TTamex_FullParam*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *TTamex_FullParam::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TTamex_FullParam*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr TTamex_FullProc::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *TTamex_FullProc::Class_Name()
{
   return "TTamex_FullProc";
}

//______________________________________________________________________________
const char *TTamex_FullProc::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TTamex_FullProc*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int TTamex_FullProc::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TTamex_FullProc*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *TTamex_FullProc::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TTamex_FullProc*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *TTamex_FullProc::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TTamex_FullProc*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr TTamex_FullEvent::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *TTamex_FullEvent::Class_Name()
{
   return "TTamex_FullEvent";
}

//______________________________________________________________________________
const char *TTamex_FullEvent::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TTamex_FullEvent*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int TTamex_FullEvent::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TTamex_FullEvent*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *TTamex_FullEvent::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TTamex_FullEvent*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *TTamex_FullEvent::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TTamex_FullEvent*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
void TTamex_FullParam::Streamer(TBuffer &R__b)
{
   // Stream an object of class TTamex_FullParam.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(TTamex_FullParam::Class(),this);
   } else {
      R__b.WriteClassBuffer(TTamex_FullParam::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_TTamex_FullParam(void *p) {
      return  p ? new(p) ::TTamex_FullParam : new ::TTamex_FullParam;
   }
   static void *newArray_TTamex_FullParam(Long_t nElements, void *p) {
      return p ? new(p) ::TTamex_FullParam[nElements] : new ::TTamex_FullParam[nElements];
   }
   // Wrapper around operator delete
   static void delete_TTamex_FullParam(void *p) {
      delete ((::TTamex_FullParam*)p);
   }
   static void deleteArray_TTamex_FullParam(void *p) {
      delete [] ((::TTamex_FullParam*)p);
   }
   static void destruct_TTamex_FullParam(void *p) {
      typedef ::TTamex_FullParam current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::TTamex_FullParam

//______________________________________________________________________________
void TTamex_FullProc::Streamer(TBuffer &R__b)
{
   // Stream an object of class TTamex_FullProc.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(TTamex_FullProc::Class(),this);
   } else {
      R__b.WriteClassBuffer(TTamex_FullProc::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_TTamex_FullProc(void *p) {
      return  p ? new(p) ::TTamex_FullProc : new ::TTamex_FullProc;
   }
   static void *newArray_TTamex_FullProc(Long_t nElements, void *p) {
      return p ? new(p) ::TTamex_FullProc[nElements] : new ::TTamex_FullProc[nElements];
   }
   // Wrapper around operator delete
   static void delete_TTamex_FullProc(void *p) {
      delete ((::TTamex_FullProc*)p);
   }
   static void deleteArray_TTamex_FullProc(void *p) {
      delete [] ((::TTamex_FullProc*)p);
   }
   static void destruct_TTamex_FullProc(void *p) {
      typedef ::TTamex_FullProc current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::TTamex_FullProc

//______________________________________________________________________________
void TTamex_FullEvent::Streamer(TBuffer &R__b)
{
   // Stream an object of class TTamex_FullEvent.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(TTamex_FullEvent::Class(),this);
   } else {
      R__b.WriteClassBuffer(TTamex_FullEvent::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_TTamex_FullEvent(void *p) {
      return  p ? new(p) ::TTamex_FullEvent : new ::TTamex_FullEvent;
   }
   static void *newArray_TTamex_FullEvent(Long_t nElements, void *p) {
      return p ? new(p) ::TTamex_FullEvent[nElements] : new ::TTamex_FullEvent[nElements];
   }
   // Wrapper around operator delete
   static void delete_TTamex_FullEvent(void *p) {
      delete ((::TTamex_FullEvent*)p);
   }
   static void deleteArray_TTamex_FullEvent(void *p) {
      delete [] ((::TTamex_FullEvent*)p);
   }
   static void destruct_TTamex_FullEvent(void *p) {
      typedef ::TTamex_FullEvent current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::TTamex_FullEvent

namespace ROOT {
   static TClass *vectorlEdoublegR_Dictionary();
   static void vectorlEdoublegR_TClassManip(TClass*);
   static void *new_vectorlEdoublegR(void *p = 0);
   static void *newArray_vectorlEdoublegR(Long_t size, void *p);
   static void delete_vectorlEdoublegR(void *p);
   static void deleteArray_vectorlEdoublegR(void *p);
   static void destruct_vectorlEdoublegR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<double>*)
   {
      vector<double> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<double>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<double>", -2, "vector", 216,
                  typeid(vector<double>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlEdoublegR_Dictionary, isa_proxy, 4,
                  sizeof(vector<double>) );
      instance.SetNew(&new_vectorlEdoublegR);
      instance.SetNewArray(&newArray_vectorlEdoublegR);
      instance.SetDelete(&delete_vectorlEdoublegR);
      instance.SetDeleteArray(&deleteArray_vectorlEdoublegR);
      instance.SetDestructor(&destruct_vectorlEdoublegR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<double> >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const vector<double>*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEdoublegR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const vector<double>*)0x0)->GetClass();
      vectorlEdoublegR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEdoublegR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEdoublegR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<double> : new vector<double>;
   }
   static void *newArray_vectorlEdoublegR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<double>[nElements] : new vector<double>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEdoublegR(void *p) {
      delete ((vector<double>*)p);
   }
   static void deleteArray_vectorlEdoublegR(void *p) {
      delete [] ((vector<double>*)p);
   }
   static void destruct_vectorlEdoublegR(void *p) {
      typedef vector<double> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class vector<double>

namespace {
  void TriggerDictionaryInitialization_libGo4UserAnalysis_Impl() {
    static const char* headers[] = {
"./TTamex_FullParam.h",
"./TTamex_FullProc.h",
"./TTamex_FullEvent.h",
0
    };
    static const char* includePaths[] = {
"/installations/go4/602-00/include",
"/installations/go4/602-00",
"/root-build/include",
"/workdir/jupyter/lab_bench_go4/",
0
    };
    static const char* fwdDeclCode = R"DICTFWDDCLS(
#line 1 "libGo4UserAnalysis dictionary forward declarations' payload"
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_Autoloading_Map;
namespace std{template <typename _Tp> class __attribute__((annotate("$clingAutoload$bits/allocator.h")))  __attribute__((annotate("$clingAutoload$string")))  allocator;
}
class __attribute__((annotate("$clingAutoload$./TTamex_FullParam.h")))  TTamex_FullParam;
class __attribute__((annotate("$clingAutoload$./TTamex_FullProc.h")))  TTamex_FullProc;
class __attribute__((annotate("$clingAutoload$./TTamex_FullEvent.h")))  TTamex_FullEvent;
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(
#line 1 "libGo4UserAnalysis dictionary payload"

#ifndef Linux
  #define Linux 1
#endif

#define _BACKWARD_BACKWARD_WARNING_H
// Inline headers
#include "./TTamex_FullParam.h"
#include "./TTamex_FullProc.h"
#include "./TTamex_FullEvent.h"

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[]={
"TTamex_FullEvent", payloadCode, "@",
"TTamex_FullParam", payloadCode, "@",
"TTamex_FullProc", payloadCode, "@",
nullptr};

    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("libGo4UserAnalysis",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_libGo4UserAnalysis_Impl, {}, classesHeaders, /*has no C++ module*/false);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_libGo4UserAnalysis_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_libGo4UserAnalysis() {
  TriggerDictionaryInitialization_libGo4UserAnalysis_Impl();
}
