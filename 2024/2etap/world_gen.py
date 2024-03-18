xml_start = '''
<?xml version="1.0" ?>
<sdf version="1.5">
  <world name="default">
    <!-- A global light source -->
    <include>
      <uri>model://sun</uri>
    </include>
    <include>
      <uri>model://parquet_plane</uri>
      <pose>0 0 -0.01 0 0 0</pose>
    </include>

    <include>
      <uri>model://aruco_cmit_txt</uri>
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


boxes_data = [float(i) for i in input().strip()[1:-1].replace(')', '').replace('(', '').replace(',', '').split()]
boxes = []
box = []
for i in range(1, len(boxes_data)+1):
    if i % 3 == 0:
        box.append(boxes_data[i-1])
        boxes.append(box)
        box = []
        continue
    box.append(boxes_data[i-1])

human_data = input().strip()[1:-1].replace(')', '').replace('(', '').replace(',', '').replace("'", '').split()
human = []
h = []
for i in range(1, len(human_data)+1):
    if i % 3 == 0:
        h.append(human_data[i-1])
        human.append(h)
        h = []
        continue
    h.append(human_data[i-1])

for i in range(len(boxes)):
    xml_start += f'''

    <model name='nto_box_{i}'>
     <pose>{boxes[i][0]} {boxes[i][1]} 0.0 0 0 0</pose>
     <link name='link'>
       <collision name='collision'>
         <geometry>
           <box>
             <size>1 1 {boxes[i][2]-0.2}</size>
           </box>
         </geometry>
       </collision>
       <visual name='visual'>
         <geometry>
           <box>
             <size>1 1 {boxes[i][2]-0.2}</size>
           </box>
         </geometry>
         <material>
           <script>
             <name>Gazebo/Gray</name>
             <uri>file://media/materials/scripts/gazebo.material</uri>
           </script>
         </material>
       </visual>
       <static>1</static>
     </link>
    </model>'''

for i in range(len(human)):
    xml_start += f'''

    <model name='nto_human_{i}'>
     <pose>{human[i][0]} {human[i][1]} 0 0 0 0</pose>
     <link name='link'>
       <collision name='collision'>
         <geometry>
          <cylinder>
            <radius>0.125</radius>
            <length>0.0001</length>
          </cylinder>
         </geometry>
       </collision>
       <visual name='visual'>
         <geometry>
          <cylinder>
            <radius>0.125</radius>
            <length>0.0001</length>
          </cylinder>
         </geometry>
         <material>
           <script>
             <name>Gazebo/{human[i][2].title()}</name>
             <uri>file://media/materials/scripts/gazebo.material</uri>
           </script>
         </material>
       </visual>
       <static>1</static>
     </link>
    </model>'''

print(xml_start+xml_end)
