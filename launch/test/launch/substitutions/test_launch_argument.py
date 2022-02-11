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

"""Tests for the LaunchArgument action class."""

from launch import LaunchContext
from launch.descriptions import LaunchArgument

import pytest


def test_launch_argument_constructors():
    """Test the constructors for LaunchArgument class."""
    LaunchArgument('name')
    LaunchArgument('name', default_value='default value')
    LaunchArgument('name', default_value='default value',
                   description='description')
    LaunchArgument('name', default_value='val1', description='description',
                   choices=['val1', 'val2'])
    with pytest.raises(TypeError) as excinfo:
        LaunchArgument()
    assert "required positional argument: 'name'" in str(excinfo.value)


def test_launch_config_methods():
    """Test the methods of the LaunchArgument class."""
    mock_context = LaunchContext()
    mock_context.launch_configurations['name'] = 'test'
    launch_arg = LaunchArgument(
        'name', default_value='default value', description='description')
    assert launch_arg.perform(LaunchContext()) == 'default value'
    assert launch_arg.perform(mock_context) == 'test'
    assert launch_arg.variable_name[0].describe() == "'name'"


def test_declare_launch_argument_methods():
    """Test the methods of the LaunchArgument class."""
    launch_arg1 = LaunchArgument(
        'name', default_value='default value', description='description')
    assert launch_arg1.name == 'name'
    assert isinstance(launch_arg1.default_value, list)
    assert launch_arg1.description == 'description'
    assert launch_arg1.choices is None
    assert 'LaunchArgument(name)' == launch_arg1.describe()
    assert isinstance(launch_arg1.describe_sub_entities(), list)
    assert isinstance(launch_arg1.describe_conditional_sub_entities(), list)

    launch_arg2 = LaunchArgument('name')
    assert launch_arg2.default_value is None
    assert launch_arg2.choices is None
    assert launch_arg2.description, 'description does not have a non-empty default value'

    launch_arg3 = LaunchArgument(
        'name', description='description', choices=['var1', 'var2'])
    assert launch_arg3.default_value is None
    assert launch_arg3.choices == ['var1', 'var2']
    assert str(launch_arg3.choices) in launch_arg3.description

    with pytest.raises(RuntimeError) as excinfo:
        LaunchArgument('name', description='description', choices=['var1', 'var2'],
                       default_value='invalid')
    assert 'not in provided choices' in str(excinfo.value)


def test_declare_launch_argument_execute():
    """Test the execute (or visit) of the LaunchArgument class."""
    action1 = LaunchArgument('name')
    lc1 = LaunchContext()
    with pytest.raises(RuntimeError) as excinfo:
        action1.visit(lc1)
    assert 'Required launch argument' in str(excinfo.value)

    lc1.launch_configurations['name'] = 'value'
    assert action1.visit(lc1) is None

    action2 = LaunchArgument('name', default_value='value')
    lc2 = LaunchContext()
    assert action2.visit(lc2) is None
    assert lc1.launch_configurations['name'] == 'value'

    action3 = LaunchArgument(
        'name', default_value='var1', choices=['var1', 'var2'])
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
