import cbld_edp.config.messages as msg


class ConfigFilePathError(Exception):
	def __init__(self, path, message=None):
		"""
		This exception is raised if the path informed for the configuration file is not correct.

		:param str or None path: Provided path to config file
		:param str or None message: Custom exception message
		"""
		default_message = msg.CONFIG_FILE_PATH_ERROR.format(path=path)
		super(ConfigFilePathError, self).__init__(message if message else default_message)


class NotInformedFieldError(Exception):
	def __init__(self, field, message=None):
		"""
		This exception is raised if a field is not informed in the configuration file.

		:param str or None field: Name of the field not informed
		:param str or None message: Custom exception message
		"""
		default_message = msg.NOT_INFORMED_FIELD_ERROR.format(field=field)
		super(NotInformedFieldError, self).__init__(message if message else default_message)


class WrongFormatError(Exception):
	def __init__(self, field, value, message=None):
		"""
		This exception is raised when a value has wrong format.

		:param str or None field: Name of the field
		:param str or None value: Value of the field
		:param str or None message: Custom exception message
		"""
		default_message = msg.WRONG_FORMAT_ERROR.format(field=field, value=value)
		super(WrongFormatError, self).__init__(message if message else default_message)


class SectionKeyError(Exception):
	def __init__(self, section, key, message=None):
		"""
		This exception is raised if a key is not present in the given section.

		:param str or None section: Section from the configuration file
		:param str or None key: Key of a section for a value from the configuration file
		:param str or None message: Custom exception message
		"""
		default_message = msg.SECTION_KEY_ERROR.format(key=key, section=section)
		super(SectionKeyError, self).__init__(message if message else default_message)


class NotExpectedValueError(Exception):
	def __init__(self, field, value, choices, message=None):
		"""
		This exception is raised if a field is informed with a value not expected.

		:param str or None field: Name of the field wrong informed
		:param str or None value: Value of the field
		:param str or list[str] or None choices: Collection of possible values for the field
		:param str or None message: Custom exception message
		"""
		if type(choices) is list:
			choices = ', '.join(choices)
		default_message = msg.NOT_EXPECTED_VALUE_ERROR.format(field=field, value=value, choices=choices)
		super(NotExpectedValueError, self).__init__(message if message else default_message)


class NoIDForDataModelError(Exception):
	def __init__(self, datamodel, message=None):
		"""
		This exception is raised if a Data Model's ID should exist but it does not.

		:param str datamodel: Name of the Data Model without ID
		:param str or None message: Custom exception message
		"""
		default_message = msg.NOT_ID_FOR_DATAMODEL_ERROR.format(datamodel=datamodel)
		super(NoIDForDataModelError, self).__init__(message if message else default_message)
