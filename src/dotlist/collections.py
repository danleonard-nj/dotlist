from functools import wraps
from collections.abc import Iterable
from enum import Enum
from typing import Union, NewType, Callable


def update(func):
    @wraps(func)
    def wrap(self, *args, **kwargs):
        func(self, *args, **kwargs)
        self._update_attributes()
    return wrap


class DotListException(Exception):
    def __init__(self, message):
        super().__init__(self, message=message)


class JoinType(Enum):
    Left = 'left',
    Inner = 'right'


join_types = NewType('JoinType', JoinType)


class dotlist:
    def __init__(self, _list=None):
        self._collection = list()

        if _list is not None:
            self._collection = _list

    def __repr__(self):
        items = ', '.join(
            [x.__repr__() for x in self._collection]
        )
        return f'dl~ [{items}]'

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, accessor):
        try:
            return self._collection[accessor]
        except:
            pass

    def __setitem__(self, accessor, value):
        try:
            self._collection[accessor] = value
        except:
            pass

    def __iter__(self):
        return iter(self._collection)

    def _is_iterable(self, obj):
        return isinstance(obj, list) or isinstance(
            obj, set) or isinstance(obj, tuple)

    def _update_attributes(self):
        _attributes = {
            'count': len(self._collection)
        }
        self.__dict__.update(_attributes)

    def to_list(self):
        return self._collection

    @update
    def add(self, obj: Union[Iterable, object]) -> None:
        '''
        Adds a single item or an iterable to the collection.  This
        method updates the properties of the collection

        Parameters:
            obj: an item or iterable
        '''

        if isinstance(obj, dotlist):
            self.add(obj._collection)
        elif self._is_iterable(obj):
            for element in obj:
                self._collection.append(element)
        else:
            self._collection.append(obj)

    @update
    def remove(self, obj: Union[Iterable, object]) -> None:
        '''
        Removes a single item or an iterable from the collection.  This
        method updates the properties of the collection

        Parameters:
            obj: an item or iterable
        '''

        if self._is_iterable(obj):
            for element in obj:
                if self.has(element):
                    self._collection.remove(element)
        else:
            if self.has(obj):
                self._collection.remove(obj)

    def distinct(self) -> 'dotlist':
        '''
        Gets the distinct elements of the collection

        Returns:
            iterable (dotlist): the distinct elements
            in the collection
        '''

        _distinct = list(set(self._collection))
        return dotlist(_distinct)

    def count_distinct(self) -> int:
        '''
        Gets the count of distinct elements of the collection

        Returns:
            count (int): the count of distinct elements in
            the collection
        '''

        return len(self.distinct())

    def intersection(self, compare: Iterable) -> 'dotlist':
        '''
        Gets the mutual elements of the current collection and a
        provided iterable

        Example:
            collection:
                dl~ ['howdy', 'there', 'world]
            compare:
                ['howdy', 'world']
            result
                dl~ ['howdy', 'world']

        Parameters:
            compare (iterable): the iterable to compare

        Returns:
            elements (dotlist): the collection of mutual items
        '''

        elements = dotlist()
        for element in compare:
            if self.has(element):
                elements.add(element)
        return elements

    def difference(self, compare: Iterable) -> 'dotlist':
        '''
        Gets the different between the the current collection and a
        provided iterable

        Example:
            colleciton:
                dl~ ['howdy', 'there', 'world']
            compare:
                ['howdy', 'world]
            result:
                dl~ ['there]

        Parameters:
            compare (iterable): the iterable to compare

        Returns:
            elements (dotlist): the collection of differences
        '''

        elements = dotlist()
        for element in compare:
            if not self.has(element):
                elements.add(element)
        return elements

    def reverse(self) -> None:
        '''
        Reverse the collection in place.
        '''

        self._collection.reverse()

    def at(self, index: int) -> Union[object, None]:
        '''
        Gets the element at the given index, or None if the
        element does not exist

        Parameters:
            index (int): index of element

        Returns:
            element (object): the element at specified index
            or None
        '''

        try:
            return self._collection[index]
        except:
            return None

    def has(self, obj: Union[Iterable, object]) -> bool:
        '''
        Checks if an element or iterable exists in the collection

        Parameters:
            obj (object): the element or iterable to look up

        Returns:
            exists (bool): True if the element or iterable exists
            in the collection
        '''

        if self._is_iterable(obj):
            for element in obj:
                if element not in self._collection:
                    return False
            return True
        else:
            return obj in self._collection

    def nas(self, obj: Union[Iterable, object]) -> bool:
        '''
        Checks if an element or iterable does not exist in the
        collection

        Parameters:
            obj (object): the element or iterable to look up

        Returns:
            exists (bool): True if the element or iterable does
            not exist in the collection
        '''

        return not self.has(obj)

    def range(self, start: int, end: int) -> Union['dotlist', None]:
        '''
        Gets a subset of the collection at the given index range
        or None if the range doesn't exist

        Parameters:
            start (int): the start index
            end (int): the end index

        Returns:
            exists (bool): True if the element or iterable does
            not exist in the collection
        '''

        return self[start: end]

    def enumerate(self) -> 'dotlist':
        '''
        Gets the enumerated collection

        Example:
            collection:
                dl~ ['hello', 'world']
            result: [(0, 'hello'), (1, 'world')]

        Returns:
            result (dotlist): The enumerated collection
        '''

        enumerated = self._collection(
            _list=list(
                enumerate(self._collection)
            )
        )

        return dotlist(enumerated)

    def index(self, obj: object) -> int:
        '''
        Gets the index of the given element

        Parameters:
            obj (object): element to look up

        Returns:
            index (int): the index of the given
            element
        '''

        for element in self.enumerate():
            if element[1] == obj:
                return element[0]
        return None

    def find(self, element: object) -> int:
        '''
        Gets the index of the given element

        Parameters:
            obj (object): element to look up

        Returns:
            index (int): the index of the given
            element
        '''

        for index in range(len(self._collection)):
            if self._collection[index] == element:
                return index
        return None

    @update
    def insert(self, obj: object, index: int = None) -> None:
        '''
        Insert an element into the colleciton, optionally
        at a given index

        Parameters:
            obj (object): element to insert
            [optional] index (int): the postion in the collection
            to insert the element
        '''

        if index is None:
            self._collection.append(obj)
        else:
            self._collection.insert(
                index, obj)

    def clone(self) -> 'dotlist':
        '''
        Gets a deep clone of the collection

        Returns:
            clone (dotlist): clone of the collection
        '''

        return [x for x in self._collection]

    def sort(self, desc: bool = False) -> None:
        '''
        Sorts the collection in place

        Parameters:
            desc (bool): sort descending
        '''

        self._collection.sort(reverse=desc)

    def apply(self, func: Callable, enum: bool = False) -> None:
        '''
        Apply a function to the collection in place, optionally
        project an enumerated collection into the func

        Enumerated example:
            val: dl~ ['hello', 'world']
            out: dl~ [(0, 'hello'), (1, 'world')] => lambda i, v

        Parameters:
            [required] func (function): function to apply
            [optional] enum (bool): optionally project an enumerated
            collection to func
        '''

        if enum:
            for index in range(len(self._collection)):
                self._collection[index] = func(
                    self._collection[index], index
                )
        else:
            for index in range(len(self._collection)):
                self._collection[index] = func(
                    self._collection[index]
                )

    # def project(self, func):
    #     for item in self._collection:
    #         func(item)

    def shave_first(self) -> None:
        '''
        Shave the first value off the collection in place
        '''

        self._collection = self._collection[1:]

    def shave_last(self):
        '''
        Shave the last value off the collection in place
        '''
        self._collection = self._collection[:-1]

    def first_or_none(self) -> object:
        '''
        Return the first element in the collection, or None
        if the element doesn't exist

        Returns:
            element (object): the first element in the colleciton
            or None
        '''

        return self.at(0)

    def last_or_none(self):
        '''
        Return the last element in the collection, or None
        if the element doesn't exist

        Returns:
            element (object): the last element in the colleciton
            or None
        '''

        return self.at(self.count - 1)

    def where(self, func: Callable) -> 'dotlist':
        '''
        Return a subset of the collection where value returned by
        func is true.  This does not mutate the collection.

        example:
            collection = dl~ ['hello', 'world']

        function:
            collection.where(lambda x: x == 'hello')

        returns:
            dl~ ['hello']

        Parameters:
            func (function): the condition to evaluate over the
            collection

        Returns:
            result (object): the subset of the collection
            where func is True
        '''

        elements = list()
        for item in self._collection:
            if func(item):
                elements.append(item)
        return dotlist(elements)

    def select(self, func: Callable) -> 'dotlist':
        '''
        Return a collection of the results of the supplied function
        over the original collection.  This does not mutate the collection

        example:
            collection = dl~ ['hello', 'world']

        function:
            collection.select(lambda x: x.upper())

        returns:
            dl~ ['HELLO', 'WORLD']

        Parameters:
            func (function): the function to evaluate over the
            collection

        Returns:
            result (object): the evaluated collection
        '''

        elements = list()
        for item in self._collection:
            elements.append(func(item))
        return dotlist(elements)

    def select_many(self, func: Callable) -> 'dotlist':
        '''
        Select over a collection of iterables

        example:
            collection = dl~ [['hello', 'world'], ['another', 'message']]

        function:
            collection.select(lambda x: x.upper())

        returns:
            dl~ ['HELLO', 'WORLD', 'ANOTHER', 'MESSAGE']

        Parameters:
            func (function): the function to evaluate over the
            collection of iterables

        Returns:
            result (object): the evaluated collection
        '''

        elements = list()
        for item in self._collection:
            for sub in item:
                elements.append(func(sub))
        return dotlist(elements)

    def take(self, start: int, count: int) -> 'dotlist':
        '''
        Return a subset of the collection of a given length, starting at
        the given index position

        Parameters:
            start (int): starting index location
            count (int): number of elements to fetch after the starting
            position

        Returns:
            result (object): the evaluated collection
        '''

        return self.range(
            start, start + count)

    def take_while(self, func: Callable) -> 'dotlist':
        '''
        Iterate over collection and evaluate each element by given func
        and return all elements that evaluate True, up to the first element
        that evaluates False

        Example:
            collection:
                ~dl [1, 2, 3, 1, 2, 3]
            example:
                collection.take_while(lambda x: x < 3)
            returns:
                ~dl [1, 2]

        Parameters:
            func (function): the function to evaluate over the collection

        Returns:
            result (dotlist): the evaluated collection
        '''

        elements = dotlist()
        for item in self._collection:
            if func(item):
                elements.add(item)
            else:
                break
        return elements

    def union(self, obj: Iterable) -> None:
        '''
        Union current collection with a given iterable in place

        Parameters:
            obj (object): iterable to union
        '''

        self.add(obj)

    def join(self, data: dict, how: JoinType = JoinType.Inner) -> dict:
        '''
        Join a dict-like object on the collection by key
        See basic SQL joins for descriptions of JoinTypes

        Example:
            collection:
                dl~ ['name', 'favorite_color']
            data:
                {'name': 'dan', 'favorite_color': 'black', car: 'toyota'}
            returns:
                {'name': 'dan', 'favorite_color': 'black'}

        Parameters:
            data (dict): dict-like object tojoin on collection
            how (JoinType): the type of join to perform 

        Results:
            result (dict): the provided data joined on the collection
            by key
        '''

        if how == JoinType.Inner:
            return self.join_inner(data)
        if how == JoinType.Left:
            return self.join_left(data)
        else:
            raise DotListException(
                message='Join type is not of valid types Inner, Left')

    def join_inner(self, data: dict) -> dict:
        '''
        Inner join a dict-like object on the collection by key. See 
        basic SQL joins for descriptions of JoinTypes

        Example:
            collection:
                dl~ ['name', 'favorite_color', 'favorite_food']
            data:
                {'name': 'dan', 'favorite_color'}
            returns:
                {'name': 'dan', 'favorite_color': 'black'}

        Parameters:
            data (dict): dict-like object tojoin on collection

        Results:
            result (dict): the provided data joined on the collection
            by key
        '''

        result = dict()
        for item in self._collection:
            value = data.get(item)
            if value:
                result.update({
                    item: value
                })
        return result

    def join_left(self, data: dict) -> dict:
        '''
        Left join a dict-like object on the collection by key. See 
        basic SQL joins for descriptions of JoinTypes

        Example:
            collection:
                dl~ ['name', 'favorite_color', 'favorite_food']
            data:
                {'name': 'dan', 'favorite_color'}
            returns:
                {'name': 'dan', 'favorite_color': 'black', 'favorite_food': None}

        Parameters:
            data (dict): dict-like object tojoin on collection

        Result:
            result (dict): the provided data joined on the collection
            by key
        '''

        result = dict()
        for item in self._collection:
            result.update({
                item: data.get(item)
            })
        return result

    def zip(self, obj: Iterable) -> 'dotlist':
        '''
        Zip an iterable over the collection

        Example:
            collection:
                dl~ ['apple', 'banana', 'grape']
            obj:
                ['red', 'yellow', 'green']
            returns:
                [('apple', 'red'), ('banana', 'yellow'), ('grape', 'green')]

        Parameters:
            obj (Iterable): the iterable to zip over collection
        '''

        elements = dotlist()
        for index in range(len(self._collections)):
            elements.add(
                (self._collection[index],
                 obj[index])
            )
        return elements

    def any(self, func: Callable) -> bool:
        '''
        Evaluate if any of the elements in collection return True when evaluated by
        given func

        Parameters:
            func (function): function to evaluate over collection

        Example:
            collection:
                dl~ ['howdy', 'world']
            func:
                collection.any(lambda x: x == 'howdy')
            returns:
                True

        Returns:
            result (bool): True if any of the elements in the collection return True when
            evaluated by the given function
        '''

        for item in self._collection:
            if func(item):
                return True
        return False

    def all(self, func: Callable) -> bool:
        '''
        Evaluate if all of the elements in collection return True when evaluated by
        given func

        Parameters:
            func (function): function to evaluate over collection

        Example:
            collection:
                dl~ ['howdy', 'world']
            func:
                collection.any(lambda x: len(x) == 5)
            returns:
                True

        Returns:
            result (bool): True if all of the elements in the collection return True 
            when evaluated by the given function
        '''

        for item in self._collection:
            if not func(item):
                return False
        return True

    def skip(self, func: Callable) -> 'dotlist':
        '''
        Return a subset of a collection excluding elements that return True when evaluated by
        the given func

        Parameters:
            func (function): function to evaluate over collection

        Example:
            collection:
                dl~ ['howdy', 'there', 'world']
            func:
                collection.skip(lambda x: x == 'there')
            returns:
                dl~ ['howdy', 'world']

        Returns:
            collection (dotlist): the subset of the collection excluding elements that return
            True when evaluated by the given func
        '''

        elements = dotlist()
        for item in self._collection:
            if not func(item):
                elements.add(item)
        return elements

    def is_numeric(self) -> bool:
        '''
        Is the collection composed of only numeric (int or float) types

        Returns:
            numeric (bool): is the collection numeric
        '''

        return self.all(lambda x: isinstance(x, int)
                        or isinstance(x, float))

    def average(self) -> Union[int, float, None]:
        '''
        Average of all numeric values in the collection, or None if the
        collection is not numeric

        Returns:
            average (int, float): is the collection numeric
        '''

        if not self.is_numeric() and len(self._collection > 0):
            return None
        else:
            return sum(self._collection) / len(self._collection)

    def sum(self) -> Union[int, float, None]:
        '''
        Returns the sum of values in the collection if the 
        collection is numeric

        Returns:
            sum (int, float, None): the sum of the numeric 
            values in the collection
        '''

        if self.is_numeric():
            return sum(self._collection)
        else:
            return None

    def max(self) -> Union[int, float, None]:
        '''
        Returns the maximum value if the collection is numeric

        Returns:
            max (int, float, None): the maximum numeric value 
            in the collection
        '''

        if self.is_numeric():
            return max(self._collection)
        else:
            return None

    def min(self) -> Union[int, float, None]:
        '''
        Returns the minimum numeric value if the collection 
        is numeric

        Returns:
            min (int, float, None): the minimum numeric value 
            in the collection
        '''

        if self.is_numeric():
            return min(self._collection)
        else:
            return None

    def group_by(self, func):
        '''
        TODO: Groupby function
        '''
        pass

    def to_dictionary(self, key_func: Callable, value_func: Callable) -> dict:
        '''
        Map the collection to a dictionary using the provided key
        and value funcs

        Parameters:
            key_func (function): function to project the dictionary key
            value_func (function): function to project the dictionary value

        Example:
            colleciton:
                dl~ ['howdy', 'there', 'world']
            to_dictionary:
                dl.to_dictionary(lambda x: x, lambda y: len(y))
            returns:
                {'howdy': 5, 'there': 5, 'world': 5}

        Returns:
            result (dict): generated dictionary
        '''

        _dict = dict()
        for item in self._collection:
            _dict.update({
                key_func(item): value_func(item)
            })
        return _dict
