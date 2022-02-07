#!/usr/bin/env python3

# Copyright 2020 Accenture, All Rights Reserved.
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
#
# DISTRIBUTION A. Approved for public release; distribution unlimited.


"""Module extending the LaunchConfiguration substitution."""

from typing import List
from typing import Optional
from typing import Text
from ..substitutions import LaunchConfiguration
from ..some_substitutions_type import SomeSubstitutionsType
from ..actions import DeclareLaunchArgument


class SimpleLaunchArgument():

    def __init__(
        self,
        name: Text,
        *,
        default_value: Optional[SomeSubstitutionsType] = None,
        description: Optional[Text] = None,
        choices: List[Text] = None,
        **kwargs
    ) -> None:
        """Declare the launch argument."""
        self.__declaration = DeclareLaunchArgument(
            name=name,
            default_value=default_value,
            description=description,
            choices=choices,
            **kwargs
        )
        """Then initialize it."""
        self.__variable = LaunchConfiguration(variable_name=name, default=default_value)

    @property
    def declaration(self) -> DeclareLaunchArgument:
        return self.__declaration

    @property
    def variable(self) -> LaunchConfiguration:
        return self.__variable
