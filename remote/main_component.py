import inspect
import logging

import js
import wwwpy.remote.component as wpc

logger = logging.getLogger(__name__)
from remote.countdown_component import CountdownComponent


class MainComponent(wpc.Component, tag_name='component-1'):
    _c1: CountdownComponent = wpc.element()
    _c2: CountdownComponent = wpc.element()
    _c3: CountdownComponent = wpc.element()
    _btn_stop: js.HTMLButtonElement = wpc.element()

    def init_component(self):
        # language=html
        self.element.innerHTML = """
v2.0.1         
<button data-name="_btn_stop">Stop</button>
<div style="display: flex; gap: 10px; margin-top : 5px;">
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

    # when the app starts it doesn't have the rights to play sounds, so the
    # timer starts but then it doesn't play the sound. It's bad because you
    # see the timer going but in the end you don't have the audio cue and miss
    # the end of the cycle.
    # async def after_init_component(self):
    #     self._c1.start()

    async def _btn_stop__click(self, event):
        for c in [self._c1, self._c2, self._c3]:
            c.stop()
    
