#include "TLorentzVector.h"

double wBox[16]={0.0,0.0417451299727,0.0595348216593,0.0755387991667,0.14605987072,0.276238113642,0.406643003225,0.554394960403,0.820718944073,0.970041275024,1.69588017464,2.41057658195,3.97522950172,4.17105531693,8.84643268585,10.7170677185};
double wTri[16]={0.0,1.48873186111,1.51379203796,1.63247823715,1.95389711857,1.80282735825,2.51512789726,3.05885887146,3.89572691917,3.86426234245,5.1943025589,5.99451589584,9.92912960052,9.23208999634,16.1879787445,17.9208660126};
double wBinMin[16]={0.0,200.0,250.0,300.0,350.0,400.0,425.0,450.0,475.0,500.0,550.0,600.0,650.0,700.0,750.0,800.0};
double wBinMax[16]={200.0,250.0,300.0,350.0,400.0,425.0,450.0,475.0,500.0,550.0,600.0,650.0,700.0,750.0,800.0,9000000000.0};

double getBoxWeight(double Vpt,double Veta,double Vphi,double Vmass,double Hpt,double Heta,double Hphi,double Hmass){
  TLorentzVector V;
  TLorentzVector H;
  V.SetPtEtaPhiM(Vpt,Veta,Vphi,Vmass);
  H.SetPtEtaPhiM(Hpt,Heta,Hphi,Hmass);
  TLorentzVector Vstar=V+H;
  
  int l=sizeof(wBox)/sizeof(wBox[0]);

  int lp=0;
  while(wBinMax[lp]<Vstar.M() && lp<l-1)
    lp++;

  return wBox[lp];
}

double getTriangleWeight(double Vpt,double Veta,double Vphi,double Vmass,double Hpt,double Heta,double Hphi,double Hmass){
  TLorentzVector V;
  TLorentzVector H;
  V.SetPtEtaPhiM(Vpt,Veta,Vphi,Vmass);
  H.SetPtEtaPhiM(Hpt,Heta,Hphi,Hmass);
  TLorentzVector Vstar=V+H;

  int l=sizeof(wBox)/sizeof(wBox[0]);

  int lp=0;
  while(wBinMax[lp]<Vstar.M() && lp<l-1)
    lp++;

  return wTri[lp];
}
