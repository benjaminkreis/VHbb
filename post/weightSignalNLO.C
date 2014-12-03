double weightSignalNLO(double pt){
  double p0 = 0.9683;
  double p1 = 6.61E-4;
  double p2 = -2.28E-6;
  double p3 = 9.923E-10;

  if(pt>400) pt=400;
  return p0+p1*pt+p2*pow(pt,2)+p3*pow(pt,3);
}
