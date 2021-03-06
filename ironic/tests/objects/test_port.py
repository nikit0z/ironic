# coding=utf-8
#
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock
from testtools.matchers import HasLength

from ironic.common import exception
from ironic import objects
from ironic.tests.db import base
from ironic.tests.db import utils


class TestPortObject(base.DbTestCase):

    def setUp(self):
        super(TestPortObject, self).setUp()
        self.fake_port = utils.get_test_port()

    def test_get_by_id(self):
        port_id = self.fake_port['id']
        with mock.patch.object(self.dbapi, 'get_port_by_id',
                               autospec=True) as mock_get_port:
            mock_get_port.return_value = self.fake_port

            port = objects.Port.get(self.context, port_id)

            mock_get_port.assert_called_once_with(port_id)
            self.assertEqual(self.context, port._context)

    def test_get_by_uuid(self):
        uuid = self.fake_port['uuid']
        with mock.patch.object(self.dbapi, 'get_port_by_uuid',
                               autospec=True) as mock_get_port:
            mock_get_port.return_value = self.fake_port

            port = objects.Port.get(self.context, uuid)

            mock_get_port.assert_called_once_with(uuid)
            self.assertEqual(self.context, port._context)

    def test_get_by_address(self):
        address = self.fake_port['address']
        with mock.patch.object(self.dbapi, 'get_port_by_address',
                               autospec=True) as mock_get_port:
            mock_get_port.return_value = self.fake_port

            port = objects.Port.get(self.context, address)

            mock_get_port.assert_called_once_with(address)
            self.assertEqual(self.context, port._context)

    def test_get_bad_id_and_uuid_and_address(self):
        self.assertRaises(exception.InvalidIdentity,
                          objects.Port.get, self.context, 'not-a-uuid')

    def test_save(self):
        uuid = self.fake_port['uuid']
        with mock.patch.object(self.dbapi, 'get_port_by_uuid',
                               autospec=True) as mock_get_port:
            mock_get_port.return_value = self.fake_port
            with mock.patch.object(self.dbapi, 'update_port',
                                   autospec=True) as mock_update_port:
                p = objects.Port.get_by_uuid(self.context, uuid)
                p.address = "b2:54:00:cf:2d:40"
                p.save()

                mock_get_port.assert_called_once_with(uuid)
                mock_update_port.assert_called_once_with(
                    uuid, {'address': "b2:54:00:cf:2d:40"})
                self.assertEqual(self.context, p._context)

    def test_refresh(self):
        uuid = self.fake_port['uuid']
        returns = [self.fake_port,
                   utils.get_test_port(address="c3:54:00:cf:2d:40")]
        expected = [mock.call(uuid), mock.call(uuid)]
        with mock.patch.object(self.dbapi, 'get_port_by_uuid',
                               side_effect=returns,
                               autospec=True) as mock_get_port:
            p = objects.Port.get_by_uuid(self.context, uuid)
            self.assertEqual("52:54:00:cf:2d:31", p.address)
            p.refresh()
            self.assertEqual("c3:54:00:cf:2d:40", p.address)

            self.assertEqual(expected, mock_get_port.call_args_list)
            self.assertEqual(self.context, p._context)

    def test_list(self):
        with mock.patch.object(self.dbapi, 'get_port_list',
                               autospec=True) as mock_get_list:
            mock_get_list.return_value = [self.fake_port]
            ports = objects.Port.list(self.context)
            self.assertThat(ports, HasLength(1))
            self.assertIsInstance(ports[0], objects.Port)
            self.assertEqual(self.context, ports[0]._context)
