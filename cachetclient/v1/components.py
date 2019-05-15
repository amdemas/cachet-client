from typing import Generator, List

from cachetclient.base import Manager, Resource
from cachetclient.v1 import enums


class Component(Resource):

    @property
    def id(self) -> int:
        return self._data['id']

    @property
    def name(self) -> str:
        return self._data['name']

    @name.setter
    def name(self, value):
        self._data['name'] = value

    @property
    def description(self) -> str:
        return self._data['description']

    @property
    def link(self) -> str:
        return self._data['link']

    @property
    def status(self) -> int:
        return self._data['status']

    @property
    def status_name(self) -> str:
        return self._data['status_name']

    @property
    def order(self) -> int:
        return self._data['order']

    @property
    def group_id(self):
        return self._data['group_id']

    @property
    def created_at(self):
        return self._data['created_at']

    @property
    def updated_at(self):
        return self._data['updated_at']

    @property
    def deleted_at(self):
        return self._data['deleted_at']


class ComponentManager(Manager):
    resource_class = Component
    path = 'components'

    def create(
            self,
            name,
            status,
            description: str = None,
            link: str = None,
            order: int = None,
            group_id: int = None,
            enabled: bool = True,
            tags: List[str] = None):
        """
        Create a component.

        Args:
            name (str): Name of the component
            status (int): Status if of the component (see enums module)

        Keyword Args:
            description (str): Description of the component (required)
            link (str): Link to the component
            order (int): Order of the component in its group
            group_id (int): The group it belongs to
            enabled (bool): Enabled status
            tags (list): String tags

        Returns:
            :py:class:`Component` instance
        """
        if not name:
            raise ValueError("Name empty or None: {}".format(name))

        if status not in enums.COMPONENT_STATUS_LIST:
            raise ValueError("Invalid status id '{}'. Valid values :{}".format(
                status,
                enums.COMPONENT_STATUS_LIST,
            ))

        return self._create(
            self.path,
            {
                'name': name,
                'description': description,
                'status': status,
                'link': link,
                'order': order,
                'group_id': group_id,
                'enabled': enabled,
                'tags': tags,
            }
        )

    def update(
            self,
            component_id,
            name=None,
            description=None,
            status=None,
            tags=None,
            **kwargs):

        return self._update(
            self.path,
            component_id,
            {
                'name': name,
                'description': description,
                'status': status,
                'tags': tags,
            }
        )

    def list(self, page: int = 1, per_page: int = 20) -> Generator[Component, None, None]:
        """
        List all components

        Keyword Args:
            page (int): The page to start listing
            per_page: Number of entires per page

        Returns:
            Generator with Component instances
        """
        yield from self._list_paginated(self.path, page=page, per_page=per_page)

    def get(self, component_id: int) -> Component:
        """
        Get a component by id

        Params:
            component_id (int): Id of the component

        Returns:
            Component instance

        Raises:
            HttpError if not found
        """
        return self._get(self.path, component_id)

    def delete(self, component_id: int) -> None:
        """
        Delete a component

        Params:
            component_id (int): Id of the component

        Raises:
            HTTPError if compontent do not exist
        """
        self._delete(self.path, component_id)

    def count(self) -> int:
        """
        Count the number of components

        Returns:
            (int) Total number of components
        """
        return self._count(self.path)
