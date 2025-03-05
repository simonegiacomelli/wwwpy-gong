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
            <div>v1.0.7</div>
            <button data-name="_btn_start">Start</button>&nbsp;
            <button data-name="_btn_stop">Stop</button>
            <div style="height: 8px; border: none; margin: none;"></div>
            <div data-name="_total_time">#</div>
            <br>
            <div data-name="_countdown">#</div>
        """
        self.cycle_time = 60
        self._reset_ui()

    @property
    def cycle_time(self) -> int:
        return self._cycle_time

    @cycle_time.setter
    def cycle_time(self, value):
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

    async def _play_sound(self):
        js.Audio.new("https://fs.simone.pro/shared/gong/singing-bowl-gong-69238.mp3").play()

    async def _timer_tick(self):
        while self.start_time:
            elapsed = int(time.time() - self.start_time)
            cycle_used = elapsed % self.cycle_time
            if cycle_used == 0:
                await self._play_sound()
            self._update_ui(self.cycle_time - cycle_used, elapsed)
            await asyncio.sleep(1)

    async def _btn_start__click(self, event):
        logger.debug(f'{inspect.currentframe().f_code.co_name} event fired %s', event)
        await self.start()

    async def start(self):
        if not self.start_time:
            self.start_time = time.time()
            self.task = asyncio.create_task(self._timer_tick())

    async def _btn_stop__click(self, event):
        logger.debug(f'{inspect.currentframe().f_code.co_name} event fired %s', event)
        await self.stop()

    async def stop(self):
        if self.task:
            self.task.cancel()
        self.start_time = None
        self._reset_ui()

    def _reset_ui(self):
        self._update_ui(self.cycle_time, 0)
