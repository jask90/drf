#!/bin/sh

python3.8 /opt/drf/drf/manage.py flush --no-input
python3.8 /opt/drf/drf/manage.py makemigrations
python3.8 /opt/drf/drf/manage.py migrate

python3.8 /opt/drf/drf/manage.py loaddata /opt/drf/drf/drf/fixtures/users.json
python3.8 /opt/drf/drf/manage.py loaddata /opt/drf/drf/hotels/fixtures/hotels.json
python3.8 /opt/drf/drf/manage.py loaddata /opt/drf/drf/hotels/fixtures/rooms.json
python3.8 /opt/drf/drf/manage.py loaddata /opt/drf/drf/hotels/fixtures/rates.json
python3.8 /opt/drf/drf/manage.py loaddata /opt/drf/drf/hotels/fixtures/inventories.json
python3.8 /opt/drf/drf/manage.py loaddata /opt/drf/drf/drf/fixtures/applications.json

