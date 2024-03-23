# Генерируем мир для симуляции


xml_start = '''
<?xml version="1.0" ?>
<sdf version="1.5">
  <world name="default">

    <include>
      <uri>model://aruco_target_map_txt</uri>
      <pose>0.0 0.0 0.0 0.0 0.0 0.0</pose>
    </include>
    <include>
      <uri>model://sun</uri>
    </include>
    <include>
      <uri>model://parquet_plane</uri>
      <pose>0 0 -0.01 0 0 0</pose>
    </include>
    '''

xml_end = '''


    <scene>
      <ambient>0.8 0.8 0.8 1</ambient>
      <background>0.8 0.9 1 1</background>
      <shadows>false</shadows>
      <grid>false</grid>
      <origin_visual>false</origin_visual>
    </scene>
  
    <physics name='default_physics' default='0' type='ode'>
      <gravity>0 0 -9.8066</gravity>
      <ode>
        <solver>
          <type>quick</type>
          <iters>10</iters>
          <sor>1.3</sor>
          <use_dynamic_moi_rescaling>0</use_dynamic_moi_rescaling>
        </solver>
        <constraints>
          <cfm>0</cfm>
          <erp>0.2</erp>
          <contact_max_correcting_vel>100</contact_max_correcting_vel>
          <contact_surface_layer>0.001</contact_surface_layer>
        </constraints>
      </ode>
      <max_step_size>0.004</max_step_size>
      <real_time_factor>1</real_time_factor>
      <real_time_update_rate>250</real_time_update_rate>
      <magnetic_field>6.0e-6 2.3e-5 -4.2e-5</magnetic_field>
    </physics>
  </world>
</sdf>'''

# координаты зданий
box_coords = [(4.2, 3.2), (6.4, 3.4), (4.2, 1.2), (5.2, 2.2)]
# типы коробок
box_sizes = ["Green_box_25", "Red_box_50", "Yellow_box_75", "Blue_box_100"]

for i in range(len(box_coords)):
    xml_start += f'''
    
    <include>
      <uri>model://{box_sizes[i]}</uri>
      <name>{box_sizes[i]}_{i}</name>

      <pose>{box_coords[i][0]} {box_coords[i][1]} 0.0 0 0 0</pose>
    </include>
    '''

# записываем мир в файл
f = open('test_world.world', 'w')
f.write(xml_start+xml_end)
# print(xml_start+xml_end) 