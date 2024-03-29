# -*- coding: UTF-8 -*-
# Copyright (C) 2010 Taverne Sylvain <sylvain@itaapy.com>
# Copyright (C) 2010-2011 Henry Obein <henry@itaapy.com>
# Copyright (C) 2010-2011 Hervé Cauwelier <herve@itaapy.com>
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
from itools.datatypes import Boolean
from itools.gettext import MSG
from itools.web import STLView

# Import from ikaaro
from ikaaro.autoform import RadioWidget, RTEWidget
from ikaaro.webpage import HTMLEditView

# Import from itws
from tags import TagsAware_Edit
from widgets import Advance_RTEWidget



class WebPage_Edit(TagsAware_Edit, HTMLEditView):


    def _get_schema(self, resource, context):
        return merge_dicts(HTMLEditView._get_schema(self, resource, context),
                           TagsAware_Edit._get_schema(self, resource, context),
                           display_title=Boolean)


    def _get_widgets(self, resource, context):
        widgets = HTMLEditView._get_widgets(self, resource, context)[:]
        # Add display title widget
        display_title_widget = RadioWidget('display_title',
                title=MSG(u'Display title on webpage view ?'))
        widgets.insert(2, display_title_widget)
        # Tags
        widgets.extend(TagsAware_Edit._get_widgets(self, resource, context))

        # TODO: Add a mechanism in ikaaro that allow to configure RTE
        new_widgets = []
        for w in widgets:
            if issubclass(w, RTEWidget):
                w = Advance_RTEWidget(w.name, title=w.title)
            new_widgets.append(w)
        return freeze(new_widgets)


    def get_value(self, resource, context, name, datatype):
        if name in ('data', 'file'):
            return HTMLEditView.get_value(self, resource, context, name,
                                          datatype)
        if name in TagsAware_Edit.keys:
            return TagsAware_Edit.get_value(self, resource, context, name,
                                            datatype)
        return HTMLEditView.get_value(self, resource, context, name, datatype)


    def set_value(self, resource, context, name, form):
        if name == 'data':
            return HTMLEditView.set_value(self, resource, context, name, form)
        if name in TagsAware_Edit.keys:
            return TagsAware_Edit.set_value(self, resource, context, name,
                                            form)
        return HTMLEditView.set_value(self, resource, context, name, form)


    def action(self, resource, context, form):
        return HTMLEditView.action(self, resource, context, form)



class WebPage_View(STLView):

    access = 'is_allowed_to_view'
    title = MSG(u'View')
    icon = 'view.png'
    template = '/ui/common/WebPage_view.xml'


    def get_namespace(self, resource, context):
        title = resource.get_property('display_title')
        if title:
            title = resource.get_title()
        return {'name': resource.name.replace('.', '-dot-'),
                'title': title,
                'content': resource.get_html_data()}
