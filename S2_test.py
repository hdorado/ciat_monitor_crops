
from sentinel2_pre import *
from sentinel_dndl import *

if __name__ == '__main__':
    
    data_dir = '/home/azalazar/data/Huila/S2/'
    out_dir = '/home/azalazar/data/Huila/pre/'
    #area_of_int = '/home/azalazar/data/spatial_ref/ibagueextent.geojson'
    
    #download_sentinel('Sentinel-2', 'S2MSI1C', 'asalazarr', 'tila8sude', '20180101', '20180314', filename='*_T18NVJ_*', down_dir=data_dir)
    
    #print('Pre-processing Sentinel-2 L1C data...')
    # Check and unzip files if needed
    
    unzipfiles(data_dir)
    
    # Sen2Cor processing
    sen2cor_L2A_batch('all', data_dir)
    
    #
    #pre_process_s2(data_dir, out_dir, area_of_int)