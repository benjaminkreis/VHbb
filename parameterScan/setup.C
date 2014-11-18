{
  gSystem->AddIncludePath("-I$ROOFITSYS/include");
  gSystem->AddIncludePath("-I$CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/interface/");
  gSystem->Load("$CMSSW_BASE/lib/slc5_amd64_gcc472/libHiggsAnalysisCombinedLimit.so");
}
