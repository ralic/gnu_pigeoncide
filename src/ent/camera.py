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

from pandac.PandaModules import Vec3
from base.util import bound
from observer import EntityListener
import math

class EntityFollower (EntityListener):

    HANGLE   = math.pi / 12
    DISTANCE = 20
    
    def __init__ (self, camera = None, *a, **k):
        super (EntityFollower, self).__init__ (*a, **k)
        self.camera = camera
        self.distance = self.DISTANCE
        self.hangle   = self.HANGLE
        
    def on_entity_set_position (self, ent, pos):
        angle = ent.angle
        direction = Vec3 (math.sin (angle),
                          math.cos (angle),
                          - math.sin  (self.hangle))
        position  = Vec3 (* ent.position)

        self.camera.setPos (position + direction * (- self.distance))
        self.camera.lookAt (*pos)
        

