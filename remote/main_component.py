import inspect
import wwwpy.remote.component as wpc
import js

import logging

logger = logging.getLogger(__name__)
from remote.countdown_component import CountdownComponent

class MainComponent(wpc.Component, tag_name='component-1'):

    def init_component(self):
        # language=html
        self.element.innerHTML = """
<div>component-1</div>
<u-countdown></u-countdown>
"""
