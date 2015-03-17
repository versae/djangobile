Just set a new context processor in your project settings.py

```
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    # This context processor is required to djangobile works properly.
    'djangobile.context_processors.mobile',
)
```