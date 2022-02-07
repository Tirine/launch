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

"""Module for the PathJoinSubstitution substitution."""

import os
from typing import Iterable
from typing import Text

from ..launch_context import LaunchContext
from ..some_substitutions_type import SomeSubstitutionsType
from ..substitution import Substitution


class JoinSubstitutions(Substitution):
    """Substitution that join other substitutions on evaluation."""

    def __init__(self, substitutions: Iterable[SomeSubstitutionsType], joinWith: Text = "") -> None:
        """Create a PathJoinSubstitution."""
        from ..utilities import normalize_to_list_of_substitutions
        self.__substitutions = normalize_to_list_of_substitutions(substitutions)
        self.__joinWith = joinWith

    @property
    def substitutions(self) -> Iterable[Substitution]:
        """Getter for substitutions."""
        return self.__substitutions

    def describe(self) -> Text:
        """Return a description of this substitution as a string."""
        return "JoinSubstitutions('{}')".format(' + '.join([s.describe() for s in self.substitutions]))

    def perform(self, context: LaunchContext) -> Text:
        """Perform the substitution by retrieving the local variable."""
        performed_substitutions = [sub.perform(context) for sub in self.__substitutions]
        return self.__joinWith.join(performed_substitutions)
