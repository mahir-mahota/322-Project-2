import pandas as pd
from math import sqrt

df = pd.read_csv('nsk.csv')
left_diameter = 66
right_diameter = 86
WxP1 = 2282
WrP1 = 3651
WtP1 = 11829
dI = 270
dII = 78
rP1 = 70
L10 = 50000
fs = 20
f2f = True

# List to store results
results = []
count = 0

for index_C, bC in df.iterrows():
    for index_D, bD in df.iterrows():
        if bC['d'] < left_diameter and bD['d'] < right_diameter and bC['damin'] <= left_diameter and bD['damin'] <= right_diameter:
            CIr = bC['Cr']
            CI0r = bC['C0r']
            CIIr = bD['Cr']
            CII0r = bD['C0r']

            if f2f == True:
                lC = dI - bC['a'] + bC['C']
                lD = dII - bD['a'] + bD['C']
            else:
                lC = dI + bC['a']
                lD = dII + bD['a']

            Cx = ((WrP1*lD)-(WxP1*rP1)) / (lC+lD)
            Cy = (WtP1*lD) / (lC+lD)
            Dx = ((WrP1*lC)+(WxP1*rP1)) / (lC+lD)
            Dy = (WtP1*(lC)) / (lC+lD)

            FrI = sqrt(Cx*Cx + Cy*Cy)
            FrII = sqrt(Dx*Dx + Dy*Dy)

            FaI = 0
            FaII = 0
            if f2f == True:
                if ((WxP1 + (0.6 * FrI / bC['Y1'])) >= (0.6 * FrII / bD['Y1'])):
                    FaII = WxP1 + (0.6 * FrI / bC['Y1'])
                else:
                    FaI = (0.6 * FrII / bD['Y1']) - WxP1
            else:
                if ((WxP1 + (0.6 * FrII / bD['Y1'])) >= (0.6 * FrI / bC['Y1'])):
                    FaI = WxP1 + (0.6 * FrII / bD['Y1'])
                else:
                    FaII = (0.6 * FrI / bC['Y1']) - WxP1
            
            PI = (0.4*FrI + bC['Y1']*FaI) if FaI > 0 else FrI 
            PII = (0.4*FrII + bD['Y1']*FaII) if FaII > 0 else FrII
            
            P0I = 0.5*FrI + bC['Y0']*FaI
            P0II = 0.5*FrII + bD['Y0']*FaII
            if FrI > P0I:
                P0I = FrI
            if FrII > P0II:
                P0II = FrII

            CIreq = PI * (L10 ** (3/10))
            CI0req = fs * P0I
            CIIreq = PII * (L10 ** (3/10))
            CII0req = fs * P0II

            if CIreq < CIr and CI0req < CI0r and CIIreq < CIIr and CII0req < CII0r:
                print(bC['Bearing'], bD['Bearing'])
                # Store all data in a dictionary
                result_row = {
                    'Bearing_I': bC['Bearing'],
                    'ID_I' : bC['d'],
                    'OD_I' : bC['D'],
                    'T_I' : bC['T'],
                    'C_I' : bC['C'],
                    'da_min_I' : bC['damin'],
                    'Bearing_II': bD['Bearing'],
                    'ID_II' : bD['d'],
                    'OD_II' : bD['D'],
                    'T_II' : bD['T'],
                    'C_II' : bD['C'],
                    'da_min_II' : bD['damin'],
                    'Fr_I' : FrI,
                    'Fr_II' : FrII,
                    'Fa_I' : FaI,
                    'Fa_II' : FaII,
                    'P_I' : PI,
                    'P_II' : PII,
                    'P0_I' : P0I,
                    'P0_II' : P0II,
                }
                results.append(result_row)
        count += 1

print(f"\n{count} combinations checked")
if results:
    results_df = pd.DataFrame(results)
    results_df.to_csv('bearing_results.csv', index=False)
    print(f"Saved {len(results)} results to bearing_results.csv")
else:
    print("No results found matching the criteria.")
            