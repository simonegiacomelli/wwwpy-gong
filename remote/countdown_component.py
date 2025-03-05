import js
import inspect
import logging
import time
import asyncio

import wwwpy.remote.component as wpc

logger = logging.getLogger(__name__)


class CountdownComponent(wpc.Component, tag_name='u-countdown'):
    _btn_start: js.HTMLButtonElement = wpc.element()
    _btn_stop: js.HTMLButtonElement = wpc.element()
    _total_time: js.HTMLDivElement = wpc.element()
    _countdown: js.HTMLDivElement = wpc.element()

    def init_component(self):
        self.cycle_time = 60
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
        self.reset_ui()

    def format_time(self, seconds):
        if seconds < 0 or seconds is None:
            seconds = 0
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes:02}:{remaining_seconds:02}"

    def update_ui(self, countdown, total_time):
        self._countdown.innerHTML = f"Cycle end:<br>{self.format_time(countdown)}"
        self._total_time.innerHTML = f"Total time:<br>{self.format_time(total_time)}"

    async def play_sound(self):
        js.Audio.new("https://fs.simone.pro/shared/gong/singing-bowl-gong-69238.mp3").play()

    async def timer_tick(self):
        while self.start_time:
            elapsed = int(time.time() - self.start_time)
            cycle_used = elapsed % self.cycle_time
            if cycle_used == 0:
                await self.play_sound()
            self.update_ui(self.cycle_time - cycle_used, elapsed)
            await asyncio.sleep(1)

    async def _btn_start__click(self, event):
        logger.debug(f'{inspect.currentframe().f_code.co_name} event fired %s', event)
        if not self.start_time:
            self.start_time = time.time()
            self.task = asyncio.create_task(self.timer_tick())

    async def _btn_stop__click(self, event):
        logger.debug(f'{inspect.currentframe().f_code.co_name} event fired %s', event)
        if self.task:
            self.task.cancel()
        self.start_time = None
        self.reset_ui()

    def reset_ui(self):
        self.update_ui(self.cycle_time, 0)
