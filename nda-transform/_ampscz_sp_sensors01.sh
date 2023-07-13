#!/bin/bash

root=${1//.csv}

file=${root}_4366.csv
head -n 2 $1 > $file
grep geolocation $1 >> $file


file=${root}_3705.csv
head -n 2 $1 > $file
grep screen $1 >> $file
grep accelerometer $1 >> $file

