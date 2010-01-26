#
#  Copyright (C) 2009 Juan Pedro Bolivar Puente, Alberto Villegas Erce
#  
#  This file is part of Pigeoncide.
#
#  Pigeoncide is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  
#  Pigeoncide is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from base.conf import *
from timer import *
import task

import patch_messenger
from direct.showbase.ShowBase import ShowBase
from direct.filter.CommonFilters import CommonFilters
from pandac.PandaModules import *

class PandaController (object):

    DEFAULT_FULLSCREEN = False
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 600
    DEFAULT_FPS = 60
    DEFAULT_FRAME_METER = False

    DEFAULT_MAX_DELTA = 1. / 20.

    def __init__ (self):
        super (PandaController, self).__init__ ()
        self._timer = Timer ()
        self._timer.max_delta = self.DEFAULT_MAX_DELTA
        self._tasks = task.TaskGroup ()
        self._tasks.add (self._panda_task)
    
    @property
    def timer (self):
        return self._timer

    @property
    def tasks (self):
        return self._tasks

    def start (self, title):
        
        cfg = GlobalConf ().child ('panda') 

        self.set_defaults (cfg)
        self.base = ShowBase ()
        self.base.disableMouse ()

        self.create_properties (title)
        self.update_properties (cfg)
        self.listen_conf (cfg)

        loadPrcFileData ("", "interpolate-frames 1")
        path = getModelPath ()
        path.prependPath ('./data')
        
        
        self.base.enableParticles ()

        self.filters = CommonFilters (self.base.win, self.base.cam)
                
    def loop (self):        
        self._timer.reset ()
        self._timer.loop (self._tasks.update)
        
    def set_defaults (self, cfg):
        cfg.child ('fps').default (self.DEFAULT_FPS)
        cfg.child ('width').default (self.DEFAULT_WIDTH)
        cfg.child ('height').default (self.DEFAULT_HEIGHT)
        cfg.child ('fullscreen').default (self.DEFAULT_FULLSCREEN)
        cfg.child ('frame-meter').default (self.DEFAULT_FRAME_METER)

    def listen_conf (self, cfg):
        cfg.on_conf_nudge += self.update_properties
        
        cfg.child ('fps').on_conf_change += self.update_fps
        cfg.child ('frame-meter').on_conf_change += self.update_frame_meter
    
    def create_properties (self, title):
        self._prop = WindowProperties ()
        self._prop.setTitle (title)
        self._prop.setCursorHidden (True)
        self._prop.setMouseMode (WindowProperties.MRelative)

    def hide_mouse (self):
        self._prop.setCursorHidden (True)
        self.base.win.requestProperties (self._prop)

    def show_mouse (self):
        self._prop.setCursorHidden (True)
        self.base.win.requestProperties (self._prop)

    def has_shaders (self):
        return self.base.win.getGsg().getSupportsBasicShaders() == 0
        
    def update_properties (self, cfg):
        self._prop.setSize (cfg.child ('width').value,
                            cfg.child ('height').value)
        self._prop.setFullscreen (cfg.child ('fullscreen').value)
        self.base.win.requestProperties (self._prop)
        
        self._timer.fps = cfg.child ('fps').value
        self.base.setFrameRateMeter (cfg.child ('frame-meter').value)

    def update_frame_meter (self, cfg):
        self.base.setFrameRateMeter (cfg.value)

    def update_fps (self, cfg):
        self._timer.fps = cfg.value

    def _panda_task (self, timer):
        if self._tasks.count > 1:
            taskMgr.step ()
            return task.running
        return task.killed
