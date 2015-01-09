#include "TLorentzVector.h"
double weightSignalFormFactor(double Vpt,double Veta,double Vphi,double Vmass,double Hpt,double Heta,double Hphi,double Hmass,double Lambda){
   TLorentzVector V;
   TLorentzVector H;
   V.SetPtEtaPhiM(Vpt,Veta,Vphi,Vmass);
   H.SetPtEtaPhiM(Hpt,Heta,Hphi,Hmass);
   return 1.0/pow(1.0+pow((V+H).M()/Lambda,2),2);
}

double weightSignalNLO(double pt){
  double p0 = 0.9669;
  double p1 = 0.0005825;
  double p2 = -1.504E-6;
  double p3 = 4.531E-10;

  if(pt>400) pt=400;
  return p0+p1*pt+p2*pow(pt,2)+p3*pow(pt,3);
}
