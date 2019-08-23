from numpy import array, pi, arcsin, floor
# from numpy import add as np_add, array
# from pprint import pprint


class Configuration:
    def __init__(self):
        self.MAX_LENGTH = 2220  # mm
        self.MIN_LENGTH = 1120  # mm
        self.MAX_WIDTH = 1250  # mm
        self.MIN_WIDTH = 780  # mm
        self.RIGHT_CENTER_DIST = 160  # mm
        self.BOTTOM_CENTER_DIST = 160  # mm
        self.START_ANGLE = 33  # deg
        self.PANEL_STOP_LENGTH = 240  # mm
        self.STOP_TIP_RADIUS = 12.5  # mm
        self.STEP_ANGLE = 1.8  # degrees
        SCREW_STARTS = 4  # no units
        SCREW_PITCH = 2  # mm
        self.SCREW_LEAD = SCREW_STARTS*SCREW_PITCH  # mm
        self.REDUCER_RATIO = 1  # no units

    def absorber_dimensions(self, values):
        if not values['is_horizontal']:
            length = values['head_to_head'] + values['header_diameter']
            width = values['panel_width'] + 2*values['header_exit_length']
        else:
            length = values['panel_length']+2*values['header_exit_length']
            width = values['head_to_head'] + values['header_diameter']

        dimensions = {
            'grid_length': length,
            'grid_width': width,
            'panel_length': values['panel_length'],
            'panel_width': values['panel_width'],
            'header_exit_length': values['header_exit_length'],
            'is_horizontal': values['is_horizontal']
        }

        return dimensions

    def vert_bar_steps(self, dimensions, offsets):
        # calculate vertical bar's steppers' steps
        distance = motor_rots = motor_steps = array([0, 0])

        distance = self.MAX_WIDTH + offsets - dimensions['grid_width']
        motor_rots = distance/self.SCREW_LEAD  # calculate rotations
        motor_steps = floor(motor_rots*360/self.STEP_ANGLE)  # steps
        return motor_steps.tolist()

    def horiz_bar_steps(self, dimensions, offsets):
        # calculate horizontal bar's steppers' steps
        distance = motor_rots = motor_steps = array([0, 0])

        distance = self.MAX_LENGTH + offsets - dimensions['grid_length']
        motor_rots = distance/self.SCREW_LEAD
        motor_steps = floor(motor_rots*360/self.STEP_ANGLE)
        return motor_steps.tolist()

    def vert_panel_steps(self, dimensions, offsets):
        # calculate vertical (right) panel side's steppers' steps
        motor_angle = motor_steps = array([0, 0])

        if not dimensions['is_horizontal']:
            distance = (self.RIGHT_CENTER_DIST - self.STOP_TIP_RADIUS +
                        dimensions['header_exit_length'])
        else:
            distance = (self.RIGHT_CENTER_DIST - self.STOP_TIP_RADIUS -
                        (dimensions['panel_width'] -
                         dimensions['grid_width'])/2)

        theta = arcsin(distance/self.PANEL_STOP_LENGTH)*360/(2*pi)
        motor_angle = theta - self.START_ANGLE - offsets  # radians
        motor_steps = floor(motor_angle/self.STEP_ANGLE)
        return motor_steps.tolist()

    def horiz_panel_steps(self, dimensions, offsets):
        # calculate horizontal (bottom) panel side's steppers' steps
        motor_angle = motor_steps = array([0, 0])

        if not dimensions['is_horizontal']:
            distance = (self.BOTTOM_CENTER_DIST - self.STOP_TIP_RADIUS -
                        (dimensions['panel_length'] -
                         dimensions['grid_length'])/2)
        else:
            distance = (self.BOTTOM_CENTER_DIST - self.STOP_TIP_RADIUS +
                        dimensions['header_exit_length'])

        theta = arcsin(distance/self.PANEL_STOP_LENGTH)*360/(2*pi)
        motor_angle = theta - self.START_ANGLE - offsets  # radians
        motor_steps = floor(motor_angle/self.STEP_ANGLE)
        return motor_steps.tolist()

    def stepper_steps(self, dimensions, offsets):
        steps = []
        offsets = array(list(offsets.values()))
        steps.extend(self.vert_bar_steps(dimensions, offsets[0:2]))
        steps.extend(self.horiz_bar_steps(dimensions, offsets[2:4]))
        steps.extend(self.vert_panel_steps(dimensions, offsets[4:6]))
        steps.extend(self.horiz_panel_steps(dimensions, offsets[6:8]))

        return steps

    def make(self, values, offsets, file_path):
        # calculate and export steps to file
        dimensions = self.absorber_dimensions(values)
        steps = self.stepper_steps(dimensions, offsets)

        with open(file_path, 'w', encoding='utf-8') as the_file:
            the_file.write('# steppers\' steps (1 step = 1.8 deg)\n')
            for i in range(len(steps)):
                the_file.write('motor_'+str(i)+': '+str(steps[i])+'\n')
