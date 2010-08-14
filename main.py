#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import logging, os, sys

# Google App Engine imports.
from google.appengine.ext.webapp import util

# # Remove the standard version of Django.
for k in [k for k in sys.modules if k.startswith('django')]:
    del sys.modules[k]

# # Force sys.path to have our own directory first, in case we want to import
# # from it.
BASE_PATH = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(BASE_PATH))
for path, dirs, files in os.walk(os.path.join(BASE_PATH, 'deps')):
    for dir in dirs:
        sys.path.insert(0, os.path.join(path, dir))
sys.path.insert(0, os.path.join(BASE_PATH, 'PhoneTap'))

# Must set this env var *before* importing any part of Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'phonetap.settings'

import django.core.handlers.wsgi
import django.core.signals

def log_exception(*args, **kwds):
   logging.exception('Exception in request:')

# Log errors.
django.core.signals.got_request_exception.connect(log_exception)

def main():
    application = django.core.handlers.wsgi.WSGIHandler()
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()