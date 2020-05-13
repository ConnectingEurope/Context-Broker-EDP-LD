import base64
import json
import logging
import os
import re
import uuid
from pathlib import Path

from time_uuid import TimeUUID

import cbld_edp.config.constants as const
import cbld_edp.config.messages as msg
from cbld_edp.config.constants import Model
from cbld_edp.errors.config import NotInformedFieldError
from cbld_edp.utils.validators import Validators


class Helpers(object):
	"""
	Utilities class.
	"""


	@staticmethod
	def generate_uri(host, structure, dataset_type, uuid=None):
		"""
		Builds a URI from the structure and host defined in config file.

		:param str host: Host value for the URI
		:param str structure: Structure used to form the final URL
		:param Model dataset_type: For which element the URI will be generated
		:param str or None uuid: ID in case that already exists. Default: None
		:return: Tuple with well formatted URI and UUID
		:rtype: (str, str)
		"""
		Validators.is_informed(const.URI_HOST, host)

		if not uuid:
			uuid = str(TimeUUID.with_utcnow())

		if dataset_type is Model.CATALOGUE:
			return 'http://{host}/'.format(host=host), uuid

		Validators.is_expected_value(const.URI_STRUCTURE, '{host}', structure)
		if structure[-1] is not '/':
			structure += '/'
		structure += '{type}/'

		return structure.format(host=host, type=dataset_type.value) + uuid, uuid

	@staticmethod
	def get_issued_date(dataset_id):
		"""
		Cleans the value provided to get the issued date of the dataset.

		:param str dataset_id: Dataset's stored identifier.
		:return: The issued date in UTC ISO 8601 format.
		:rtype: str
		"""
		time_uuid = TimeUUID.convert(uuid.UUID('{%s}' % dataset_id))
		return Helpers.format_datetime(time_uuid.get_datetime())

	@staticmethod
	def format_datetime(datetime):
		"""
		Transforms a given date in UTC ISO 8601 format.

		:param datetime.datetime datetime: Date to format.
		:return: UTC ISO 8601 formatted date.
		:rtype: str
		"""
		return datetime.strftime('%Y-%m-%dT%H:%M:%SZ')

	@staticmethod
	def split_uppercase(value):
		"""
		Splits a string based on its upper case characters.

		:param str value: The string to be split.
		:return: A string with blanks between its upper case characters.
		:rtype: str
		"""
		return re.sub(r'([A-Z])', r' \1', value).strip()

	@staticmethod
	def transform_themes(themes):
		"""
		From the dataset.themes field from the config file, transforms them to the URIs defined in DCAT-AP.

		:param list[str] themes: String collection of themes from a dataset.
		:return: Expected theme URIs.
		:rtype: list
		"""
		transformed_themes = []
		if len(themes) > 1 and themes[0]:
			for theme in themes:
				transformed_themes.append(
					Helpers.transform_vocabulary(const.DATASET_THEMES, theme, const.DATASET_THEMES_RELATION))
		return transformed_themes

	@staticmethod
	def transform_vocabulary(field, value, vocabulary):
		"""
		Translates a value used in the config file to a value from a vocabulary.

		:param str field: Name of the field from the configuration file.
		:param str value: Value for the field.
		:param dict vocabulary: Equivalence between config file and DCAT-AP values.
		:return: The value transformed.
		:rtype: str
		"""
		if not value:
			return ''
		Validators.is_expected_value(field, value, list(vocabulary.keys()))
		return vocabulary[value]

	@staticmethod
	def get_spatial_polygon(path):
		"""
		Loads the geometry from a GeoJSON.

		:param str path: GeoJSON file location.
		:return: Tuple which first value is a geometry-like object and the second one a string with geometry coordinates JSON formatted
		:rtype: (str, str)
		:raises NotInformedFieldError:
		"""
		try:
			if os.path.isdir('/'.join(path.split('/')[:-1])):
				if not os.path.exists(path):
					return
			else:
				return

			with open(path) as file:
				geojson = json.load(file)
				if len(geojson['features']) > 1:
					logging.warning(msg.HELPERS_SPATIAL_GEOJSON_NODES.format(path=path))

				geometry = geojson['features'][0]['geometry']
				type = geometry['type']
				geometry = str(geometry['coordinates'])[1:][:-1]

				geometry_json = '"type":"{type}","coordinates":[{coordinates}'.format(type=type,
																					  coordinates=geometry[:-1])
				geometry_json = '{' + geometry_json + ']]}'

				coordinates = re.sub(r'(,?)\s*\[(-?[\d\.]+),\s*(-?[\d\.]+)\]', '\g<1>\g<2> \g<3>', geometry)
				coordinates = coordinates.replace('[', '(').replace(']', ')')
				geometry_object = '{type}({coordinates})'.format(type=type.upper(), coordinates=coordinates)

				return geometry_object, geometry_json
		except OSError:
			raise NotInformedFieldError(None, message=msg.HELPERS_SPATIAL_GEOJSON_FILE_NOT_FOUND.format(path=path))

	@staticmethod
	def encode_base64_url(url):
		"""
		Encodes a URL in Base64 replacing then those chars that may cause troubles when used on a well-formatted URL.

		:param url: URL to encode
		:return: Base64 url
		:rtype: str
		"""
		url = base64.b64encode(url.encode('ascii'))
		url = url.replace(b'+', b'.').replace(b'=', b'').replace(b'/', b'_')
		return url.decode('utf8')

	@staticmethod
	def decode_base64_url(url):
		"""
		Decodes a URL in Base64 replacing first delicate chars put before by encode_base64_url() method.

		:param url: URL to decode
		:return: Usable and readable url
		:rtype: str
		"""
		url = url.replace('.', '+').replace('_', '/')
		missing_padding = len(url) % 4
		if missing_padding:
			url += '=' * (4 - missing_padding)
		url = base64.b64decode(url.encode('ascii'))
		return url.decode('utf8')

	@staticmethod
	def get_project_root():
		"""
		Returns project root folder path.

		:return: Path to project's root
		:rtype: str
		"""
		return str(Path(__file__).parent.parent)

	@staticmethod
	def get_rdf_template_path():
		"""
		Returns RDF template file folder path.

		:return: Path to RDF template file
		:rtype: str
		"""
		return Helpers.get_project_root() + const.RDF_FILE_TEMPLATE_PATH

	@staticmethod
	def get_datasets_ids_file_path():
		"""
		Returns dataset IDs file path.

		:return: Path to config file
		:rtype: str
		"""
		return Helpers.get_project_root() + const.CONFIG_FILE_DATASETS_IDS_PATH

	@staticmethod
	def get_config_file_template_path():
		"""
		Returns configuration file template folder path.

		:return: Path to config file template
		:rtype: str
		"""
		return Helpers.get_project_root() + const.CONFIG_FILE_TEMPLATE_PATH

	@staticmethod
	def get_rdf_path():
		"""
		Returns output RDF file folder path.

		:return: Path to RDF file
		:rtype: str
		"""
		return Helpers.get_project_root() + const.RDF_FILE_PATH
