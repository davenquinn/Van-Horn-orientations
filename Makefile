proj := data/DJI_0062_projected.json

all: $(proj)

install:
	pipenv install

data/DJI_0062.json: data/DJI_0062.db
	ogr2ogr -nln linework -of GeoJSON \
		-gcp 0 0 0 0 \
		-gcp 0 -3000000 0 -3000 \
		-gcp 4000000 0 4000 0 \
		$@ $^

# Create mbtiles
data/DJI_0062.mbtiles:data/DJI_0062.PNG
	gdal_translate -a_srs EPSG:3857 \
		-gcp 0 0 0 0 \
		-gcp 4000 3000 4000000 -3000000 \
		-gcp 4000 0 4000000 0 \
		-of mbtiles $^ $@
	gdaladdo DJI_0062.mbtiles \
		2 4 8 16 32 64 128 256 512 1024 2048 \
		4096 8192 16384

$(proj): project-data.py data/DJI_0062.json
	pipenv run python $^ $@
