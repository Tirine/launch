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

"""Module for the JoinSubstitutions substitution."""
from __future__ import annotations

from math import floor

from typing import List
from typing import Text

from ..launch_context import LaunchContext
from ..some_substitutions_type import SomeSubstitutionsType
from ..substitution import Substitution
from ..utilities import normalize_to_list_of_substitutions
from .substitution_failure import SubstitutionFailure


class JoinSubstitutions(Substitution):
    """
    Substitution that join other substitutions on evaluation.

    Beware: This should not be used instead of PathJoinSubstitution for paths,
    as that is platform independent.
    """

    def __init__(self, substitutions: SomeSubstitutionsType = [], join_symbol: Text = "") -> None:
        """Create a JoinSubstitutions."""
        Substitution.__init__(self)
        self.__join_symbol = join_symbol
        self.__substitutions = []
        self.extend(substitutions)

    def __add__(self, substitutions: SomeSubstitutionsType) -> JoinSubstitutions:
        return JoinSubstitutions(self.__substitutions, self.__join_symbol).extend(substitutions)

    def __iadd__(self, substitutions: SomeSubstitutionsType) -> JoinSubstitutions:
        return self + substitutions

    def __radd__(self, substitutions: SomeSubstitutionsType) -> JoinSubstitutions:
        return JoinSubstitutions(substitutions, self.__join_symbol).extend(self.__substitutions)

    def __nonzero__(self) -> bool:
        return len(self.__substitutions) != 0

    def __mul__(self, integer: int) -> JoinSubstitutions:
        if integer < 0:
            raise ValueError("Negative multiplications are not possible." +
                             " For Substitution: '{}'".format(self.describe()))
        if floor(integer) != integer:
            raise ValueError("Non-integer multiplications are not possible." +
                             " For Substitution: '{}'".format(self.describe()))
        new_substitution = JoinSubstitutions(join_symbol=self.__join_symbol)
        for i in range(integer):
            new_substitution += self
        return new_substitution

    def __imul__(self, integer: int) -> JoinSubstitutions:
        return self*integer

    def __rmul__(self, integer: int) -> JoinSubstitutions:
        return self*integer

    def __eq__(self, other) -> bool:
        if type(self) is type(other):
            if self is other:
                return True
            if self.describe() == other.describe():
                return True
        return False

    @property
    def list_of_substitutions(self) -> List[SomeSubstitutionsType]:
        """Getter for substitutions."""
        return self.__substitutions

    @property
    def join_symbol(self) -> Text:
        """Getter for substitutions."""
        return self.__join_symbol

    def extend(self, substitutions: SomeSubstitutionsType) -> JoinSubstitutions:
        """
        Extend substitutions or list of substitutions to the existing ones.

        If it's the list contains another list, a sub_list, the sub_list will be made into
        a JoinSubstitution(sub_list).
        """
        try:
            if isinstance(substitutions, List):
                for sub in substitutions:
                    if isinstance(sub, List):
                        sub = JoinSubstitutions(sub)
                    sub = normalize_to_list_of_substitutions(sub)
                    self.__substitutions.extend(sub)
            else:
                self.__substitutions.extend(normalize_to_list_of_substitutions(substitutions))
            return self
        except TypeError:
            raise SubstitutionFailure(
                f'Cannot join a "{type(substitutions).__name__}" object as substitution.'
            )

    def set_join_symbol(self, symbol: Text) -> None:
        self.__join_symbol = symbol

    def describe(self) -> Text:
        """Return a description of this substitution as a string."""
        return "JoinSubstitutions('{}')".format(
            " + '{}' + ".format(self.__join_symbol)
            .join([s.describe() for s in self.__substitutions]))

    def perform(self, context: LaunchContext) -> Text:
        """Perform the substitution by retrieving the local variable."""
        performed_substitutions = [sub.perform(context) for sub in self.__substitutions]
        return self.__join_symbol.join(performed_substitutions)
