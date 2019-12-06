all: output/orientations.pdf extractions build/DJI_0045.json build/DJI_0062.json

tilesets: build/DJI_0045.mbtiles build/DJI_0062.mbtiles
extractions: output/DJI_0045_extracted.png output/DJI_0062_extracted.png

install:
	pipenv install

build output:
	mkdir -p $@

build/DJI_%_proj.json: project-data.py build/DJI_%.json
	pipenv run python $^ $@

build/DJI_%.json: data/DJI_%.mapboard-project/project.db | build
	ogr2ogr -nln linework -of GeoJSON \
		-gcp 0 0 0 0 \
		-gcp 0 -3000000 0 -3000 \
		-gcp 4000000 0 4000 0 \
		$@ $^

# Create mbtiles
data/DJI_%.mbtiles: build/DJI_%.JPG | build
	gdal_translate -a_srs EPSG:3857 \
		-gcp 0 0 0 0 \
		-gcp 4000 3000 4000000 -3000000 \
		-gcp 4000 0 4000000 0 \
		-of mbtiles $^ $@
	gdaladdo $@ \
		2 4 8 16 32 64 128 256 512 1024 2048 \
		4096 8192 16384 32768

build/DJI_%_render.jpg: render-models.py data/DJI_%.JPG | build
		pipenv run python $^ build

output/DJI_%_extracted.png: export-renders.py build/DJI_%_render.jpg build/DJI_%.json | output
	pipenv run python $^ $@

output/orientations.pdf: compute-orientations.py build/DJI_0045_proj.json build/DJI_0062_proj.json | output
	pipenv run python $^ $@
