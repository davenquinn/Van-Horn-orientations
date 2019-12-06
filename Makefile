all: data/orientations.pdf data/DJI_0045_extracted.png data/DJI_0062_extracted.png

install:
	pipenv install

data/DJI_%.json: data/DJI_%.mapboard-project/project.db
	ogr2ogr -nln linework -of GeoJSON \
		-gcp 0 0 0 0 \
		-gcp 0 -3000000 0 -3000 \
		-gcp 4000000 0 4000 0 \
		$@ $^

# Create mbtiles
data/DJI_%.mbtiles:data/DJI_%.JPG
	gdal_translate -a_srs EPSG:3857 \
		-gcp 0 0 0 0 \
		-gcp 4000 3000 4000000 -3000000 \
		-gcp 4000 0 4000000 0 \
		-of mbtiles $^ $@
	gdaladdo $@ \
		2 4 8 16 32 64 128 256 512 1024 2048 \
		4096 8192 16384 32768

renders:
	mkdir -p $@

renders/DJI_%_render.jpg: render-models.py DJI_%.JPG | renders
		pipenv run python $^

data/DJI_%_projected.json: project-data.py data/DJI_%.json
	pipenv run python $^ $@

data/DJI_%_extracted.png: export-renders.py renders/DJI_%_render.jpg data/DJI_%.json
	pipenv run python $^ $@

data/orientations.pdf: compute-orientations.py data/DJI_0045_projected.json data/DJI_0062_projected.json
	pipenv run python $^ $@
