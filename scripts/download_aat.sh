#!/bin/sh

# download only explicit statements
wget http://aatdownloads.getty.edu/VocabData/explicit.zip
mkdir aat/
unzip explicit.zip -d aat/ 
# for explicit+inferred terms use  http://aatdownloads.getty.edu/VocabData/full.zip