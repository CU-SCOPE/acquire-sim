acquire-sim
===========================

This repository contains two folders that contain both the Blender files necessary for 3D simulation footage and data along with the Python script necessary to find approximate centroid locations.

Usage
-----
Setup a simulation in Blender and output a video for use with the Python script. A script to obtain the centroid locations is also included. It is important to note that if running the Python script for Blender it must be through the Python console in Blender and must have the Camera object selected or else it will throw an error.

Run the Python script with the generated video and a csv file with approximate centroid locations along with an output video of the centroid detection will be created. 

Todo
-----
Improve the algorithms for centroid detection and the Blender script for centroid detection. Moreover, more automation and dynamic pixel detection.
