import inspect
import wwwpy.remote.component as wpc
import js

import logging

logger = logging.getLogger(__name__)
from remote.countdown_component import CountdownComponent


class MainComponent(wpc.Component, tag_name='component-1'):
    _c1: CountdownComponent = wpc.element()
    _c2: CountdownComponent = wpc.element()

    def init_component(self):
        # language=html
        self.element.innerHTML = """<div style="display: flex; gap: 10px">
    <u-countdown data-name='_c1'></u-countdown>
    <u-countdown data-name='_c2'></u-countdown>
</div>
"""
        self._c1.cycle_time = 20*60
        self._c2.cycle_time = 20
