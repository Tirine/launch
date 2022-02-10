# Copyright 2019 Open Source Robotics Foundation, Inc.
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

"""Tests for the JoinSubstitutions substitution class."""

from launch.substitutions import JoinSubstitutions, SubstitutionFailure
from launch.actions import DeclareLaunchArgument
from launch.launch_description import LaunchContext, LaunchDescription

import pytest


def test_empty_join_object():
    sub = JoinSubstitutions()
    assert sub.perform(None) == ""


def test_join_one_text_object():
    text = "Test"
    sub = JoinSubstitutions(text)
    assert sub.perform(None) == text


def test_join_faulty_object():
    text = "Test"
    faulty_subs = [
        SubstitutionFailure(text),
        DeclareLaunchArgument(text),
        LaunchContext(),
        LaunchDescription(),
    ]
    for sub in faulty_subs:
        for i in range(10):
            with pytest.raises(SubstitutionFailure):
                JoinSubstitutions(sub)
            sub = [text, sub]


def test_join_multiple_text_object():
    text = "Test"
    text_list = [text]
    result_text = text
    for i in range(10):
        sub = JoinSubstitutions(text_list)
        assert sub.perform(None) == result_text
        sub.extend(text_list)
        for add_text in text_list:
            result_text += add_text
        text_list += text_list


def test_join_text_object_with_join_symbol():
    text = "Test"
    join_symbol = " + "
    sub = JoinSubstitutions([text, text, text], join_symbol)
    assert sub.perform(None) == text + join_symbol + text + join_symbol + text
    assert sub.join_symbol == join_symbol


def test_join_text_object_and_change_join_symbol():
    text = "Test"
    join_symbol = " + "
    sub = JoinSubstitutions([text, text, text], join_symbol)
    assert sub.perform(None) == text + join_symbol + text + join_symbol + text
    join_symbol = "_-_"
    sub.set_join_symbol(join_symbol)
    assert sub.perform(None) == text + join_symbol + text + join_symbol + text


def test_join_multiple_text_and_list_object():
    text = "Test"
    join_symbol = " + "
    sub = JoinSubstitutions([text, [text, text], text], join_symbol)
    assert sub.perform(None) == text + join_symbol + text + text + join_symbol + text


def test_add_join():
    text = "Test"
    join_symbol = " + "
    sub = JoinSubstitutions(text, join_symbol)
    sub = sub + text
    text = text + join_symbol + text
    assert sub.perform(None) == text


def test_radd_join():
    text = "Test"
    join_symbol = " + "
    sub = JoinSubstitutions(text, join_symbol)
    sub = text + sub
    text = text + join_symbol + text
    assert sub.perform(None) == text


def test_iadd_join():
    text = "Test"
    join_symbol = " + "
    sub = JoinSubstitutions(text, join_symbol)
    sub += sub
    text += join_symbol + text
    assert sub.perform(None) == text


def test_mul_join():
    text = "Test"
    join_symbol = " + "
    sub = JoinSubstitutions(text, join_symbol)
    sub = sub*2
    text = text + join_symbol + text
    assert sub.perform(None) == text


def test_imul_join():
    text = "Test"
    join_symbol = " + "
    sub = JoinSubstitutions(text, join_symbol)
    sub *= 2
    text = text + join_symbol + text
    assert sub.perform(None) == text


def test_rmul_join():
    text = "Test"
    join_symbol = " + "
    sub = JoinSubstitutions(text, join_symbol)
    sub = 3*sub
    text = text + join_symbol + text + join_symbol + text
    assert sub.perform(None) == text


def test_identity():
    text = "Test"
    join_symbol = " + "
    sub1 = JoinSubstitutions([text, text])
    sub2 = sub1
    assert sub1 is sub2
    sub2 += ""
    assert sub1 is not sub2
    sub1 = JoinSubstitutions([text, text], join_symbol)
    sub2 = JoinSubstitutions([text, text], join_symbol)
    assert sub1 is not sub2
    sub2 = JoinSubstitutions([text, text])
    assert sub1 is not sub2
    sub2 = JoinSubstitutions(text + join_symbol, join_symbol)
    assert sub1 is not sub2
    sub2 = JoinSubstitutions(text + join_symbol + text, join_symbol)
    assert sub1 is not sub2


def test_equality():
    text = "Test"
    join_symbol = " + "
    sub1 = JoinSubstitutions([text, text])
    sub2 = sub1
    assert sub1 == sub2
    sub2 = JoinSubstitutions([text, text])
    assert sub1 == sub2
    sub2 += ""
    assert sub1 != sub2
    sub2 = JoinSubstitutions([text, text], join_symbol)
    assert sub1 != sub2
    sub2 = JoinSubstitutions(text + join_symbol, join_symbol)
    assert sub1 != sub2
    # Would be nice to be able to evaluate these equal,
    # but for that a preform is needed or simplification of TextSub.
    # sub2 = JoinSubstitutions(text + join_symbol + text, join_symbol)
    # assert sub1 != sub2
    # sub2 = sub1
    # sub2 += ""
    # assert sub1 != sub2
