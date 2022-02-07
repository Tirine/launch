# Copyright 2018 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the SimpleLaunchArgument action class."""

from launch import LaunchContext
from launch.descriptions import SimpleLaunchArgument

import pytest


def test_declare_launch_argument_constructors():
    """Test the constructors for SimpleLaunchArgument class."""
    SimpleLaunchArgument('name').declaration
    SimpleLaunchArgument('name', default_value='default value').declaration
    SimpleLaunchArgument('name', default_value='default value', 
                          description='description').declaration
    SimpleLaunchArgument('name', default_value='val1', description='description',
                          choices=['val1', 'val2']).declaration


def test_declare_launch_argument_methods():
    """Test the methods of the SimpleLaunchArgument class."""
    dla1 = SimpleLaunchArgument('name', default_value='default value', description='description').declaration
    assert dla1.name == 'name'
    assert isinstance(dla1.default_value, list)
    assert dla1.description == 'description'
    assert dla1.choices is None
    assert 'DeclareLaunchArgument' in dla1.describe()
    assert isinstance(dla1.describe_sub_entities(), list)
    assert isinstance(dla1.describe_conditional_sub_entities(), list)

    dla2 = SimpleLaunchArgument('name').declaration
    assert dla2.default_value is None
    assert dla2.choices is None
    assert dla2.description, 'description does not have a non-empty default value'

    dla3 = SimpleLaunchArgument('name', description='description', choices=['var1', 'var2']).declaration
    assert dla3.default_value is None
    assert dla3.choices == ['var1', 'var2']
    assert str(dla3.choices) in dla3.description

    with pytest.raises(RuntimeError) as excinfo:
        SimpleLaunchArgument('name', description='description', choices=['var1', 'var2'],
                              default_value='invalid').declaration
    assert 'not in provided choices' in str(excinfo.value)


def test_declare_launch_argument_execute():
    """Test the execute (or visit) of the SimpleLaunchArgument class."""
    action1 = SimpleLaunchArgument('name').declaration
    lc1 = LaunchContext()
    with pytest.raises(RuntimeError) as excinfo:
        action1.visit(lc1)
    assert 'Required launch argument' in str(excinfo.value)

    lc1.launch_configurations['name'] = 'value'
    assert action1.visit(lc1) is None

    action2 = SimpleLaunchArgument('name', default_value='value').declaration
    lc2 = LaunchContext()
    assert action2.visit(lc2) is None
    assert lc1.launch_configurations['name'] == 'value'

    action3 = SimpleLaunchArgument('name', default_value='var1', choices=['var1', 'var2']).declaration
    lc3 = LaunchContext()
    assert action3.visit(lc3) is None
    lc3.launch_configurations['name'] = 'invalid_value'
    with pytest.raises(RuntimeError) as excinfo:
        action3.visit(lc3)
        assert 'Valid options are: [var1, var2]' in str(excinfo.value)
    lc3.launch_configurations['name'] = 'var1'
    assert action3.visit(lc3) is None
    lc3.launch_configurations['name'] = 'var2'
    assert action3.visit(lc3) is None
