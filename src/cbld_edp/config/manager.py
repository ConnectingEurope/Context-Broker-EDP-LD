import os

from configobj import ConfigObj
from configobj import ConfigObjError

import cbld_edp.config.constants as const
from cbld_edp.errors.config import ConfigFilePathError
from cbld_edp.errors.config import NoIDForDataModelError
from cbld_edp.errors.config import SectionKeyError
from cbld_edp.utils.helpers import Helpers


class ConfigManager:
	"""
	Configuration files manager class. Implements the methods needed to work with the main solution's configuration
	file and the file used to store datasets' IDs. It works as a singleton.
	"""
	__instance = None
	__datasets_ids = None
	__config_file_path = None

	def __init__(self, config_file_path):
		"""
        Instantiate the ConfigManager class.

        :param str config_file_path: Path where the config file is located.
        :raises: ConfigObjError ConfigFilePathError
        """
		try:

			self.__config = ConfigObj(config_file_path, write_empty_values=True, list_values=False, encoding='utf8',
									  raise_errors=True)
		except ConfigObjError as error:
			raise ConfigObjError(error.msg.strip('.'))
		except Exception:
			raise ConfigFilePathError(config_file_path)

	@classmethod
	def get_instance(cls):
		"""
        Singleton method that retrieves the main ConfigManager instance.
        If it is not instantiated yet, it does it with the __config_file_path that must be previously specified.

        :return: The ConfigManager class singleton.
        :rtype: ConfigManager
        """
		if cls.__instance is None:
			cls.__instance = ConfigManager(cls.__config_file_path)
		return cls.__instance

	@classmethod
	def get_datasets_ids_instance(cls):
		"""
		Singleton method that retrieves the ConfigManager instance for the datasets IDs storing file.
		If it is not instantiated yet, it does it with the the static defined path.

		:return: The ConfigManager class singleton.
		:rtype: ConfigManager
		"""
		if cls.__datasets_ids is None:
			cls.__datasets_ids = ConfigManager(Helpers.get_datasets_ids_file_path())
		return cls.__datasets_ids

	@classmethod
	def set_config_path(cls, config_file_path):
		"""
        Sets the value for the configuration file location.

        :param str config_file_path: Path where the config file is.
        :return: None
        """
		if os.path.isdir('/'.join(config_file_path.split('/')[:-1])):
			if os.path.exists(config_file_path):
				cls.__config_file_path = config_file_path
				return
		raise ConfigFilePathError(config_file_path)

	@classmethod
	def _get_configobj(cls, config_manager):
		"""
        Returns the previously set property __config parser for a config manager.

        :param ConfigManager config_manager: Instance of the config manager
        :return: The instance of the ConfigObj class
        :rtype: ConfigObj
        """
		return config_manager.__config

	@classmethod
	def set_value(cls, section, key, value):
		"""
        Given a section, a key and a value, writes the value to the corresponding section-key in the file.

        :param str section: Section where the key is located in config file.
        :param str key: Name of the key corresponding to the value to be added.
        :param str value: value to be added in the corresponding section-key.
        :return: None
        """
		cls._get_configobj(cls.get_instance())[section][key] = value

	@classmethod
	def get_value(cls, section, key, default=''):
		"""
        Reads a value from the config file.
        Raises a KeyError exception if either section or key are not preset.

        :param section: Section where the key is located in config file.
        :param key: Name of the key whose value has to be returned.
        :param default: If the field is empty the method will return this value.
        :return: The value of the corresponding section-key.
        :rtype: str
        :raises SectionKeyError:
        """
		try:
			value = cls._get_configobj(cls.get_instance())[section][key]
			return value if value else default
		except KeyError:
			raise SectionKeyError(section, key)

	@classmethod
	def get_keys(cls, section):
		"""
		Returns the keys present in the configuration file for a specific section.

        :param str section: Section of the config file whose keys have to be returned
        :return: Collection of keys for a given section
        :rtype: list[str]
        """
		return [key for key in cls._get_configobj(cls.get_instance())[section]]

	@classmethod
	def get_datamodels(cls):
		"""
		Returns the entire list of Data Models specified in the configuration file.

		:return: Data Models written in config file
		:rtype: list[str]
		"""
		sections = cls._get_configobj(cls.get_instance()).keys()
		for section in [const.MAIN_SECTION, const.CATALOGUE_SECTION]:
			sections.remove(section)
		return sections

	@classmethod
	def update_file(cls):
		"""
        Writes all the changes made using the set_ methods in the config file.

        :return: None
        """
		cls._get_configobj(cls.get_instance()).write()

	@classmethod
	def get_dataset_id(cls, datamodel):
		"""
		Reads from the datasets IDs file the ID for a Data Model.

		:param str datamodel: Data Model to look for
		:return: ID of the given Data Model
		:rtype: str
		"""
		ids = cls._get_configobj(cls.get_datasets_ids_instance())
		if datamodel in ids:
			return ids[datamodel]
		else:
			return ''

	@classmethod
	def save_dataset_id(cls, datamodel, id):
		"""
		Saves the ID of a dataset/Data Model in the datasets IDs file writing it on disk.

		:param str datamodel: Data Model whose ID will be stored
		:param str id: Dataset ID to store
		:return: None
		"""
		ids = cls._get_configobj(cls.get_datasets_ids_instance())
		ids[datamodel] = id
		ids.write()

	@classmethod
	def remove_dataset_id(cls, datamodel):
		"""
		Removes from the datasets IDs file the entry of a given Data Model.

		:param str datamodel: Data Model whose ID will be removed
		:return: None
		"""
		ids = cls._get_configobj(cls.get_datasets_ids_instance())
		if datamodel not in ids:
			raise NoIDForDataModelError(datamodel)
		ids.pop(datamodel)
		ids.write()

	@classmethod
	def get_integrated_datasets(cls):
		"""
		Returns a collection with the Data Models already integrated.

		:return: List with the Data Models integrated
		:rtype: list[str]
		"""
		ids = cls._get_configobj(cls.get_datasets_ids_instance())
		return list(ids.keys())
