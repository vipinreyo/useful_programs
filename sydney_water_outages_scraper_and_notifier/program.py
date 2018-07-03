import sys

import requests

URL = 'https://www.sydneywater.com.au/wrs/water_service_updates/geojson/wo_low_v3.geojson'


def get_outage():
    resp = requests.get(URL)
    resp.raise_for_status()
    return resp.json()


def get_outage_data(suburb, data):
    outages = []
    for d in data.get('features'):
        location = d.get('properties').get('location')
        if suburb in location.lower():
            status = d.get('properties').get('type')
            water_off = d.get('properties').get('water_off_a')
            last_updated = d.get('properties').get('updated')

            if status == 'RESOLVED':
                water_on = d.get('properties').get('water_on_a')
                status = 'Work completed'
                outages.append('Location: {}, Status: {}, Water off: {}, Water on: {}, Last updated on: {}'.
                               format(location, status, water_off, water_on, last_updated))

            if status == 'CURRENT':
                water_on_planned = d.get('properties').get('water_on_p')
                status = 'Work in progress'
                outages.append('Location: {}, Status: {}, Water off: {}, Water on (planned): {}, Last updated on: {}'.
                               format(location, status, water_off, water_on_planned, last_updated))

    return outages


def main():
    suburb = input('Enter your suburb details: ').strip().lower()

    if not suburb:
        print('Please enter a valid Suburb name. Exiting....')
        sys.exit(1)

    data = get_outage()
    outages = get_outage_data(suburb, data)

    print('-'*20)
    print('Outages in {}: {}'.format(suburb.title(), 'None' if not len(outages) else ''))
    print('-'*20)

    for outage in outages:
        print(outage)


if __name__ == '__main__':
    main()
