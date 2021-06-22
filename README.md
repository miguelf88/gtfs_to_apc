# gtfs_to_apc
Script that generates an APC reference file from a GTFS feed

The APC reference file that is generated works for a trip-based GTFS feed. </br>

I have a folder titled `GTFS Workspace` with a folder for each service change. Those folders use the naming convention `PART_YYYYMMDD`. </br>
To use, replace the `path_to_gtfs_workspace` variable to whatever workspace you use for your GTFS feed. </br>
You will also need to update the `path_to_folder` variable to reflect your naming covention. </br>
Finally, you will need to update the variable `prefix` that is used to name the final file. </br>

This script also assumes all feeds are a zipped file named `gtfs.zip`
