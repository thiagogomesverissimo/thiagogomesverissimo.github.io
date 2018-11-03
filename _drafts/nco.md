#NetCDF operations:

#Converter arquivo em NetCDF4 para NetCDF3

 ncks -3 inputfile.nc4 outputfile.nc3 #Opção1
 nccopy -k classic foo4c.nc foo3.nc #opção2

#Converter NetCDF3 para netCDF4: 
 ncks -4 --deflate=5 infile.nc3 outfile.nc4
