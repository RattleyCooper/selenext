"""
This is the Middleware super-class.  Its only responsibility is providing
a consistent API for resolving the child classes methods and executing them.
Any model middleware should inherit from the Middleware class.

Example:
    class UserMiddleware(Middleware):

"""
base_model = [
    'DoesNotExist', '__class__', '__delattr__', '__dict__',
    '__doc__', '__eq__', '__format__', '__getattribute__',
    '__hash__', '__init__', '__module__', '__ne__', '__new__',
    '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
    '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
    '_create_indexes', '_data', '_dirty', '_fields_to_index',
    '_get_pk_value', '_meta', '_obj_cache', '_pk_expr',
    '_populate_unsaved_relations', '_prepare_instance',
    '_prune_fields', '_set_pk_value', 'alias', 'as_entity',
    'create', 'create_or_get', 'create_table', 'created_at',
    'delete', 'delete_instance', 'dependencies', 'dirty_fields',
    'drop_table', 'filter', 'get', 'get_id',
    'get_or_create', 'insert', 'insert_from',
    'insert_many', 'is_dirty', 'prepared', 'raw',
    'save', 'select', 'set_id', 'sqlall', 'table_exists',
    'update'
]


class Middleware(object):
    """ The Middleware class enables sub-classes to run Middleware. """

    def _modify_in(self, **kwargs):
        # grab child class which will equal the class that inherited Modifier.
        child_class = self.__class__
        child_class_methods = dir(child_class)

        # print child_class, child_class_methods

        output = {}
        for key, value in kwargs.iteritems():
            # Instantiate the child class and call the key function on value / set output.
            if 'set_' + key in child_class_methods:
                function = getattr(child_class(), 'set_' + key)
                value = function(value)
            output[key] = value
        return output

    def _modify_inputs(self, **kwargs):
        """ Modify the given input **kwargs using the appropriate Middleware. """

        # grab child class which will equal the class that inherited Modifier.
        child_class = self.__class__
        child_class_methods = dir(child_class)

        output = {}
        for key, value in kwargs.iteritems():
            # Instantiate the child class and call the key function on value / set output.
            if 'set_' + key in child_class_methods:
                function = getattr(child_class(), 'set_' + key)
                value = function(value)
            output[key] = value
        return output

    def _modify_dictionary_outputs(self, **kwargs):
        """ Modifies the given output **kwargs using the appropriate Middleware. """

        # Grab child class which will equal the class that inherited Modifier.
        child_class = self.__class__
        child_class_methods = dir(child_class)

        # Generate the output using the appropriate Middleware.
        output = {}
        for key, value in kwargs.iteritems():
            if 'get_' + key in child_class_methods:
                # Grabs the function from `ModelMiddleware`
                method = getattr(child_class(), 'get_' + key)
                # Run the method.
                value = method(value)
            output[key] = value
        return output

    def _modify_function_output(self, function, mod_in=True, mod_out=True, **kwargs):
        # Parse control flow flags.
        try:
            mod_in = kwargs['mod_in']
        except KeyError:
            pass
        try:
            mod_out = kwargs['mod_out']
        except KeyError:
            pass

        secondary_result = None

        # Grab child class which will equal the class that inherited
        # the `Middlware` class(the class we're in now :P).
        child_class = self.__class__
        child_class_methods = dir(child_class)

        # Modify the inputs unless told otherwise.
        if mod_in:
            kwargs = self._modify_inputs(**kwargs)

        # Run the function and then start checking the output
        # to decide how to handle it.
        results = function(**kwargs)

        # Return the results if the mod_out flag isn't set.
        if not mod_out:
            return results

        # Split vars up if results is a tuple, then business as usual.
        if type(results) == tuple:
            if len(results) == 2:
                results, secondary_result = results

        # |-------------- Start handling function output. --------------|

        # Handle models.
        if 'Models.' in str(results):
            model_directory = dir(results)
            data_output = {}
            for model_attribute in model_directory:
                if model_attribute not in base_model:
                    attribute_value = getattr(results, model_attribute)
                    data_output[model_attribute] = attribute_value
            return self._modify_dictionary_outputs(**data_output)

        # Opt out if there is no iterable object after this point.
        else:
            try:
                results = iter(results)
            except TypeError:
                if secondary_result:
                    return results, secondary_result
                return results

        # Handle iterable peewee object...
        data_output = []
        for result_key, result in enumerate(results):
            result_dir = dir(result)
            for value in result_dir:
                if 'get_' + value in child_class_methods:
                    function = getattr(child_class(), 'get_' + value)
                    mod_value = getattr(result, value)
                    # print mod_value
                    mod_value = function(mod_value)
                    # print 'val/modval:', value, mod_value
                    setattr(result, value, mod_value)
                    data_output.append(result)
        if secondary_result:
            return data_output, secondary_result
        return data_output

    def _modify_query_output(self, query):
        # grab child class which will equal the class that inherited Modifier.
        child_class = self.__class__
        child_class_methods = dir(child_class)

        results = query.execute()
        # print 'results:', dir(results)

        data_output = []
        for result_key, result in enumerate(results):
            result_dir = dir(result)
            # print 'result_dir:', result_dir
            for value in result_dir:

                if 'get_' + value in child_class_methods:
                    function = getattr(child_class(), 'get_' + value)
                    mod_value = getattr(result, value)
                    # print mod_value
                    mod_value = function(mod_value)
                    # print 'val/modval:', value, mod_value
                    setattr(result, value, mod_value)
                    data_output.append(result)
        return data_output
