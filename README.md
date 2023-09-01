# iot-pv-data
Household photovoltaic powerplant data feed for use in IoT

Intended to run on kubernetes and using NATS JetStream for comunication and data storage. 
Project consists of several independent microservices:
* `goodwe-poller` - polling raw data from goodwe inverters and publishing them as JSON data to NATS,
* `pv-filter` - filters configured data and publish changes on them in specified intervals

Not needed?
* `pv-sensors` - provides sensor information (ID, name and unit)
* `pv-runtime` - simple runtime data feed to NATS (power generation/consumption/battery usage),
* `pv-event` - generate events when specified conditions are met (useful for generating alerts),