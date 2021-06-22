# gtfs_to_apc
Script that generates an APC reference file from a GTFS feed

The APC reference file that is generated works for a trip-based GTFS feed. 

I have a folder titled `GTFS Workspace` with a folder for each service change. Those folders use the naming convention `PART_YYYYMMDD`. 
To use, replace the `path_to_gtfs_workspace` variable to whatever workspace you use for your GTFS feed.
You will also need to update the `path_to_folder` variable to reflect your naming covention.
Finally, you will need to update the variable `prefix` that is used to name the final file.

This script also assumes all feeds are a zipped file named `gtfs.zip`
