# -*- coding: utf-8 -*-
"""
Gain_results_to_LaTeX.py

Created on Thu 23/02/2023

@author: t.lawson

Extract data from IVY_Results.json (or similar results file) and reformat the data to suit a LaTeX report table.

"""

import os
import json

D_B_SLASH = r'\\'


results_path = input('Full path to results directory > ')
results_filename = input('Results file (press "d" to default to IVY_Results.json) > ')
if results_filename == 'd':
    results_filename = r'IVY_Results.json'

with open(os.path.join(results_path, results_filename), 'r') as results_fp:
    results = json.load(results_fp)
    run_IDs = list(results.keys())
    print('Found the following runs:')
    for run in run_IDs:
        print(run)

while True:
    run = input('\nSelect a run from the above list (or "q" to quit)> ')
    if run == "q":
        break
    duc = results[run]["DUC name"]
    gain = results[run]["DUC gain"]
    nom_V_outs = results[run]["Nom_dV"].keys()
    print(f'DUC = {duc}; gain = {gain}; V-out list: {nom_V_outs}\n')

    for v in nom_V_outs:
        if v == '0.1':
            G = f'{gain:1.0e}\t'
        else:
            G = '\t\t'
        val = results[run]["Nom_dV"][v]["Delta_Iin"]["value"]
        exp_u = results[run]["Nom_dV"][v]["Delta_Iin"]["EU"]
        k = results[run]["Nom_dV"][v]["Delta_Iin"]["k"]
        line = f'{G} & {v} & {val:e} & {exp_u:1.2e} & {k:1.1f} {D_B_SLASH} % {run}'
        print(line)
