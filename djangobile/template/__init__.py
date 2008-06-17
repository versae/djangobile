# -*- coding: utf-8 -*-


class Ideal(object):
    def __init__(self, source, origin=None, name=None):
        self.source = source.encode("utf-8")

    def render(self, context=None, cls=None):
        if not context:
            return self.source
        device = context.get('device')
        if cls:
            processor = cls(self.source)
            return processor.render(context)
        preferred_markup = device.get('preferred_markup').lower()
        if preferred_markup in ('html_web_3_2', 'html_web_4_0'):
            from djangobile.template.ideal import HtmlWeb as Processor
        elif preferred_markup in ('html_wi_imode_compact_generic', ):
            from djangobile.template.ideal import GenericIMode as Processor
        elif preferred_markup in ('html_wi_imode_html_1', 'html_wi_imode_html_2', \
                                  'html_wi_imode_html_3', 'html_wi_imode_html_4', \
                                  'html_wi_imode_html_5'):
            from djangobile.template.ideal import IMode as Processor
        elif preferred_markup in ('html_wi_oma_xhtmlmp_1_0', ):
            from djangobile.template.ideal import OmaXhtmlMp as Processor
        elif preferred_markup in ('html_wi_w3_xhtmlbasic', ):
            from djangobile.template.ideal import W3Xhtml as Processor
        elif preferred_markup in ('wml_1_1', 'wml_1_2', 'wml_1_3'):
            from djangobile.template.ideal import Wml as Processor
        else:
            from djangobile.template.ideal import GenericXhtml as Processor
        processor = Processor(self.source)
        return processor.render(context)
