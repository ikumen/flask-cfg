import logging
import os
import yaml

from abc import ABCMeta, abstractmethod

def hello():
    print('hello')

class AbstractConfig(object):
    """Configuration object that attempts to load config values from 
    YAML files. Implementing classes can optionally try to resolve any 
    missing values (useful in certain environments).
    """
    def __init__(self,
                default_conf_paths='default.yaml',
                override_conf_paths=None,
                secret_conf_paths=None,
                ignore_errors=True):
        """Load config values for each of the given file paths. If a duplicate
        value is loaded (e.g value was loaded in a preceeding config file), it
        is merge or replaced with the latter value taking precedence.
        
        @param default_conf_paths file path(s) that will provide default config values
        @param override_conf_paths file path(s) that will provide config values overriding 
                                values from default_conf_paths. This is a good place to 
                                put environment specific config values.
        @param secret_conf_paths file path(s) that will provide config values overriding
                                override_conf_paths and default_conf_paths. This is a good
                                place to put secret settings (make sure to keep out of 
                                source control).
        @param ignore_errors file path and missing values should be ignored if True
        """
        self.ignore_errors = ignore_errors
        self.config_values = {}

        # Normalize all file paths to a single array.
        # Note: order is important as latter configs will override earlier.
        config_paths = self._normalize_file_paths(
            default_conf_paths,
            override_conf_paths,
            secret_conf_paths)

        # Load the config values, then resolve any missing values
        self.config_values = self.resolve_missing_values(self._load_all_configs(config_paths, {}))

    def resolve_missing_values(self, values):
        """Resolve any missing config values.

        @param values dictionary of config values
        """
        unresolved = self._resolve([], values)
        if len(unresolved) > 0:
            logging.warn("""
                \n---------------------------
                \nMissing values for:
                \n{}
                \n---------------------------
                """.format(unresolved))
            if not self.ignore_errors:
                raise LookupError("Unresolved values: {}".format(unresolved))
        return values

    
    def _resolve(self, dict_path, values, unresolved=[]):
        """Attempts to resolve any config value that is missing (e.g. None).

        @param dict_path our current path as we traverse the values dict
        @param values dictionary containing configs we want to resolve
        @param unresolved keep track of config values that are missing
        @returns list containing all unresolved configs
        """
        if isinstance(values, dict):
            for k, v in values.items():
                if not k.isupper():
                    del values[k]
                    # Flask only supports config values that are uppercase.
                    # see: http://flask.pocoo.org/docs/1.0/config/#configuring-from-files
                    continue
                dict_path.append(''.join(['_', k])) # track our dict traversal
                # Found a missing value, try to resolve
                if v is None:
                    path = (''.join(dict_path))[1:]
                    resolved_value = self.handle_missing_value(k, values, path)
                    if resolved_value is None:
                        unresolved.append(path)
                    else:
                        values[k] = resolved_value
                # is config has value, and it's another dict, traverse it
                elif hasattr(v, '__iter__'):
                    self._resolve(dict_path, v, unresolved)
                # again, update where we are in dict traversal
                dict_path.pop()
        elif isinstance(values, list):
            for _ in values:
                self._resolve(dict_path, _, unresolved)
        return unresolved

    @abstractmethod
    def handle_missing_value(self, k, values, dict_path):
        """Actual method where we handle missing value.
        
        @param k key of missing value
        @param values dictionary that contains missing value
        @param dict_path that path we used to get to this values dictionary
        @returns resolved value
        """
        pass


    def _load_all_configs(self, paths, values={}):
        """Loads configuration values for each of the files (from given paths), merging
        duplicate values (e.g. latter values with same keys override earlier values).
        
        @param paths list of config file paths to load
        @param values dictionary to store the loaded values
        """
        if not isinstance(values, dict):
            raise TypeError('values must be a dictionary!')
        for p in paths:
            # delegate load of actual config values, then merge with any existing values
            self._merge_values(values, self._load_config(p))
        return values


    def _merge_values(self, to_values, from_values):
        """Merges two dictionaries of values recursively. This is a very naive
        implementation that expects the two dictionaries to be fairly similar 
        in structure.

        @param to_values destination dictionary
        @param from_values dictionary with values to copy
        """
        if from_values is not None:
            for k, v in from_values.items():
                if k in to_values and isinstance(to_values[k], dict):
                    self._merge_values(to_values[k], v) # merge
                else:
                    to_values[k] = v # replaces instead of merge
        return to_values
                
    
    def _load_config(self, path):
        """Return YAML values from given config file.

        @param path file to load
        """
        try:
            with open(path) as f:
                values = yaml.safe_load(f)
                if isinstance(values, dict):
                    return values
                else:
                    raise yaml.YAMLError('Unable to parse/load {}'.format(path))
        except(IOError, yaml.YAMLError) as e:
            if self.ignore_errors:
                return None
            else:
                raise e


    def _normalize_file_paths(self, *args):
        """Returns all given configuration file paths as one list."""
        paths = []
        for arg in args:
            if arg is None:
                continue
            elif self._is_valid_file(arg):
                paths.append(arg)
            elif isinstance(arg, list) and all(self._is_valid_file(_) for _ in arg):
                paths = paths + arg
            elif not self.ignore_errors:
                raise TypeError('Config file paths must be string path or list of paths!')
        return paths


    def _is_valid_file(self, path):
        """Simple check to see if file path exists. Does not check for valid YAML format."""
        return isinstance(path, basestring) and os.path.isfile(path)

    def to_object(self):
        """Return config values as a simple object that Flask can understand."""
        return self._Config(**self.config_values)

    class _Config(object):
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)


class SimpleConfig(AbstractConfig):
    def __init__(self, **kwargs):
        super(SimpleConfig, self).__init__(**kwargs)

    """Config implementation that does NOT try to resolve any missing values
    and simply ignores them."""
    def handle_missing_value(self, k, values, dict_path):
        return None