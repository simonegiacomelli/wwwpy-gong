import logging

import js
import wwwpy.remote.component as wpc

logger = logging.getLogger(__name__)
from remote.countdown_component import CountdownComponent


class MainComponent(wpc.Component, tag_name='component-1'):
    _c1: CountdownComponent = wpc.element()
    _c2: CountdownComponent = wpc.element()
    _c3: CountdownComponent = wpc.element()

    def init_component(self):
        # language=html
        self.element.innerHTML = """
v1.0.8        
<div style="display: flex; gap: 10px">
    <u-countdown data-name='_c1'></u-countdown>
    <u-countdown data-name='_c2'></u-countdown>
    <u-countdown data-name='_c3'></u-countdown>
</div>
"""

        self._c1.cycle_time = 20 * 60
        self._c2.cycle_time = 20
        self._c3.cycle_time = 20
        self._c1.on_completion = lambda: self._c2.start()
        self._c2.on_completion = lambda: self._c3.start()
        self._c3.on_completion = lambda: self._c1.start()
        js.document.body.style.marginTop = "3px"
        js.document.body.style.marginLeft = "3px"
