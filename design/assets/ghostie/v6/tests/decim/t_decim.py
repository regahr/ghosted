# Test (direction.md step 2): does a decimated smooth surface give a smoother outline per triangle than the lattice?
import bpy, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
B = bpy.data.objects['body']
B.modifiers.remove(B.modifiers['skin'])
B.vertex_groups.clear()
m = B.modifiers.new('sub', 'SUBSURF'); m.levels = 2; m.render_levels = 2
with bpy.context.temp_override(object=B, active_object=B): bpy.ops.object.modifier_apply(modifier='sub')
print('HI', len(B.data.polygons))
d = B.modifiers.new('dec', 'DECIMATE'); d.decimate_type = 'COLLAPSE'; d.use_symmetry = True; d.symmetry_axis = 'X'
B.data.calc_loop_triangles(); n = len(B.data.loop_triangles); d.ratio = 478 / n
with bpy.context.temp_override(object=B, active_object=B): bpy.ops.object.modifier_apply(modifier='dec')
B.data.calc_loop_triangles(); print('LOW', len(B.data.loop_triangles))
B.data.polygons.foreach_set('use_smooth', [True] * len(B.data.polygons))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, 'ghostie.blend'))
