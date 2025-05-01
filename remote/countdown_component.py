import asyncio
import inspect
import logging
import time

import js
import wwwpy.remote.component as wpc

logger = logging.getLogger(__name__)


class CountdownComponent(wpc.Component, tag_name='u-countdown'):
    _btn_start: js.HTMLButtonElement = wpc.element()
    _btn_stop: js.HTMLButtonElement = wpc.element()
    _total_time: js.HTMLDivElement = wpc.element()
    _countdown: js.HTMLDivElement = wpc.element()

    def init_component(self):
        self.start_time = None
        self.task = None
        self.element.innerHTML = """
            <button data-name="_btn_start">Start</button>
            <button data-name="_btn_stop">Stop</button>
            <div style="height: 8px; border: none; margin: none;"></div>
            <div data-name="_total_time" style="margin-bottom:5px">#</div>
            <div data-name="_countdown">#</div>
        """
        self.cycle_time = 60
        self.on_completion = lambda: None
        self.sound_on_start = False

    def disconnectedCallback(self):
        self.stop()

    @property
    def cycle_time(self) -> int:
        return self._cycle_time

    @cycle_time.setter
    def cycle_time(self, value):
        logger.debug(f'setting cycle_time to {value}')
        self._cycle_time = value
        self.stop()

    def _format_time(self, seconds):
        if seconds < 0 or seconds is None:
            seconds = 0
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes:02}:{remaining_seconds:02}"

    def _update_ui(self, countdown, total_time):
        self._countdown.innerHTML = f"Cycle end:<br>{self._format_time(countdown)}"
        self._total_time.innerHTML = f"Total time:<br>{self._format_time(total_time)}"

    def _cycle_complete(self):
        self.stop()
        self.on_completion()
        js.Audio.new("https://fs.simone.pro/shared/gong/gong-short.ogg").play()

    async def _timer_tick(self):
        start = True
        while self.start_time:
            elapsed = int(time.time() - self.start_time)
            cycle_used = elapsed % self.cycle_time
            if cycle_used == 0:
                if start:
                    start = False
                else:
                    await self._cycle_complete()
                    return
            left = self.cycle_time - cycle_used
            self._update_ui(left, elapsed)
            self._set_active(True)
            await asyncio.sleep(1)

    async def _btn_start__click(self, event):
        logger.debug(f'{inspect.currentframe().f_code.co_name} event fired %s', event)
        self.start()

    def start(self):
        if not self.start_time:
            self.start_time = time.time()
            self.task = asyncio.create_task(self._timer_tick())

    async def _btn_stop__click(self, event):
        self.stop()

    def stop(self):
        if self.task:
            self.task.cancel()
        self.start_time = None
        self._update_ui(self.cycle_time, 0)
        self._set_active(False)

    def _set_active(self, active: bool):
        # change the background color of self.element to something distinct if it's active or delete the bk color if not
        style = self.element.style
        if active:
            style.backgroundColor = "darkblue"
        else:
            style.removeProperty('background-color')


