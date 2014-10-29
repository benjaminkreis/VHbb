double weightSignalNLO(double pt){
  double p0 = 0.9663;
  double p1 = 0.0007301;
  double p2 = -2.822E-6;
  double p3 = 2.191E-9;
  double p4 = -7.468E-13;

  if(pt>400) pt=400;
  return p0+p1*pt+p2*pow(pt,2)+p3*pow(pt,3)+p4*pow(pt,4);
}
