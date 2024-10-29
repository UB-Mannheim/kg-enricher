import geopandas as gpd
import pkg_resources
import requests
from shapely.geometry import Point

# Configuration
wikibase_api_url = "https://www.wikidata.org/w/api.php"
wikibase_special_entitydata = "https://www.wikidata.org/wiki/Special:EntityData/"
coordinate_property = 'P625'
person_properties = {'P569': 'date_of_birth', 'P570': 'date_of_death', 'P214': 'VIAF ID', 'P213': 'ISNI', 'P496': 'ORCID iD', 'P227': 'GND ID', 'P244': 'Library of Congress authority ID', 'P2671': 'Google Knowledge Graph ID', 'P646': 'Freebase ID'}
org_properties = {'P571': 'inception', 'P576': 'dissolution', 'P3220': 'OpenCorporates ID', 'P1278': 'LEI code', 'P2427': 'GRID ID', 'P946': 'ISIN', 'P2657': 'EU Transparency Register ID', 'P2671': 'Google Knowledge Graph ID', 'P646': 'Freebase ID', 'P5785': 'EU Research participant ID', 'P10301': 'German Lobbyregister ID', 'P4264': 'LinkedIn organization ID', 'P3347': 'PermID', 'P4293': 'PM20 folder ID'}
geo_properties = {'P625': 'geographic coordinates', 'P1566': 'GeoNames ID', 'P402': 'OSM Relation ID', 'P440': 'German district key', 'P439': 'German municipality key', 'P1388': 'German regional key', 'P1937': 'UN/LOCODE', 'P2671': 'Google Knowledge Graph ID', 'P646': 'Freebase ID', 'P590': 'GNIS ID', 'P774': 'FIPS 55-3', 'P11693': 'OpenStreetMap node ID'}

# Load boundary data for Germany
historical_germany_1886_1919 = gpd.read_file(pkg_resources.resource_filename('enricher', '84.json'))
historical_germany_1919_1920 = gpd.read_file(pkg_resources.resource_filename('enricher', '85.json'))
historical_germany_1920_1938 = gpd.read_file(pkg_resources.resource_filename('enricher', '86.json'))
historical_germany_1938_1945 = gpd.read_file(pkg_resources.resource_filename('enricher', '87.json'))
historical_GFR_1945_1949 = gpd.read_file(pkg_resources.resource_filename('enricher', '88.json'))
historical_GFR_1949_1990 = gpd.read_file(pkg_resources.resource_filename('enricher', '89.json'))
historical_GFR_1990_2019 = gpd.read_file(pkg_resources.resource_filename('enricher', '90.json'))
historical_GDR_1945_1949 = gpd.read_file(pkg_resources.resource_filename('enricher', '91.json'))
historical_GDR_1949_1990 = gpd.read_file(pkg_resources.resource_filename('enricher', '92.json'))
current_germany_boundary = historical_GFR_1990_2019


def is_within_boundary(lat, lon, boundary_gdf):
    point = Point(lon, lat)
    return any(boundary_gdf.contains(point))


def query_wikibase(entity, limit=1, api_url=wikibase_api_url):
    search_url = f"{api_url}?action=wbsearchentities&search={entity}&language=en&format=json&limit={limit}"
    search_response = requests.get(search_url).json()
    if search_response.get('search'):
        return [result['id'] for result in search_response['search'][:limit]]
    return []


def get_label_description_aliases(data, language='en'):
    label = data['labels'][language]['value'] if language in data['labels'] else None
    description = data['descriptions'][language]['value'] if language in data['descriptions'] else None
    aliases = [alias['value'] for alias in data['aliases'][language]] if language in data['aliases'] else []

    return {
        'label': label, 
        'description': description, 
        'aliases': aliases
    }


def get_coordinates(entity_id, special_entitydata_url=wikibase_special_entitydata, coordinate_property_id=coordinate_property):
    url = f"{special_entitydata_url}{entity_id}.json"
    response = requests.get(url).json()
    data = response['entities'][entity_id]
    if coordinate_property_id in data['claims']:
        coordinates_claim = data['claims'][coordinate_property_id][0]['mainsnak']['datavalue']['value']
        return {'latitude': coordinates_claim['latitude'], 'longitude': coordinates_claim['longitude']}
    return None


def determine_properties(entity_data, entity_type=None):
    """
    Determines the properties to fetch based on the entity type. 
    If entity_type is None, it does not filter by type and returns the appropriate properties.
    """
    if entity_type == "per":
        if 'P31' in entity_data['claims'] and any(x['mainsnak']['datavalue']['value']['id'] == 'Q5' for x in entity_data['claims']['P31']):
            return person_properties
    elif entity_type == "geo":
        if coordinate_property in entity_data['claims']:
            return geo_properties
    elif entity_type == "org":
        return org_properties
    elif entity_type is None:
        # Determine properties without filtering by type
        if 'P31' in entity_data['claims'] and any(x['mainsnak']['datavalue']['value']['id'] == 'Q5' for x in entity_data['claims']['P31']):
            return person_properties
        elif coordinate_property in entity_data['claims']:
            return geo_properties
        else:
            return org_properties
    return None


def extract_information(entity_id, properties_to_fetch, language='en'):
    entity_data = fetch_entity_data(entity_id)
    if entity_data:
        info = get_label_description_aliases(entity_data, language)
        info['id'] = entity_id
        info['url'] = f"{wikibase_special_entitydata}{entity_id}"

        # Fetch external identifiers and other properties
        for prop_id, prop_label in properties_to_fetch.items():
            if prop_id in entity_data['claims']:
                prop_values = entity_data['claims'][prop_id]
                if prop_values:
                    value = prop_values[0]['mainsnak']['datavalue']['value']
                    if isinstance(value, dict):
                        info[prop_label] = value.get('id') if 'id' in value else value
                    else:
                        info[prop_label] = value

        # Check if it's a geographic entity and if so, check if it's within current or historical Germany boundaries
        if properties_to_fetch == geo_properties:
            coordinates = get_coordinates(entity_id)
            if coordinates:
                lat, lon = coordinates['latitude'], coordinates['longitude']
                info['is_within_current_germany'] = is_within_boundary(lat, lon, current_germany_boundary)
                info['is_within_historical_germany_1886_1919'] = is_within_boundary(lat, lon, historical_germany_1886_1919)
                info['is_within_historical_germany_1919_1920'] = is_within_boundary(lat, lon, historical_germany_1919_1920)
                info['is_within_historical_germany_1920_1938'] = is_within_boundary(lat, lon, historical_germany_1920_1938)
                info['is_within_historical_germany_1938_1945'] = is_within_boundary(lat, lon, historical_germany_1938_1945)
                info['is_within_historical_GFR_1945_1949'] = is_within_boundary(lat, lon, historical_GFR_1945_1949)
                info['is_within_historical_GFR_1949_1990'] = is_within_boundary(lat, lon, historical_GFR_1949_1990)
                info['is_within_historical_GFR_1990_2019'] = is_within_boundary(lat, lon, historical_GFR_1990_2019)
                info['is_within_historical_GDR_1945_1949'] = is_within_boundary(lat, lon, historical_GDR_1945_1949)
                info['is_within_historical_GDR_1949_1990'] = is_within_boundary(lat, lon, historical_GDR_1949_1990)
        return info
    else:
        return {'error': 'Entity data not found'}


def fetch_entity_data(entity_id, special_entitydata_url=wikibase_special_entitydata):
    url = f"{special_entitydata_url}{entity_id}.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['entities'][entity_id]
    else:
        return None


def enrich(entity_string, limit=1, language='en', entity_type=None):
    """
    Enriches entities optionally based on the specified entity_type: "per" for person, "org" for organization, "geo" for geographic entity.
    If entity_type is None, it enriches with an entity of any entity type.
    """
    entity_ids = query_wikibase(entity_string, limit=limit)
    if entity_ids:
        results = []
        for entity_id in entity_ids:
            entity_data = fetch_entity_data(entity_id)
            if entity_data:
                properties_to_fetch = determine_properties(entity_data, entity_type)
                if properties_to_fetch:
                    enriched_data = extract_information(entity_id, properties_to_fetch, language)
                    results.append(enriched_data)
                else:
                    results.append({'error': 'Entity does not match the specified entity type', 'id': entity_id})
            else:
                results.append({'error': 'Entity data not found', 'id': entity_id})
        return results
    return [{'error': 'Entity ID not found for given string'}]
