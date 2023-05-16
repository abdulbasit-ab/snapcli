import os

global baseSNAP
global procfiles_directory

""" MODULE: processSAR.py
-----------------
This module contains functions to process SAR data before peforming offset tracking.

List of functions:

* applyOrbitFile()
* applyCalibration() 
* applyCoregistration()
* applyTerrainCorrection()
* createSpatialSubset()

More functions will be added soon
"""
def applyOrbitFile(granule,baseGran):
    """
    This function applies precise orbit file.
    
    INPUTS:
    - granule (str): Path to SAR source file (.zip)
    - baseGran (str): SAR source file name without extension.
    RETURN:
    - filename (str): Name of the processed file to be used in next step of processing.
    """
    aoFlag = 'Apply-Orbit-File '
    oType =  '-PcontinueOnFail=\'true\' -PorbitType=\'Sentinel Precise (Auto Download)\' '
    out = '-t %s/%s ' % (procfiles_directory,baseGran+'_OB')
    
    cmd = baseSNAP + aoFlag + out + oType + granule
    print('Applying Precise Orbit file')
    print(cmd)
    os.system(cmd)
    
    return '%s' % baseGran+'_OB.dim'

def applyCalibration(granule):
    """
    This function performs radiometric calibration.
    
    INPUTS:
    - granule (str): Processed file name (returned by applyOrbitFile() function)
    RETURN:
    - filename (str): Name of the processed file to be used in next step of processing.
    """
    calFlag = 'Calibration -PoutputBetaBand=\'false\' -PoutputSigmaBand=\'false\' -PselectedPolarisations=\'VV\' '
    out = '-t %s/%s ' % (procfiles_directory,granule.replace('.dim','_CAL'))
    inD = '-Ssource=%s/%s' % (procfiles_directory,granule)
    
    cmd = baseSNAP + calFlag + out + inD
    print ('Applying Calibration')
    print(cmd)
    os.system(cmd)
    
    return '%s' % granule.replace('.dim','_CAL.dim')

def applyCoregistration(granule_mst,granule_slv):
    """
    This function performs DEM assisted coregistraion using SRTM 1sec HGT DEM.
    
    INPUTS:
    - granule_mst (str): Processed file name (returned by applyCalibration() function) to be used as master.
    - granule_slv (str): Processed file name (returned by applyCalibration() function) to be used as slave.
    RETURN:
    - filename (str): Name of the processed file to be used in next step of processing.
    """
    corFlag = 'DEM-Assisted-Coregistration -PdemName=\'SRTM 1Sec HGT\' -PmaskOutAreaWithoutElevation=\'false\' '
    out = '-t %s/%s ' % (procfiles_directory,granule_mst.replace('.dim','_COR'))
    inD = '-Ssource=%s %s' % (procfiles_directory+'/'+granule_mst,procfiles_directory+'/'+granule_slv)
    
    cmd = baseSNAP + corFlag + out + inD
    print ('Applying DEM-Assited-Coregistration')
    print(cmd)
    os.system(cmd)
    
    return '%s' % granule_mst.replace('.dim','_COR.dim')

def applyTerrainCorrection(granule_stack,projection='WGS84(DD)',pixsiz=10.0):
    """
    This function performs terrain correction using SRTM 1sec HGT DEM.
    
    INPUTS:
    - granule_stack (str): Processed file name (returned by applyCoregistration() function).
    - projection (str): Specify map projection i.e., EPSG:32632, default value is WGS84(DD).
    - pixsiz (float): Pixel spacing, default value is 10.0 
    RETURN:
    - filename (str): Name of the processed file to be used in next step of processing.
    """
    tcFlag = 'Terrain-Correction '
    out = '-t %s/%s ' % (procfiles_directory,granule_stack.replace('.dim','_TC'))
    inD = '-Ssource=%s/%s ' % (procfiles_directory,granule_stack)
    inD = inD + '-PpixelSpacingInMeter=%s ' % pixsiz
    inD = inD + ' -PdemName=\'SRTM 1Sec HGT\' '
    inD = inD + ' -PmapProjection=%s ' % projection
    
    cmd = baseSNAP + tcFlag + out + inD
    print ('Applying Terrain Correction')
    print (cmd)
    os.system(cmd)
    return '%s' % granule_stack.replace('.dim','_TC.dim')

def createSpatialSubset(granule_stack,bbox):
    """
    This function creates spatial subset around region of interest.
    
    INPUTS:
    - granule_stack (str): Processed file name (returned by applyTerrainCorrection() function).
    - bbox (str): Geometry WKT i.e., POLYGON((7.9175 46.3891,8.1454 46.3891,8.1454 46.5773,7.9175 46.5773,7.9175 46.3891))
    RETURN:
    - filename (str): Name of the processed file to be used in next step of processing.
    """
    ssFlag = 'Subset '
    out = '-t %s/%s ' % (procfiles_directory,granule_stack.replace('.dim','_Subset'))
    inD = '-Ssource=%s/%s ' % (procfiles_directory,granule_stack)
    inD = inD + ' -PgeoRegion=%s ' % bbox
    
    cmd = baseSNAP + ssFlag + out + inD
    print ('Creating Spatial Subset')
    print (cmd)
    os.system(cmd)
    
    return '%s' % granule_stack.replace('.dim','_Subset.dim')

def writeGeoTIFF(granule_stack):
    """
    This function saves spatial subset around region of interest as GeoTIFF.
    
    INPUTS:
    - granule_stack (str): Spatial subset name (returned by createSpatialSubset() function).
    RETURN:
    - 
    """
    tcFlag = 'Write '
    inD = '-Ssource=%s/%s ' % (procfiles_directory,granule_stack)
    inD = inD + '-Pfile=%s/%s ' % (procfiles_directory,granule_stack.replace('.dim','.tif'))
    inD = inD + '-PformatName=GeoTIFF-BigTIFF '
    
    cmd = baseSNAP + tcFlag + inD
    print ('Writing GeoTIFF')
    print (cmd)
    os.system(cmd)
    
    return
