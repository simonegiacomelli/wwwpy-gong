import js
import inspect
import logging

import wwwpy.remote.component as wpc

logger = logging.getLogger(__name__)


class CountdownComponent(wpc.Component, tag_name='u-countdown'):
    _btn_start: js.HTMLButtonElement = wpc.element()
    def init_component(self):
        # language=html
        self.element.innerHTML = """
<button data-name="_btn_start">Start</button>


"""
    
    async def _btn_start__click(self, event):
        logger.debug(f'{inspect.currentframe().f_code.co_name} event fired %s', event)

    
