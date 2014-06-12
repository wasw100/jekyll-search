# -*- coding: utf-8 -*-
"""
create pylucene index
"""

from flask import current_app


def build_index():
    store_dir = current_app.config['INDEX_STORE_DIR']
    print store_dir