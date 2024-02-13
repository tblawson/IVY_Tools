# -*- coding: utf-8 -*-
"""
Gain_results_to_LaTeX.py

Created on Thu 23/02/2023

@author: t.lawson

Extract data from IVY_Results.json (or similar results file) and reformat the data to suit a LaTeX report table.

"""
import math
import os
import json


D_B_SLASH = r'\\'  # Double back-slash
CMC = {1e-3: 5e-9,  # DC-I CMC: keys = nominal I, vals = our best Exp. Uncert.
       1e-4: 5e-10,
       1e-5: 5e-11,
       1e-6: 1e-11,
       1e-7: 1e-12,
       1e-8: 2e-13,
       1e-9: 1.5e-13,
       1e-10: 5.4e-14,
       1e-11: 5.6e-15}

# Start with an IVY_Results.json file - can have any name.
results_path = input('Full path to results directory > ')
results_filename = input('Results file (press "d" to default to IVY_Results.json) > ')
if results_filename == 'd':
    results_filename = r'IVY_Results.json'

# Open file and print list of runs
with open(os.path.join(results_path, results_filename), 'r') as results_fp:
    results = json.load(results_fp)
    run_IDs = list(results.keys())
    print('Found the following runs:')
    for run in run_IDs:
        print(run)

# Infinite loop allows selection of multiple runs (gains)
while True:
    run = input('\nSelect a run from the above list (or "q" to quit)> ')
    if run == "q":
        break
    duc = results[run]["DUC name"]
    gain = results[run]["DUC gain"]
    nom_V_outs = results[run]["Nom_dV"].keys()

    # Print some vital stats for this run
    # (not really necessary, but helps with de-bugging)
    print(f'DUC = {duc}; gain = {gain}; V-out list: {nom_V_outs}\n')

    # Environmental conditions:
    Tduc_val = results[run]['Tduc_GMH']['value']
    Tduc_EU = results[run]['Tduc_GMH']['ExpU']
    Tduc_k = results[run]['Tduc_GMH']['k']

    Hum_val = results[run]['RH']['value']
    Hum_EU = results[run]['RH']['ExpU']
    Hum_k = results[run]['RH']['k']

    print(f'________\nTduc = {Tduc_val} +/- {Tduc_EU}, coverage factor = {Tduc_k}')
    print(f'RH = {Hum_val} +/- {Hum_EU}, coverage factor = {Hum_k}\n---------\n')

    for v in nom_V_outs:
        if v == '0.1':
            G = f'{gain:1.0e}\t'  # Only include gain field for 1st line...
        else:
            G = '\t\t'  # ... blank, otherwise.
        cmc_statement = ''
        val = results[run]["Nom_dV"][v]["Delta_Iin"]["value"]  # I value
        nom_I = 10**round(math.log10(abs(val)))
        cmc = CMC[nom_I]
        exp_u = results[run]["Nom_dV"][v]["Delta_Iin"]["EU"]  # I Exp U
        reported_exp_u = max(cmc, exp_u)  # I Exp U, constrained by CMC
        k = results[run]["Nom_dV"][v]["Delta_Iin"]["k"]  # coverage factor
        if reported_exp_u > exp_u:
            cmc_statement = f' - CMC-LIMITED ({exp_u:1.2e})'

        # Put it all together, line-by-line, with appropriate formatting:
        line = f'{G} & {v} & {val:1.6e} & {reported_exp_u:1.2e} & {k:1.1f} {D_B_SLASH} % {run}{cmc_statement}'
        print(line)
