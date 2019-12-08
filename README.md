# Van Horn orientations

This repository contains a preliminary analysis of bedding orientation for
a small 3D model of outcrops of the Van Horn Formation, in its exposure
area north of Van Horn, Texas. The project is based on drone imagery and 3D models
collected during a field trip to the region in 2016.

## Installation

First, clone this repository and use `git submodule --init` to get submodules.

The code for this project is chiefly written in Python. Dependencies are managed
using `pipenv`; install Pipenv on your machine and run `pipenv install` in the
root directory of the repository.

## About

This project uses the [Attitude](https://github.com/davenquinn/Attitude)
Python module to extract geological orientations
from an Agisoft Metashape 3D model. Bedding traces are digitized directly on
the oblique imagery that forms the source data for the model, and projected
into model space. This allows extraction of 3D shapes from the model by digitizing
on arbitrarily-oriented 2D imagery.


