# -*- coding: utf-8 -*-
"""
Created on Wed Mar 07 14:56:16 2018

Functions with pre-processing workflow for Sentinel-1 data for CIAT
crop_monitoring_project using ESA SNAP api tools.

@author: ASALAZAR
"""

# Import packages
import os, shutil, re, sys, subprocess, json
from math import ceil

def pre_process_s1(data_dir, out_dir, orbit, area_of_int=None, ref_raster=None, polarizations=['VV','VH'], write_int=False):
    """
    Args:
        data_dir (str): The location of Sentinel-1 unzipped products (.SAFE dir)
        our_dir (str): Directory for saving the results
        area_of_int (geojson):  A geoJSON file specifying coordinates of a
                                regions within the Sentinel-1 images (WGS84)
        ref_raster (str): location of a raster product with same extent and target resolution
        polarizations ([str]): strings of polarizations to consider in processing chain
    """
    print('Pre-processing Sentinel-1 images...')
    #batches = make_batches(sorted(filter(re.compile(r'^S1.....GRD.*SAFE$').search, os.listdir(data_dir))))
    batches = make_batches(sorted(filter(re.compile(r'^S1.....GRD.*SAFE$').search, os.listdir(data_dir))), 8)
    
    print('Processing {} batches from {}. Results will be saved in {}'.format(str(len(batches)), data_dir, out_dir))
    
    for bkey, batch in batches.iteritems():
        params_dict = dict(data_dir = data_dir, out_dir=out_dir, orbit=orbit, area_of_int=area_of_int, ref_raster = ref_raster, polarizations = polarizations, write_int = write_int, bkey = bkey, batch = batch)
        batch_json = json.dumps(params_dict)
        
        subprocess.call(['python', 'sentinel1_pre_sub.py', batch_json])

def make_batches_gen(l, n):
    """Generator approach / TODO test"""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def make_batches(prdlist, maxprods):
     """"""
     # 
     max_prods = maxprods
     # Calculate number of batches to allow no more than max_prods
     nbatch = ceil(len(prdlist)/float(max_prods))
     
     # Get the indices of products to save
     batchindex = {}
     
     # Create a dictionary to read Sentinel-1 L1 GRD products
     batches = {}
     
     # Assign the indices of the products to save to each batch
     counter = len(prdlist)
     for batch in range(int(nbatch)):
         if counter >max_prods:
             batchindex[batch] = range(int(batch*max_prods), max_prods+max_prods*batch)
         else:
             batchindex[batch] = range(int(batch*max_prods), counter+max_prods*batch)
         counter = counter - max_prods
     
     # Make the batches based on index order
     for key, value in batchindex.iteritems():
         batches[key] = {}
         for index in value:
             batches[key][prdlist[index][:-5]] = {}
     
     return batches

#def createProgressMonitor():
#    PWPM = jpy.get_type('com.bc.ceres.core.PrintWriterProgressMonitor')
#    JavaSystem = jpy.get_type('java.lang.System')
#    monitor = PWPM(JavaSystem.out)
#    return monitor