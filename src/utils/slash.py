"""
Unifier - A sophisticated Discord bot uniting servers and platforms
Copyright (C) 2023-present  UnifierHQ

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import nextcord

class SlashHelper:
    def __init__(self, language):
        self.language = language

    def option(self, name, *args, **kwargs):
        cogname, cmdname, optionname = name.split('.')
        localizations = self.language.slash_options(cogname+'.'+cmdname)
        if not localizations:
            return nextcord.SlashOption(
                *args,
                name=optionname,
                **kwargs
            )

        base = localizations.pop(self.language.get_locale())

        names = {}
        descriptions = {}

        for locale in localizations.keys():
            try:
                names.update({locale: localizations[locale][optionname]['name']})
                descriptions.update({locale: localizations[locale][optionname]['description']})
            except KeyError:
                pass

        return nextcord.SlashOption(
            *args,
            name=optionname,
            description=base[optionname]['description'],
            name_localizations=names,
            description_localizations=descriptions,
            **kwargs
        )
