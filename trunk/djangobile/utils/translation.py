# -*- coding: utf-8 -*-
import os
import sys
import gettext as gettext_module

from django.utils.thread_support import currentThread
from django.utils import translation
from django.utils.translation import trans_real as trans

from djangobile.utils import get_device_directories


device_translations = {}

def add_device_locale(device=None):
    global device_translations

    from django.conf import settings

    if not device and not settings.USE_I18N:
        return

    current_translation = trans._active[currentThread()]
    lang = current_translation.language()
    key = "%s#%s" % (lang, device.id)
    loc = trans.to_locale(lang)
    klass = trans.DjangoTranslation
    if sys.version_info < (2, 4):
        klass = trans.DjangoTranslation23

    device_trans = device_translations.get(key, None)
    if device_trans is None:
        translations_paths = get_translations_paths(device)
        for translations_path in translations_paths:
            try:
                t = gettext_module.translation('django', translations_path,
                                               [loc], klass)
                t.set_language(lang)
                if device_trans is None:
                    device_trans = t
                else:
                    device_trans.merge(t)
            except IOError, e:
                pass
        device_translations[key] = device_trans
        fallback = getattr(device_trans, '_fallback', None)
        if not fallback and hasattr(device_trans, 'add_fallback'):
            device_trans.add_fallback(current_translation)
    if device_trans:
        trans._active[currentThread()] = device_trans
    else:
        trans._active[currentThread()] = current_translation


def get_locale_paths(device, path):
    locale_paths = []
    device_directories = get_device_directories(device)
    for device_directory in device_directories:
        locale_path = os.path.join(path, device_directory)
        if os.path.isdir(locale_path):
            locale_paths.append(locale_path)
    return locale_paths


def get_translations_paths(device):
    from django.conf import settings
    translations_paths = []

    globalpath = os.path.join(os.path.dirname(sys.modules[settings.__module__].__file__), 'locale')
    translations_paths.extend(get_locale_paths(device, globalpath))

    if settings.SETTINGS_MODULE is not None:
        parts = settings.SETTINGS_MODULE.split('.')
        project = __import__(parts[0], {}, {}, [])
        projectpath = os.path.join(os.path.dirname(project.__file__), 'locale')

    for localepath in settings.LOCALE_PATHS:
        if os.path.isdir(localepath):
            translations_paths.extend(get_locale_paths(device, localepath))

    if projectpath and os.path.isdir(projectpath):
        translations_paths.extend(get_locale_paths(device, projectpath))

    for appname in settings.INSTALLED_APPS:
        p = appname.rfind('.')
        if p >= 0:
            app = getattr(__import__(appname[:p], {}, {}, [appname[p+1:]]), appname[p+1:])
        else:
            app = __import__(appname, {}, {}, [])

        apppath = os.path.join(os.path.dirname(app.__file__), 'locale')
        if os.path.isdir(apppath):
            translations_paths.extend(get_locale_paths(device, apppath))

    return translations_paths

