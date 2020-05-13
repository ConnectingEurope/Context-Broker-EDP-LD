import cbld_edp.config.messages as msg


class CouldNotReadRDFError(Exception):
	def __init__(self, payload=None, message=None, short_message=None):
		"""
		This exception is raised when there is a problem accessing RDF file.

		:param int or None status_code: Response's status code
		:param str or None payload: Additional information for the response
		:param str or None message: Custom exception message
		:param str or None short_message: Custom exception short message
		"""
		Exception.__init__(self)
		default_message = msg.API_COULD_NOT_READ_RDF_ERROR
		default_short_message = msg.API_COULD_NOT_READ_RDF_SHORT_ERROR
		self.message = message if message else default_message
		self.status_code = 404
		self.payload = payload
		self.short_message = short_message if short_message else default_short_message


class APIProcessError(Exception):
	def __init__(self, payload=None, message=None, short_message=None):
		"""
		This exception is raised when there is a problem processing the query submitted by the user.

		:param int or None status_code: Response's status code
		:param str or None payload: Additional information for the response
		:param str or None message: Custom exception message
		:param str or None short_message: Custom exception short message
		"""
		Exception.__init__(self)
		default_message = msg.API_PROCESS_FAILED_ERROR
		default_short_message = msg.API_PROCESS_FAILED_SHORT_ERROR
		self.message = message if message else default_message
		self.status_code = 500
		self.payload = payload
		self.short_message = short_message if short_message else default_short_message
