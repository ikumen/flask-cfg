### 0.0.5 (2018-06-18)
* Added two additional methods (on_process_loaded_configs_complete, on_process_loaded_configs_failure) for hooking into processing of loaded config file 
life cycle.

### 0.0.4 (2018-06-15)
* (Breaking change) Removed AbstractConfig.to_object(), allowing user to simply return the AbstractConfig object to Flask's config.from_object(). 

### 0.0.3 (2018-06-14)
* Fixed setup script

### 0.0.1-0.0.2 (2018-06-14)
* Initial release
