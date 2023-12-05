"""
Django settings for tests
"""
from sandbox.settings.base import *  # noqa: F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Media directory dedicated to tests to avoid polluting other environment
# media directory
MEDIA_ROOT = VAR_PATH / "media-tests"  # noqa: F405

# Add specific test templates
TEMPLATES[0]["DIRS"].extend([
    BASE_DIR / "tests" / "data_fixtures" / "templates" / "staticpages_tests",
])

# Neutralize default settings
STATICPAGES = []
STATICPAGES_DEFAULT_TEMPLATEPATH = None
STATICPAGES_DEFAULT_NAME_BASE = None
STATICPAGES_DEFAULT_URLPATH = None
