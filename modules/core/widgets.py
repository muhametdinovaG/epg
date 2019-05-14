from django.contrib.admin import widgets
from django.utils.safestring import mark_safe


class MultiImageInput(widgets.AdminFileWidget):

    def render(self, name, value, attrs=None, renderer=None):
        attrs['multiple'] = 'true'
        output = super(MultiImageInput, self).render(name, value, attrs=attrs)
        return mark_safe(output)
