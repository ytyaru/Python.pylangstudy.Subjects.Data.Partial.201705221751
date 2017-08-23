import collections
# ネストしたdictをマージする手段がない

# map.updateだと上書きされる
dict1 = {'breadcrumbs_data': { 'directional_icon_type': 'FontAwesome' }}
dict2 = {'breadcrumbs_data': { 'is_child_first': True }}
dict3 = dict1
dict3.update(dict2)
print(dict3)

# Python3.3以降。連結される
dict1 = {'breadcrumbs_data': { 'directional_icon_type': 'FontAwesome' }}
dict2 = {'breadcrumbs_data': { 'is_child_first': True }}
c = collections.ChainMap(dict1, dict2)
print(c)

# Python3.5以降。上書きされる
# http://qiita.com/kk6/items/6362a5fc9f3f06a5969a
dict4 = {**dict1, **dict2}
print(dict4)


class DeepChainMap(collections.ChainMap):
    def __setitem__(self, key, value):
        for mapping in self.maps:
            if key in mapping:
                mapping[key] = value
                return
        self.maps[0][key] = value

    def __delitem__(self, key):
        for mapping in self.maps:
            if key in mapping:
                del mapping[key]
                return
        raise KeyError(key)

class DeepMargeChainMap(collections.ChainMap):
    def __setitem__(self, key, value):
        self.__RecursionCheck(self.maps, key, value)
        self.maps[0][key] = value
        
    def __RecursionCheck(self, mapping, key, value):
        if isinstance(mapping, (dict, list, tuple)) and isinstance(value, (dict, list, tuple)):
            for map1 in mapping:
                self.__RecursionCheck(map1, key, value)
            for map1 in mapping:
                if key in map1 and isinstance(map1[key], (dict, list, tuple)) and isinstance(value, (dict, list, tuple)):
                    for m_key in map1[key]:
                        self.__RecursionCheck(map1[key], m_key, map1[key][m_key])
                        map1[key].update(value)

    def __delitem__(self, key):
        for mapping in self.maps:
            if key in mapping:
                del mapping[key]
                return
        raise KeyError(key)

"""
class DeepMargeChainMap(collections.ChainMap):
    def __setitem__(self, key, value):
        for mapping in self.maps:
            if key in mapping and isinstance(mapping[key], (dict, list, tuple)) and isinstance(value, (dict, list, tuple)):
                mapping[key].update(value)
                return
        self.maps[0][key] = value

    def __delitem__(self, key):
        for mapping in self.maps:
            if key in mapping:
                del mapping[key]
                return
        raise KeyError(key)
"""


if __name__ == '__main__':
#    dict1 = {'breadcrumbs_data': { 'directional_icon_type': 'FontAwesome' }}
#    dict2 = {'breadcrumbs_data': { 'is_child_first': True }}
#    d = DeepChainMap(dict1, dict2)
#    print(d)

#    d = DeepChainMap()
#    d['breadcrumbs_data'] = { 'directional_icon_type': 'FontAwesome' }
#    d['breadcrumbs_data'] = { 'is_child_first': True }
#    print(d)

    # 1階層ネストしたdictならマージできた
    d = DeepMargeChainMap()
    d['breadcrumbs_data'] = { 'directional_icon_type': 'FontAwesome' }
    d['breadcrumbs_data'] = { 'is_child_first': True }
    print(d)

    # 2階層ネストだと代入になってしまう
    d = DeepMargeChainMap()
    d['breadcrumbs_data'] = {'datas': [{'text': '孫', 'href': 'http://2'}]}
    d['breadcrumbs_data'] = {'datas': [{'text': '子', 'href': 'http://1'}]}
    print(d)

