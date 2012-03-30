#!/usr/bin/env python
# encoding: utf-8

import util

def get_json_resource(resource_name, **kwargs):
    result = util.callm("%s.json" % resource_name, kwargs)
    return result

def get_listed_things(get_function, attribute, response_key, results, **kwargs):
    if results == -1:
        # hopefully you don't have more followers than this....
        # i'm looking at you wil wheaton
        results = int(1e4)
    things = []
    num_pages = max(results/10, 1)
    for page_num in xrange(num_pages):
        raw = get_function(attribute, page=page_num+1, **kwargs)
        page_things = raw[response_key]
        if not page_things:
            break
        things += page_things
    return things[:results]
        
class GenericProxy(object):
    def __init__(self):
        self.cache = {}

    def get_json_resource(self, *args, **kwargs):
        return get_json_resource(*args, **kwargs)
    
    def _get_listed_things(self, attribute, response_key, results, **kwargs):
        get_function = self.get_json_user_attribute
        return get_listed_things(get_function, attribute, response_key, results, **kwargs)

class UserProxy(GenericProxy):
    def __init__(self, name, **kwargs):
        super(UserProxy, self).__init__()
        self.id = name
        kwargs = util.fix(kwargs)
        core_attrs = [] # things you want/need initted at object creation time

        if not all(core_attr in kwargs for core_attr in core_attrs):
            profile = get_json_resource(self.id)['person']
            kwargs.update(profile)
        
        self.cache.update(kwargs)

    def _get_simple_attribute(self, attribute_name):
        if not attribute_name in self.cache:
            profile = get_json_resource(self.id)['person']
            self.cache.update(profile)
        return self.cache.get(attribute_name)

    def get_json_user_attribute(self, attribute_name, **kwargs):
        meta_resource_name = "%s/%s" % (self.id, attribute_name)
        return get_json_resource(meta_resource_name, **kwargs)
                
class JamProxy(GenericProxy):
    def __init__(self, id, **kwargs):
        super(JamProxy, self).__init__()
        self.id = id
        kwargs = util.fix(kwargs)
        core_attrs = [] # things you want/need initted at object creation time

        if not all(core_attr in kwargs for core_attr in core_attrs):
            profile = get_json_resource("jams/%s" % self.id)['jam']
            kwargs.update(profile)

        self.cache.update(kwargs)

    def _get_simple_attribute(self, attribute_name):
        if not attribute_name in self.cache:
            profile = get_json_resource("jams/%s" % self.id)['jam']
            self.cache.update(profile)
        return self.cache.get(attribute_name)
    
    def get_json_user_attribute(self, attribute_name, **kwargs):
        meta_resource_name = "jams/%s/%s" % (self.id, attribute_name)
        return get_json_resource(meta_resource_name, **kwargs)
