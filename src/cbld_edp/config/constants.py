from pathlib import Path

BASE_PATH = Path(__file__).parent.parent

LOG_FOLDER_PATH = BASE_PATH / 'logs'
TEST_PATH = BASE_PATH / 'tests'

MAIN_SECTION = 'main'

URI_STRUCTURE = 'uri.structure'
URI_HOST = 'uri.host'
INTEGRATION_API = 'integration.api'
INTEGRATION_ORION = 'integration.orion'

CATALOGUE_SECTION = 'catalogue'
CATALOGUE_TITLE = 'title'
CATALOGUE_DESCRIPTION = 'description'
CATALOGUE_PUBLISHER_NAME = 'publisher-name'
CATALOGUE_PUBLISHER_URI = 'publisher-uri'
CATALOGUE_PUBLISHER_HOMEPAGE = 'publisher-homepage'
CATALOGUE_PUBLISHER_TYPE = 'publisher-type'
CATALOGUE_HOMEPAGE = 'homepage'
CATALOGUE_ID = 'id'

DATAMODEL_SECTION = '[datamodel section]'
DATAMODEL_TYPE = 'datamodel.type'
DATAMODEL_FIWARE_SERVICE = 'datamodel.service'
DATAMODEL_FIWARE_SERVICE_PATH = 'datamodel.service-path'
DATASET_TITLE = 'dataset.title'
DATASET_DESCRIPTION = 'dataset.description'
DATASET_CONTACT_POINT = 'dataset.contact-point'
DATASET_KEYWORDS = 'dataset.keywords'
DATASET_PUBLISHER_NAME = 'dataset.publisher-name'
DATASET_PUBLISHER_URI = 'dataset.publisher-uri'
DATASET_PUBLISHER_HOMEPAGE = 'dataset.publisher-homepage'
DATASET_PUBLISHER_TYPE = 'dataset.publisher-type'
DATASET_THEMES = 'dataset.themes'
DATASET_ACCESS_RIGHTS = 'dataset.access-rights'
DATASET_PERIODICITY = 'dataset.periodicity'
DATASET_SPATIAL = 'dataset.spatial'
DATASET_LANDING_PAGE = 'dataset.landing-page'
DATASET_ALLOCATION = 'dataset.allocation'
DATASET_ID = 'dataset.id'
RESOURCE_LICENSE = 'distribution.license'
RESOURCE_LOCATIONS = 'distribution.locations'

DATAMODELS = {
	'Alerts': {
		'models': ['Alert'],
		'allocation': ['location', 'category']
	},
	'Parks & Gardens': {
		'models': ['Garden', 'GreenspaceRecord', 'FlowerBed'],
		'allocation': ['location', 'category']
	},
	'Environment': {
		'models': ['AeroAllergenObserved', 'AirQualityObserved', 'WaterQualityObserved', 'NoiseLevelObserved'],
		'allocation': ['location', 'category']
	},
	'Point of Interest': {
		'models': ['PointOfInterest', 'Beach', 'Museum'],
		'allocation': ['location', 'category']
	},
	'Civic Issue Tracking': {
		'models': ['Open311:ServiceType', 'Open311:ServiceRequest'],
		'allocation': ['category']
	},
	'Street Lightning': {
		'models': ['Streetlight', 'StreetlightModel', 'StreetlightGroup', 'StreetlightControlCabinet'],
		'allocation': ['location', 'category']
	},
	'Device': {
		'models': ['Device', 'DeviceModel'],
		'allocation': ['category']
	},
	'Transportation': {
		'models': ['BikeHireDockingStation', 'Road', 'RoadSegment', 'TrafficFlowObserved', 'Vehicle', 'VehicleModel',
				   'EVChargingStation'],
		'allocation': ['location', 'category']
	},
	'Indicators': {
		'models': ['KeyPerformanceIndicator'],
		'allocation': ['location', 'category']
	},
	'Waste Management': {
		'models': ['WasteContainerIsle', 'WasteContainerModel', 'WasteContainer'],
		'allocation': ['location', 'category']
	},
	'Parking': {
		'models': ['OffStreetParking', 'OnStreetParking', 'ParkingGroup', 'ParkingAccess', 'ParkingSpot'],
		'allocation': ['location', 'category']
	},
	'Weather': {
		'models': ['WeatherObserved', 'WeatherForecast'],
		'allocation': ['location', 'category']
	},

	'Agrifood': {
		'models': ['AgriApp','AgriCrop','AgriFarm','AgriGreenhouse','AgriParcel','AgriParcelOperation',
				   'AgriParcelRecord','AgriPest'],
		'allocation': ['category']
	},
	'Building': {
		'models': ['Building','BuildingOperation'],
		'allocation': ['category']
	},
	'Energy': {
		'models': ['ThreePhaseAcMeasurement'],
		'allocation': ['location']
	},
	'Points of Interaction': {
		'models': ['SmartPointOfInteraction','SmartSpot'],
		'allocation': ['category']
	},
	'Urban Mobility': {
		'models': ['Gtfs Agency','Gtfs Stop','Gtfs Station','GtfsAccessPoint','GtfsRoute','GtfsTrip','GtfsStopTime',
				   'GtfsService','GtfsCalendarRule','GtfsCalendarDateRule','GtfsFrequency','GtfsTransferRule',
				   'GtfsShape ','ArrivalEstimation'],
		'allocation': ['category']
	},
}
DATAMODELS_DEFAULT = {
	'models': '',
	'allocation': ['category', 'location']
}

DATASET_THEMES_RELATION = {
	'agriculture': 'http://publications.europa.eu/resource/authority/data-theme/AGRI',
	'education': 'http://publications.europa.eu/resource/authority/data-theme/EDUC',
	'environment': 'http://publications.europa.eu/resource/authority/data-theme/ENVI',
	'energy': 'http://publications.europa.eu/resource/authority/data-theme/ENER',
	'transport': 'http://publications.europa.eu/resource/authority/data-theme/TRAN',
	'technology': 'http://publications.europa.eu/resource/authority/data-theme/TECH',
	'economy': 'http://publications.europa.eu/resource/authority/data-theme/ECON',
	'social': 'http://publications.europa.eu/resource/authority/data-theme/SOCI',
	'health': 'http://publications.europa.eu/resource/authority/data-theme/HEAL',
	'government': 'http://publications.europa.eu/resource/authority/data-theme/GOVE',
	'regions': 'http://publications.europa.eu/resource/authority/data-theme/REGI',
	'justice': 'http://publications.europa.eu/resource/authority/data-theme/JUST',
	'international': 'http://publications.europa.eu/resource/authority/data-theme/INTR',
	'provisional': 'http://publications.europa.eu/resource/authority/data-theme/OP_DATPRO'
}
DATASET_FREQUENCY_RELATION = {
	'triennial': 'http://publications.europa.eu/resource/authority/frequency/TRIENNIAL',
	'biennial': 'http://publications.europa.eu/resource/authority/frequency/BIENNIAL',
	'annual': 'http://publications.europa.eu/resource/authority/frequency/ANNUAL',
	'semiannual': 'http://publications.europa.eu/resource/authority/frequency/ANNUAL_2',
	'three_times_year': 'http://publications.europa.eu/resource/authority/frequency/ANNUAL_3',
	'quarterly': 'http://publications.europa.eu/resource/authority/frequency/QUARTERLY',
	'bimonthly': 'http://publications.europa.eu/resource/authority/frequency/BIMONTHLY',
	'monthly': 'http://publications.europa.eu/resource/authority/frequency/MONTHLY',
	'semimonthly': 'http://publications.europa.eu/resource/authority/frequency/MONTHLY_2',
	'biweekly': 'http://publications.europa.eu/resource/authority/frequency/BIWEEKLY',
	'three_times_month': 'http://publications.europa.eu/resource/authority/frequency/MONTHLY_3',
	'weekly': 'http://publications.europa.eu/resource/authority/frequency/WEEKLY',
	'semiweekly': 'http://publications.europa.eu/resource/authority/frequency/WEEKLY_2',
	'three_times_week': 'http://publications.europa.eu/resource/authority/frequency/WEEKLY_3',
	'daily': 'http://publications.europa.eu/resource/authority/frequency/DAILY',
	'continuously': 'http://publications.europa.eu/resource/authority/frequency/UPDATE_CONT',
	'irregular': 'http://publications.europa.eu/resource/authority/frequency/IRREG',
	'unknown': 'http://publications.europa.eu/resource/authority/frequency/UNKNOWN',
	'other': 'http://publications.europa.eu/resource/authority/frequency/OTHER',
	'twice_day': 'http://publications.europa.eu/resource/authority/frequency/DAILY_2',
	'continuous': 'http://publications.europa.eu/resource/authority/frequency/CONT',
	'never': 'http://publications.europa.eu/resource/authority/frequency/NEVER',
	'quadrennial': 'http://publications.europa.eu/resource/authority/frequency/QUADRENNIAL',
	'quinquennial': 'http://publications.europa.eu/resource/authority/frequency/QUINQUENNIAL',
	'hourly': 'http://publications.europa.eu/resource/authority/frequency/HOURLY',
	'decennial': 'http://publications.europa.eu/resource/authority/frequency/DECENNIAL',
	'provisional': 'http://publications.europa.eu/resource/authority/frequency/OP_DATPRO'
}
DATASET_ACCESS_RIGHTS_RELATION = {
	'public': 'http://publications.europa.eu/resource/authority/access-right/PUBLIC',
	'restricted': 'http://publications.europa.eu/resource/authority/access-right/RESTRICTED',
	'non_public': 'http://publications.europa.eu/resource/authority/access-right/NON_PUBLIC',
	'provisional': 'http://publications.europa.eu/resource/authority/access-right/OP_DATPRO'
}
PUBLISHER_TYPE_RELATION = {
	'academia_scientific_org': 'http://purl.org/adms/publishertype/Academia-ScientificOrganisation',
	'company': 'http://purl.org/adms/publishertype/Company',
	'industry_consortium': 'http://purl.org/adms/publishertype/IndustryConsortium',
	'local_authority': 'http://purl.org/adms/publishertype/LocalAuthority',
	'national_authority': 'http://purl.org/adms/publishertype/NationalAuthority',
	'nongovernmental_org': 'http://purl.org/adms/publishertype/NonGovernmentalOrganisation',
	'nonprofit_org': 'http://purl.org/adms/publishertype/NonProfitOrganisation',
	'private_individual': 'http://purl.org/adms/publishertype/PrivateIndividual(s)',
	'regional_authority': 'http://purl.org/adms/publishertype/RegionalAuthority',
	'standardisation_body': 'http://purl.org/adms/publishertype/StandardisationBody',
	'supranational_authority': 'http://purl.org/adms/publishertype/SupraNationalAuthority'
}

RDF_CATALOGUE = 'dcat:Catalog'
RDF_CATALOGUE_DATASET = 'dcat:dataset'
RDF_DATASET = 'dcat:Dataset'
RDF_DATASET_RESOURCE = 'dcat:distribution'
RDF_RESOURCE = 'dcat:Distribution'
RDF_ORGANIZATION = 'foaf:Organization'
RDF_ATTRIBUTE_ABOUT = 'rdf:about'
RDF_ATTRIBUTE_RESOURCE = 'rdf:resource'
RDF_IDENTIFIER = 'dct:identifier'
RDF_TITLE = 'dct:title'
RDF_DESCRIPTION = 'dct:description'
RDF_PUBLISHER = 'dct:publisher'
RDF_HOMEPAGE = 'foaf:homepage'
RDF_TYPE = 'rdf:type'
RDF_ISSUED = 'dct:issued'
RDF_MODIFIED = 'dct:modified'
RDF_THEME = 'dcat:theme'
RDF_KEYWORD = 'dcat:keyword'
RDF_CONTACT_POINT = 'dcat:contactPoint'
RDF_CONTACT_POINT_NAME = 'vcard:fn'
RDF_CONTACT_POINT_EMAIL = 'vcard:hasEmail'
RDF_PERIODICITY = 'dct:accrualPeriodicity'
RDF_RIGHTS = 'dct:accessRights'
RDF_LANDING_PAGE = 'dcat:landingPage'
RDF_SPATIAL = 'dct:spatial'
RDF_SPATIAL_GEOMETRY = 'locn:geometry'
RDF_ACCESS_URL = 'dcat:accessURL'
RDF_DOWNLOAD_URL = 'dcat:downloadURL'
RDF_LICENSE = 'dct:license'
RDF_ORGANIZATION_NAME = 'foaf:name'
RDF_ELEMENT_XPATH = './/{element}'
RDF_ATTRIBUTE_XPATH = '{element}[@{attribute}="{value}"]'

from enum import Enum


class Model(Enum):
	CATALOGUE = 'catalogue'
	DATASET = 'dataset'
	RESOURCE = 'distribution'

class Allocation(Enum):
	CATEGORY = 'category'
	LOCATION = 'location'

API_FIWARE_TOTAL_COUNT_HEADER = 'Fiware-Total-Count'
API_FIWARE_RESPONSE_IGNORE_HEADERS = ['Content-Encoding', 'Transfer-Encoding']
API_FIWARE_SERVICE = 'fiware-service'
API_FIWARE_SERVICEPATH = 'fiware-servicepath'
API_FIWARE_URL_STRUCTURE = '{host}/ngsi-ld/v1/entities?type=https://uri.fiware.org/ns/data-models%23{entity}&options=count'
API_FIWARE_URL_STRUCTURE_LOCATION = '&address.addressRegion={location}&address.addressLocality={location}'
API_URL_STRUCTURE_FIWARE_SERVICE = '?fs={value}'
API_URL_STRUCTURE_FIWARE_SERVICEPATH = '&fp={value}'
API_URL_STRUCTURE = '/<regex("[\w\-\.~:/?#\[\]@!$&\'()*+,;=]*/?"):rel_path>api/{route}'
API_URL_STATUS = 'status'
CONFIG_FILE_DEFAULT_PATH = '/etc/cb_edp.ini'
CONFIG_FILE_TEMPLATE_PATH = '/config/template.ini'
CONFIG_FILE_DATASETS_IDS_PATH = '/config/integrated.ini'
RDF_FILE_NAME = 'catalogue.rdf'
RDF_FILE_PATH = '/api/' + RDF_FILE_NAME
RDF_FILE_TEMPLATE_PATH = '/core/rdf/template.xml'
URI_STRUCTURE_DEFAULT = 'http://{host}/cb/'

DEFAULT_DATAMODEL_OPTION_COMMAND = 'all'
SIMPLE_DATE_FORMAT = '%H:%M:%S'
