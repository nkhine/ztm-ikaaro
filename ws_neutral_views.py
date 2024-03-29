# -*- coding: UTF-8 -*-
# Copyright (C) 2010 Hervé Cauwelier <herve@itaapy.com>
# Copyright (C) 2010 Taverne Sylvain <sylvain@itaapy.com>
# Copyright (C) 2010-2011 Henry Obein <henry@itaapy.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Import from itools
from itools.core import freeze, merge_dicts
from itools.database import PhraseQuery
from itools.gettext import MSG

# Import from ikaaro
from ikaaro.autoform import SelectWidget, TextWidget
from ikaaro.datatypes import Multilingual
from ikaaro.resource_views import DBResource_Edit

# Import from itws
from bar import Section
from rss import BaseRSS
from section_views import SectionViews_Enumerate
from tags import TagsAware
from views import EditView



class NeutralWS_RSS(BaseRSS):

    excluded_formats = freeze(['rssfeeds'])


    def get_base_query(self, resource, context):
        query = BaseRSS.get_base_query(self, resource, context)
        query.append(PhraseQuery('workflow_state', 'public'))
        return query


    def get_item_value(self, resource, context, item, column, site_root):
        brain, item_resource = item
        if column == 'pubDate':
            if isinstance(item_resource, TagsAware):
                return brain.pub_datetime
            else:
                return brain.mtime
        elif column == 'title':
            # Special case for the title
            title = item_resource.get_title()
            # FIXME
            if brain.name == 'index':
                parent = item_resource.parent
                if isinstance(parent, Section):
                    title = parent.get_title()
            return title

        return BaseRSS.get_item_value(self, resource, context, item,
                                      column, site_root)



class NeutralWS_Edit(EditView, DBResource_Edit):


    def _get_widgets(self, resource, context):
        return freeze(DBResource_Edit._get_widgets(self, resource, context)
            + [SelectWidget('view', title=MSG(u'View'),
                            has_empty_option=False),
               TextWidget('breadcrumb_title', title=MSG(u'Breadcrumb title'))])


    def _get_schema(self, resource, context):
        return merge_dicts(DBResource_Edit._get_schema(self, resource, context),
                           view=SectionViews_Enumerate,
                           breadcrumb_title=Multilingual)


    def action(self, resource, context, form):
        self.check_edit_conflict(resource, context, form)
        if context.edit_conflict:
            return
        EditView.action(self, resource, context, form)
        return DBResource_Edit.action(self, resource, context, form)
