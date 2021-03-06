#include "TLorentzVector.h"
double weightSignalFormFactor(double Vpt,double Veta,double Vphi,double Vmass,double Hpt,double Heta,double Hphi,double Hmass,double Lambda){
   TLorentzVector V;
   TLorentzVector H;
   V.SetPtEtaPhiM(Vpt,Veta,Vphi,Vmass);
   H.SetPtEtaPhiM(Hpt,Heta,Hphi,Hmass);
   return 1.0/(pow(1.0+pow(V.M()/Lambda,2),2)*pow(1.0+pow((V+H).M()/Lambda,2),2));
}

double weightSignalNLO(double pt){
  double p0 = 0.9683;
  double p1 = 6.61E-4;
  double p2 = -2.28E-6;
  double p3 = 9.923E-10;

  if(pt>400) pt=400;
  return p0+p1*pt+p2*pow(pt,2)+p3*pow(pt,3);
}

double weightZHSignalNLO(double pt){
  double p0 = 0.9669;
  double p1 = 0.0005825;
  double p2 = -1.504E-6;
  double p3 = 4.531E-10;

  if(pt>400) pt=400;
  return p0+p1*pt+p2*pow(pt,2)+p3*pow(pt,3);
}

double weightWpt_for_WJets(double pt){
  double wptslope = -1.057e-03;

  return 1.0+wptslope*(pt-170.0);
}

double weightWpt_for_TTbar(double pt){
  double ttwptslope = -1.087e-03;

  return 1.0+ttwptslope*(pt-170.0);
}
