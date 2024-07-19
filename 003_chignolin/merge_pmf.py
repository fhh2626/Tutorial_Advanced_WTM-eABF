#!/usr/bin/env python3
import os
import argparse
import numpy as np
from scipy.interpolate import interp1d
import copy

def readHeaderString(inputfile):
    headerLines = []
    with open(inputfile, 'r') as fp_in:
        for line in fp_in:
            if line.strip():
                fields = line.split()
                if fields[0][0] == '#':
                    headerLines.append(line)
    return headerLines

def mergepmf(pmf1, pmf2, outputname):
    cv_czar, pmf_czar = np.genfromtxt(pmf1, unpack = True)
    cv_amd, pmf_amd = np.genfromtxt(pmf2, unpack = True)
    f = interp1d(cv_amd, pmf_amd, fill_value = 'extrapolate', kind = 'quadratic')
    pmf_amd = f(cv_czar)
    pmf_total = pmf_amd + pmf_czar
    pmf_total_min = np.min(pmf_total)
    pmf_total = pmf_total - pmf_total_min
    headerLines = readHeaderString(pmf1)
    with open(outputname, 'w') as fp_out:
        for line in headerLines:
            fp_out.write(line)
        for cv, pmf in np.nditer([cv_czar, pmf_total]):
            fp_out.write(f'{cv:10.4f} {pmf:12.7f}\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('pmf1', help='PMF file from CZAR of Colvars')
    parser.add_argument('pmf2', help='PMF file from GaMD reweighting')
    parser.add_argument('-o', '--output', default='output.pmf', help = 'merged output')
    args = parser.parse_args()
    mergepmf(args.pmf1, args.pmf2, args.output)

if __name__ == "__main__":
    main()
