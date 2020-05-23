cd ..
python -m thinkpol.server run-server rabbitmq://127.0.0.1:5672 &
python -m thinkpol.client upload-sample sample.mind.gz &
python -m thinkpol.parsers run-parser color_image rabbitmq://127.0.0.1:5672 &
python -m thinkpol.parsers run-parser depth_image rabbitmq://127.0.0.1:5672 &
python -m thinkpol.parsers run-parser pose rabbitmq://127.0.0.1:5672 &
python -m thinkpol.parsers run-parser feelings rabbitmq://127.0.0.1:5672 &
python -m thinkpol.saver run-saver mongodb://127.0.0.1:27017 rabbitmq://127.0.0.1:5672 &
