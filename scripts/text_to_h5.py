#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
* Author: KANG, Jin-Wen
* E-Mail: kangjinwen@vip.qq.com
* Desc: Use for transform TRENTo ascii dat to hdf5 file (only for 2D data)
* Date: 2019-12-29 15:26:34 +0800
"""

import numpy as np 
import h5py as h5
import sys
import re
from os.path import splitext

def regularize(comment):
    res = comment.replace('#', '').replace('\n','').strip()
    # remove spaces around '='
    res = re.sub(r'\s+=\s+', r'=', res)
    return res.split()

def get_comments(fname):
    '''get comment lines in file=fname,
    return a dictionary of options'''
    options = dict()
    with open(fname, 'r') as fin:
        for line in fin.readlines():
            if '#' in line and '=' in line:
                for opt in regularize(line):
                    opt_name, opt_value = opt.split('=')
                    options[opt_name] = float(opt_value)
    return options

def read_entropy_ascii_dat(fname):
    entropy_density_dat = np.loadtxt(fname)
    comment = get_comments(fname)
    ncoll_fname = splitext(fname)[0] + ".ncoll"
    ncoll_density_dat = np.loadtxt(ncoll_fname)
    comment.update(get_comments(ncoll_fname))
    return entropy_density_dat, ncoll_density_dat, comment

def write_to_hdf5(fname, entropy, ncoll, comment):
    h5file = h5.File(fname, 'w')
    group = h5file.create_group('event_0')
    group.attrs['b'] = comment['b']
    group.attrs['npart'] = int(comment['npart'])
    group.attrs['ncoll'] = int(comment['ncoll'])
    group.attrs['mult'] = comment['mult']
    group.attrs['dxy'] = comment['xy_step']
    group.attrs['deta'] = comment['eta_step']
    group.attrs['Ny'] = int(comment['n_xy_step'])
    group.attrs['Nx'] = int(comment['n_xy_step'])
    group.attrs['Nz'] = int(comment['n_eta_step'])
    group.attrs['xyMax'] = comment['xy_max']
    group.attrs['etaMax'] = comment['n_eta_step']
    group.attrs['e2'] = comment['e2']
    group.attrs['e3'] = comment['e3']
    group.attrs['e4'] = comment['e4']
    group.attrs['e5'] = comment['e5']
    group.attrs['psi2'] = comment['psi2']
    group.attrs['psi3'] = comment['psi3']
    group.attrs['psi4'] = comment['psi4']
    group.attrs['psi5'] = comment['psi5']
    group.create_dataset('matter_density', data=entropy)
    group.create_dataset('Ncoll_density', data=ncoll)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        fname = sys.argv[1]
        outname = sys.argv[2]
        entropy_density_dat, ncoll_density_dat, comment = read_entropy_ascii_dat(fname)
        try:
            write_to_hdf5(outname, entropy_density_dat, ncoll_density_dat, comment)
            print(  "\033[1;32mInfo\033[0m: Transformation succeeded!")
        except Exception as err:
            print("  \033[1;31mERROR\033[0m: ", err)
    else:
        print("  --\033[1;32mUsage\033[0m: ./text_to_h5.py intput_dat_file output_hdf5_file")