from urllib.parse import urlparse
from urllib.parse import quote

import cbld_edp.config.constants as const
from cbld_edp.config.manager import ConfigManager
from cbld_edp.utils.helpers import Helpers
from cbld_edp.utils.validators import Validators


class APIBuilder:

	"""
	Utils class that includes different methods to build well-formatted solution's API URLs.
	"""

	@staticmethod
	def build_resource_url(fiware_service, fiware_service_path, **kwargs):
		"""
		Builds a REST API call based on the parameters passed and the specification of solution's API.

		:param fiware_service: FIWARE Service which the Data Model belongs to
		:param fiware_service_path: FIWARE Service Path where Data Model is located in its service
		:param kwargs: Filters to apply to the query done to Orion Context Broker (order matters)
		:return: Integration API URL for querying context data
		:rtype: str
		"""
		api_host = APIBuilder.get_host(const.INTEGRATION_API)

		orion_host = APIBuilder.get_host(const.INTEGRATION_ORION)
		orion_host = APIBuilder.encode_orion(orion_host)

		url = '{api_host}/{orion_host}'.format(api_host=api_host, orion_host=orion_host)

		url += '/{param}/{value}'.format(param='entity', value=quote(kwargs['entity']))
		del kwargs['entity']
		for name, value in kwargs.items():
			url += '/{param}/{value}'.format(param=name, value=quote(value))

		url += APIBuilder.build_parameters(fiware_service, fiware_service_path)

		return url

	@staticmethod
	def get_host(key):
		"""
		Obtains the host value specified in the config file.

		:param str key: Key name of wanted host
		:return: Well-formatted host wanted.
		:rtype: str
		"""
		host = ConfigManager.get_value(const.MAIN_SECTION, key)
		Validators.is_valid_url(key, host)
		return APIBuilder.clean_host(host)

	@staticmethod
	def encode_orion(orion_host):
		"""
		Encodes Orion's host in HTTP request compatible format.

		:param str orion_host: Orion's reachable address
		:return: Encoded Orion host
		:rtype: str
		"""
		orion_host_parsed = urlparse(orion_host)
		if orion_host_parsed.path:
			orion_host = '{scheme}://{netloc}{path}'.format(scheme=orion_host_parsed.scheme,
															netloc=orion_host_parsed.netloc,
															path=quote(orion_host_parsed.path))
		return Helpers.encode_base64_url(orion_host)

	@staticmethod
	def clean_host(host):
		"""
		Remove from a host string those characters not desired.

		:param str host: Host value to treat
		:return: Cleaned host string
		:rtype: str
		"""
		if host[-1] is '/':
			host = host[:-1]
		return host

	@staticmethod
	def build_parameters(fiware_service, fiware_service_path):
		"""
		Builds the parameters to add to the API call.

		:param str fiware_service: FIWARE service
		:param fiware_service_path: FIWARE service path
		:return: Portion with HTTP request parameters
		:rtype: str
		"""
		params = ''
		if fiware_service:
			params += const.API_URL_STRUCTURE_FIWARE_SERVICE.format(value=Helpers.encode_base64_url(fiware_service))
			if fiware_service_path:
				if fiware_service_path[0] is '/':
					fiware_service_path = fiware_service_path[1:]
				params += const.API_URL_STRUCTURE_FIWARE_SERVICEPATH.format(
					value=Helpers.encode_base64_url(fiware_service_path))
		return params
