import esper

from simulator.components.Renderable import Renderable
from simulator.components.Position import Position
from simulator.components.Label import Label


class RenderProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self, env):
        # This will iterate over every Entity that has BOTH of these components:
        for ent, (pos, rend) in self.world.get_components(Position, Renderable):
            if not pos.changed:
                print("[Render] Position not changed")
                continue
            # Update the Renderable Component's position by it's Velocity:
            # An example of keeping the sprite inside screen boundaries. Basically,
            # adjust the position back inside screen boundaries if it is outside:
            if rend.is_primitive:
                lst_pos = rend.center
                this_pos = (pos.x + pos.w // 2, pos.y + pos.h // 2)
                delta = this_pos[0] - lst_pos[0], this_pos[1] - lst_pos[1]
                rend.center = this_pos
                for i, v in enumerate(rend.sprite.vertices):
                    rend.sprite.vertices[i] = int(v + delta[(i&1)])
                if self.world.has_component(ent, Label):
                    label = self.world.component_for_entity(ent, Label)
                    label.labelTag.x = this_pos[0]
                    label.labelTag.y = this_pos[1]
            else:
                rend.sprite.position = (pos.x, pos.y)
