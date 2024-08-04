import asyncio
import goodwe
import json
import nats
import os
import pprint

from nats.aio.client import Client as NATS

'''
Service polling goodwe inverter for data in regular intervals and publishing them to NATS subject.
Parameters are defined using following environment variables:
    GWP_ADDRESS - IP address or hostname of the inverter
    GWP_INTERVAL - polling interval in seconds (default: 60)
    NATS_URL - URL of the NATS server (default: "nats://localhost:4222")
    NATS_SUBJECT - NATS subject to publish data to (default: "home.pv.inverter.data")
    NATS_CREDS - path to credentials file for NATS server (default: None)
'''

async def main():
    # Import environment variables
    goodwe_address = os.getenv("GWP_ADDRESS", "goodwe")
    # goodwe_port = int(os.getenv("GWP_PORT", 8899))
    goodwe_interval = int(os.getenv("GWP_INTERVAL", 60))
    nats_url = os.getenv("NATS_URL", "nats://localhost:4222")
    nats_subject = os.getenv("NATS_SUBJECT", "home.pv.inverter.data")
    nats_creds = os.getenv("NATS_CREDS", None)

    # Create goodwe client
    inverter = await goodwe.connect(goodwe_address)

    # Connect to NATS server
    nc = NATS()
    await nc.connect(nats_url, user_credentials=nats_creds)

    # Polling loop
    while True:
        # Get data from inverter
        data = await inverter.read_runtime_data()

        # Publish data to NATS
        data['timestamp'] = int(data['timestamp'].timestamp())
        # pprint.pprint(data)
        print("Publishing: timestamp: {}, battery: {}%, pv: {} W, load: {} W, backup: {} W".format(data['timestamp'], data['battery_soc'], data['ppv'], data['load_ptotal'], data['backup_ptotal']))
        await nc.publish(nats_subject, bytes(json.dumps(data), 'utf-8'))

        # Wait for next polling interval
        await asyncio.sleep(goodwe_interval)


if __name__ == "__main__":
    asyncio.run(main())