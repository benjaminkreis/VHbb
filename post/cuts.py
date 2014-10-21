cuts=[{} for i in range(10)]

jetPt_cut   = 'hJet_ptCorr[0]>20 && hJet_ptCorr[1]>20'
jetEta_cut  = 'abs(hJet_eta[0]) < 2.4 && abs(hJet_eta[1])<2.4'
jetpuID_cut = 'hJet_puJetIdL[0]>0 && hJet_puJetIdL[1]>0'
hbhe_cut    = 'hbhe'
bad_pixels = '(!(207883<=EVENT.run && EVENT.run<=208307))'

preselection = jetPt_cut + ' && ' + jetEta_cut + ' && ' + hbhe_cut + ' && ' + jetpuID_cut + ' && ' + bad_pixels

CSVT = 0.898
CSVL = 0.244
CSVC = 0.5

noAddJet = 'Sum$(aJet_pt > 20 && abs(aJet_eta) < 2.4) == 0'
max1AddJet = 'Sum$(aJet_pt > 20 & abs(aJet_eta) < 2.4) < 2.'

zWindow = 'V.mass > 75. && V.mass < 105'
zVeto =  '(V.mass > 105 || V.mass < 75.)'
looseHMass = 'H.mass > 40. && H.mass < 250.'
upperHMass = 'H.mass < 250.'
vetoHMass = '(H.mass < 90. || H.mass > 145.)'
dPhiVH = 'abs( HVdPhi ) > 2.9'
twoCSV0 = 'hJet_csv[0] > 0. && hJet_csv[1] > 0.'
pullAngle = 'deltaPullAngle < 10. && deltaPullAngle2 < 10.'

rMed = 'V.pt > 50. && V.pt < 100.'
rTight = 'V.pt > 100.' 

minBtag = 'min(hJet_csv[0],hJet_csv[1])'
maxBtag = 'max(hJet_csv[0],hJet_csv[1])'

tcBtag = maxBtag + ' > ' + CSVT + ' && ' + minBtag + ' > ' + CSVC
ntBtag = '(hJet_csv[0] > ' + CSVT + ' || hJet_csv[1] > ' + CSVT + ')'

cuts[2]['ZLight']= preselection + ' && ' + noAddJet + ' && ' + zWindow + ' && ' + ntBtag + ' && ' + upperHMass + ' && ' + twoCSV0 + ' && ' + dPhiVH + ' && ' + maxBtag + ' > ' + CSVL + ' && V.pt > 50.' + ' && Vtype == 1' # ee
cuts[3]['ZLight']= preselection + ' && ' + noAddJet + ' && ' + zWindow + ' && ' + ntBtag + ' && ' + upperHMass + ' && ' + twoCSV0 + ' && ' + dPhiVH + ' && ' + maxBtag + ' > ' + CSVL + ' && V.pt > 50.' + ' && Vtype == 0' # mumu
cuts[2]['TTbar'] = preselection + ' && ' + upperHMass + ' && ' + tcBtag + ' && ' + zVeto + ' && H.pt > 100.' + ' && Vtype == 1'
cuts[3]['TTbar'] = preselection + ' && ' + upperHMass + ' && ' + tcBtag + ' && ' + zVeto + ' && H.pt > 100.' + ' && Vtype == 0'
cuts[2]['Zbb']   = preselection + ' && ' + vetoHMass + ' && ' + upperHMass + ' && ' + zWindow + ' && ' + tcBtag + ' && ' + max1AddJet + ' && ' + dPhiVH + ' && Vtype == 1'
cuts[3]['Zbb']   = preselection + ' && ' + vetoHMass + ' && ' + upperHMass + ' && ' + zWindow + ' && ' + tcBtag + ' && ' + max1AddJet + ' && ' + dPhiVH + ' && Vtype == 0'
cuts[2]['bdt']   = preselection + ' && ' + maxBtag + ' > ' + CSVC + ' && ' + minBtag + ' > ' + CSVL + ' && ' + zWindow + ' && ' + pullAngle + ' && Vtype == 1'
cuts[3]['bdt']   = preselection + ' && ' + maxBtag + ' > ' + CSVC + ' && ' + minBtag + ' > ' + CSVL + ' && ' + zWindow + ' && ' + pullAngle + ' && Vtype == 0'

