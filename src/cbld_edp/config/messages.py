# commands.py
COMMANDS_INTEGRATE_PROMPT = 'You have already generated an RDF file. Do you want to continue?'
COMMANDS_NEW_CONFIG_PROMPT = 'You have already generated a configuration file. Do you want to continue?'
COMMANDS_HELP_CONFIG_FILE = 'The configuration file path.  [optional]'
COMMANDS_HELP_DATAMODELS = 'Name of the Data Models to {command} separated by blanks. Use "{option}" to {command} every Data Model.'
COMMANDS_HELP_OVERWRITE = 'Ignore confirmation and overwrite existing file.'
COMMANDS_SHOW_INTEGRATED_DATAMODELS = 'Data Models available in the RDF file:'
COMMANDS_SHOW_INTEGRATED_DATAMODELS_EMPTY = 'You have not integrated any Data Models yet.'

# edp.py
EDP_INITIALIZING = 'Initializing CB-EDP integration process (instantiating EDP core class)'
EDP_READING_CONFIG = 'Reading config file from {path}'
EDP_CHECK_API_STATUS = 'Checking if solution\'s API at {host} is up...'
EDP_API_STATUS_DOWN = '{host} seems to be down. Check if solution\'s API host is set correctly in config file or if the server is up'
EDP_INTEGRATION_START = 'Starting integration process for {datamodels} Data Model/s'
EDP_INTEGRATION_FINISHED_OK = 'Integration process finished successfully'
EDP_INTEGRATION_FINISHED_KO = 'Integration process finished with errors'
EDP_MODIFICATION_START = 'Starting integration modification process for {datamodels} Data Model/s'
EDP_MODIFICATION_FINISHED_OK = 'Integration modification process finished successfully'
EDP_MODIFICATION_FINISHED_KO = 'Integration modification process finished with errors'
EDP_DELETE_START = 'Starting integration removal process for {datamodels} Data Model/s'
EDP_DELETE_FINISHED_OK = 'Integration removal process finished successfully'
EDP_DELETE_FINISHED_KO = 'Integration removal process finished with errors'
EDP_CONFIG_FILE_GENERATION = 'Configuration file created successfully at {path}'
EDP_CONFIG_FILE_GENERATION_FAILED = 'Cannot create configuration file: Permission denied'
EDP_ERROR_INSTANTIATING_LOGGER = "{date} ERROR    [{script}] Permission denied: you must run cb-edp as sudoer"

# /api/main.py
API_STATUS_OK = 'CBLD-EDP API service running'

# /errors/api.py
API_COULD_NOT_READ_RDF_SHORT_ERROR = 'Error trying to access RDF file'
API_COULD_NOT_READ_RDF_ERROR = 'There was an error trying to access the RDF/XML: file not found in filesystem.'
API_PROCESS_FAILED_SHORT_ERROR = 'Error during query processing'
API_PROCESS_FAILED_ERROR = 'There was an error processing your query. Check API service logs or contact application administrator.'

# /errors/config.py
CONFIG_FILE_PATH_ERROR = 'There was a problem with the path to config file: {path}'
NOT_INFORMED_FIELD_ERROR = 'Field "{field}" is not informed'
WRONG_FORMAT_ERROR = 'Field "{field}" value is not well-formatted: {value}'
SECTION_KEY_ERROR = 'Key "{key}" is not present in section "{section}" from config file'
NOT_EXPECTED_VALUE_ERROR = 'Field "{field}" value ({value}) not expected. Possible values: {choices}'
NOT_ID_FOR_DATAMODEL_ERROR = 'ID for Data Model "{datamodel}" not found'

# /errors/rdf.py
WRITING_RDF_ERROR = 'There was an error trying to write the RDF file in disk: {path}'
RDF_FILE_NOT_FOUND_ERROR = 'RDF/XML file not found when trying to load XML tree at: {path}'
RDF_PARSING_ERROR = 'There was a problem parsing the RDF/XML file at "{path}". Maybe it is malformed?'
DATASET_NOT_FOUND_ERROR = 'Dataset for "{datamodel}" Data Model not found in RDF file'
LAST_DATASET_ERROR = 'Removing last dataset in RDF file. This will remove entire RDF file'

# /model/catalogue.py
CATALOGUE_INSTANTIATING_MODEL_START = 'Instantiating new Catalogue model for {datamodels} Data Models from config file info'
CATALOGUE_INSTANTIATING_MODEL_FINISHED = 'New Catalogue model instantiating process finalized successfully'
CATALOGUE_DATASETS_CREATED = '{datasets} dataset/s created'

# /model/dataset.py
DATASET_INSTANTIATING_MODEL_START = 'Instantiating new Dataset model for "{datamodel}" Data Model from config file info'
DATASET_INSTANTIATING_MODEL_FINISHED = 'New Dataset model instantiating process finalized successfully'
DATASET_SAVING_ID = 'Saving {datamodel} dataset ID: {id}'
DATASET_RESOURCES_CREATED = '{resources} distribution/s created for "{datamodel}" dataset'

# /model/resource.py
RESOURCE_INSTANTIATING_MODEL_START = 'Instantiating new Resource model for "{datamodel}" Data Model from config file info'
RESOURCE_INSTANTIATING_MODEL_FINISHED = 'New Resource model instantiating process finalized successfully'
RESOURCE_CREATE_RESOURCES = 'Building resources collection by {allocation} for {datamodels} Data Models'
RESOURCE_CREATE_RESOURCE_ENTITY = 'New resource "{name}" for "{datamodel}" created'
RESOURCE_CREATE_RESOURCE_LOCATION = 'New resource "{name}" for "{datamodel}" and {location} location created'
RESOURCE_DESCRIPTION = 'Results can be paginated using "offset" and "limit" as URL parameters'
RESOURCE_TITLE_LOCATION = '{datamodel} in {location}'

# /rdf/rdf.py
SERIALIZER_RDF_CREATION_START = 'Creating new RDF/XML file from scratch'
SERIALIZER_RDF_CREATION_FINISHED = 'RDF/XML file creation process finished successfully'
SERIALIZER_RDF_UPDATE_START = 'Updating already created RDF file with "{dataset}" dataset'
SERIALIZER_RDF_UPDATE_NEW_DATASET = 'Adding new dataset to RDF file: {dataset}'
SERIALIZER_RDF_UPDATE_FINISHED = 'RDF file update with "{dataset}" dataset finished successfully'
SERIALIZER_RDF_REMOVE_START = 'Removing "{dataset}" dataset from already created RDF file'
SERIALIZER_RDF_REMOVE_FINISHED = '"{dataset}" dataset removal from RDF file process finished successfully'
SERIALIZER_LOAD_TREE = 'Loading tree from {path} XML file'
SERIALIZER_CATALOGUE_SERIALIZE_START = 'Serializing new catalogue for {datamodels} Data Models'
SERIALIZER_CATALOGUE_SERIALIZE_FINISHED = 'Catalogue serialization finished successfully'
SERIALIZER_DATASETS_SERIALIZE_START = 'Serializing catalogue\'s datasets...'
SERIALIZER_DATASETS_SERIALIZE_FINISHED = 'Catalogue\'s datasets serialization process finished successfully'
SERIALIZER_DATASET_SERIALIZE_START = 'Serializing "{datamodel}" Data Model dataset'
SERIALIZER_DATASET_SERIALIZE_FINISHED = 'Dataset serialization finished: "{datamodel}" dataset added to RDF'
SERIALIZER_RESOURCES_SERIALIZE_START = 'Serializing datasets\' distributions...'
SERIALIZER_RESOURCES_SERIALIZE_FINISHED = 'Dataset\'s distributions serialization process finished successfully'
SERIALIZER_RESOURCE_SERIALIZE_START = 'Serializing new distribution'
SERIALIZER_RESOURCE_SERIALIZE_FINISHED = 'Distribution serialization finished successfully'
SERIALIZER_PUBLISHERS_SERIALIZE_START = 'Serializing catalogue\'s publishers...'
SERIALIZER_PUBLISHERS_SERIALIZE_FINISHED = 'Catalogue\'s publishers serialization process finished successfully'
SERIALIZER_PUBLISHER_SERIALIZE_START = 'Serializing new publisher: {name}'
SERIALIZER_PUBLISHER_SERIALIZE_FINISHED = '{name} publisher serialization finished successfully'
SERIALIZER_UPDATE_DATASET_NODE = 'Adding new dataset version for "{datamodel}" Data Model to RDF file'
SERIALIZER_REMOVE_DATASET_NODE = 'Removing "{datamodel}" dataset from RDF file'
SERIALIZER_REMOVE_DATASET_NODE_NOT_PRESENT = 'Dataset not present in RDF file (ignoring removal)'
SERIALIZER_CATALOGUE_DATE_NOT_EXISTS = '<dct:modified> not exists for <dcat:Catalog> (creating with {date})'
SERIALIZER_CATALOGUE_DATE_ALREADY_EXISTS = '<dct:modified> already exists for <dcat:Catalog> (modifying with {date})'
SERIALIZER_PUBLISHER_NODE_APPEARANCES = '<dct:publisher> node appears {times} times'

# /utils/helpers.py
HELPERS_SPATIAL_GEOJSON_NODES = 'There is more than one drawable object (feature) in the GeoJSON provided at {path}. Using only the first one'
HELPERS_SPATIAL_GEOJSON_NOT_FOUND = 'GeoJSON could not be located in {path} file. Is it in JSON file provided? It should be at first place'
HELPERS_SPATIAL_GEOJSON_FILE_NOT_FOUND = 'There was an error trying to access GeoJSON file specified in {path}'
