import sys
from os import environ, path
from configuration_utils import Configuration
from file_utils import FileManager

# from pprint import pprint

if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg


class Gui:
    def __init__(self):
        LCOL_WIDTH = 16
        FRAME_LCOL_WIDTH = 13
        OFFSETS_LCOL_WIDTH = 11
        TB_WID = 8
        self.was_horizontal = False

        HOMEPATH = 'C:' + environ['HOMEPATH']
        if getattr(sys, 'frozen', False):
            CURRENT_DIR = path.dirname(path.realpath(sys.executable))
        elif __file__:
            CURRENT_DIR = path.dirname(path.realpath(__file__))
        self.guessed_name = 'configuration'
        self.default_output_folder = HOMEPATH + '\\'
        self.output_file = (self.default_output_folder +
                            self.guessed_name + '.dat')
        self.input_file = self.output_file
        self.OLDS_DIR = 'old'
        self.OFFSETS_FILE = CURRENT_DIR + '\\offsets.cfg'
        self.OFFSETS_FILE_EXISTS = path.isfile(self.OFFSETS_FILE)
        self.CONFIG_FILE = CURRENT_DIR + '\\configuration.txt'

        # machine default offsets
        self.default_offsets = {
            'motor_1': 0,
            'motor_2': 0,
            'motor_3': 0,
            'motor_4': 0,
            'motor_5': 0,
            'motor_6': 0,
            'motor_7': 0,
            'motor_8': 0
        }

        # offsets in use
        self.offsets = self.default_offsets.copy()

        # visual options
        sg.SetOptions(
            icon=None,
            button_color=(None, None),
            element_size=(None, None),
            margins=(None, None),
            element_padding=(None, None),
            auto_size_text=None,
            auto_size_buttons=None,
            font=None,
            border_width=None,
            slider_border_width=None,
            slider_relief=None,
            slider_orientation=None,
            autoclose_time=None,
            message_box_line_width=None,
            progress_meter_border_depth=None,
            progress_meter_style=None,
            progress_meter_relief=None,
            progress_meter_color=None,
            progress_meter_size=None,
            text_justification=None,
            background_color=None,
            element_background_color=None,
            text_element_background_color=None,
            input_elements_background_color=None,
            scrollbar_color=None, text_color=None,
            debug_win_size=(None, None),
            window_location=(None, None)
        )

        # define main window layout
        self.layout = [
            # absobrber info
            [sg.Text("Κωδικός συλλέκτη:",
             size=(14, 1),
             auto_size_text=False,
             justification='right')],
            [sg.InputText(do_not_clear=True, size=(30, 1),
                          enable_events=True, key='absorber_info')],

            # is horizontal absorber
            [sg.Checkbox("Οριζόντιος", default=False,
             enable_events=True,
             key='is_horizontal')],

            # panel/strips section
            [sg.Frame("Χαρακτηριστικά συλλέκτη " + '(mm)', layout=[
                # header diameter
                [sg.Text("Φ κολεκτέρ", size=(FRAME_LCOL_WIDTH, 1),
                 auto_size_text=False,
                 justification='right'),
                 sg.InputText('22', do_not_clear=True, size=(TB_WID, 1),
                 enable_events=True,
                 key='header_diameter')],

                # head to head distance
                [sg.Text("Κέντρο-κέντρο", size=(FRAME_LCOL_WIDTH, 1),
                 auto_size_text=False,
                 justification='right'),
                 sg.InputText(do_not_clear=True, size=(TB_WID, 1),
                 enable_events=True,
                 key='head_to_head')],

                # free header exit length
                [sg.Text("Μήκος ελεύθερης " + '\n' + "εξόδου κολεκτέρ",
                 size=(FRAME_LCOL_WIDTH, 2),
                 auto_size_text=False,
                 justification='right'),
                 sg.InputText(do_not_clear=True, size=(TB_WID, 1),
                 enable_events=True,
                 key='header_exit_length')],

                # panel width
                [sg.Text("Πλάτος φύλλου",
                 size=(FRAME_LCOL_WIDTH, 1),
                 auto_size_text=False,
                 justification='right'),
                 sg.InputText(do_not_clear=True, size=(TB_WID, 1),
                 enable_events=True,
                 key='panel_width')],

                # panel width
                [sg.Text("Μήκος φύλλου",
                 size=(FRAME_LCOL_WIDTH, 1),
                 auto_size_text=False,
                 justification='right'),
                 sg.InputText(do_not_clear=True, size=(TB_WID, 1),
                 enable_events=True,
                 key='panel_length')]
             ])],

            # error box
            [sg.Text('', text_color='red', size=(27, 3),
                     key='error_box')],

            # buttons
            [sg.Text(' ' * 3),
             sg.Button("Αποστολή", size=(9, 1), key='send_button'),
             sg.Button("Αποθήκευση", size=(9, 1), key='save_button')],
            [sg.Text(' ' * 3),
             sg.Button('Offsets', size=(9, 1), key='offsets_button'),
             sg.Button("Φόρτωση", size=(9, 1), key='load_button')]
        ]

        # define machine offsets window layout
        self.offsets_layout = [
            [sg.Frame("Πλέγμα " + 'X', layout=[
                [sg.Text("Μοτέρ 1 (mm)", size=(OFFSETS_LCOL_WIDTH, 1),
                 auto_size_text=False,
                 justification='right'),
                 sg.InputText('', do_not_clear=True, size=(6, 1),
                 enable_events=True,
                 key='motor_1')],
                [sg.Text("Μοτέρ 2 (mm)", size=(OFFSETS_LCOL_WIDTH, 1),
                 auto_size_text=False,
                 justification='right'),
                 sg.InputText('', do_not_clear=True, size=(6, 1),
                 enable_events=True,
                 key='motor_2')]
            ])],
            [sg.Frame("Πλέγμα " + 'Y', layout=[
                [sg.Text("Μοτέρ 3 (mm)", size=(OFFSETS_LCOL_WIDTH, 1),
                 auto_size_text=False,
                 justification='right'),
                 sg.InputText('', do_not_clear=True, size=(6, 1),
                 enable_events=True,
                 key='motor_3')],
                [sg.Text("Μοτέρ 4 (mm)", size=(OFFSETS_LCOL_WIDTH, 1),
                 auto_size_text=False,
                 justification='right'),
                 sg.InputText('', do_not_clear=True, size=(6, 1),
                 enable_events=True,
                 key='motor_4')]
            ])],
            [sg.Frame("Φύλλο X", layout=[
                [sg.Text("Μοτέρ 5 (deg)", size=(OFFSETS_LCOL_WIDTH, 1),
                 auto_size_text=False,
                 justification='right'),
                 sg.InputText('', do_not_clear=True, size=(6, 1),
                 enable_events=True,
                 key='motor_5')],
                [sg.Text("Μοτέρ 6 (deg)", size=(OFFSETS_LCOL_WIDTH, 1),
                 auto_size_text=False,
                 justification='right'),
                 sg.InputText('', do_not_clear=True, size=(6, 1),
                 enable_events=True,
                 key='motor_6')]
            ])],
            [sg.Frame("Φύλλο Y", layout=[
                [sg.Text("Μοτέρ 7 (deg)", size=(OFFSETS_LCOL_WIDTH, 1),
                 auto_size_text=False,
                 justification='right'),
                 sg.InputText('', do_not_clear=True, size=(6, 1),
                 enable_events=True,
                 key='motor_7')],
                [sg.Text("Μοτέρ 8 (deg)", size=(OFFSETS_LCOL_WIDTH, 1),
                 auto_size_text=False,
                 justification='right'),
                 sg.InputText('', do_not_clear=True, size=(6, 1),
                 enable_events=True,
                 key='motor_8')]
            ])],

            # error box
            # [sg.Text('', text_color='red', size=(20, 3),
            #          key='offsets_error_box')],

            # buttons
            [sg.Button('OK', size=(10, 1),
                       key='OK_button'),
             sg.Button("Επαναφορά", size=(10, 1),
                       key='reset_button')]
        ]

        # configuration instance
        self.configuration = Configuration()

        # file manager instance
        self.file_manager = FileManager()

    def is_positive_float(self, string):
        try:
            if float(string) > 0.0:
                return True
            else:
                return False
        except ValueError:
            return False

    def is_float(self, string):
        try:
            a = float(string)
        except ValueError:
            return False
        else:
            return True

    def check_for_errors(self, values):
        # check for positive floats
        try:
            for key in values.keys():
                # skip absorber info
                if key in ('absorber_info'):
                    continue

                if type(values[key]) == str:
                    if not self.is_positive_float(values[key]):
                        return "Σφάλμα: επιτρέπονται μόνο θετικοί αριθμοί"
        except AttributeError:
            return "Σφαλμα: μη έγκυρη τιμή"

        size_error = False
        dimension = ''
        comparison = ''

        # check head-to-head+header diameter and fixture length or width
        if not values['is_horizontal']:
            effective_length = (values['head_to_head'] +
                                values['header_diameter'])
            effective_width = (values['panel_width'] +
                               2*values['header_exit_length'])
        else:
            effective_length = (values['panel_length'] +
                                2*values['header_exit_length'])
            effective_width = (values['head_to_head'] +
                               values['header_diameter'])

        if (effective_width > self.configuration.MAX_WIDTH):
            size_error = True
            dimension = "πλάτος"
            comparison = "μεγαλύτερο"
        elif (effective_width < self.configuration.MIN_WIDTH):
            size_error = True
            dimension = "πλάτος"
            comparison = "μικρότερο"

        if (effective_length > self.configuration.MAX_LENGTH):
            size_error = True
            dimension = "μήκος"
            comparison = "μεγαλύτερο"
        elif (effective_length < self.configuration.MIN_LENGTH):
            size_error = True
            dimension = "μήκος"
            comparison = "μικρότερο"

        if size_error:
            return ("Σφάλμα: το " + dimension + " του συλλέκτη είναι "
                    + comparison + " από αυτό που εξυπηρετεί η διάταξη.")

        return ''

    def check_offsets_for_errors(self, values):
        # check for positive floats
        try:
            for key in values.keys():
                if type(values[key]) == str:
                    if not self.is_float(values[key]):
                        return ("Σφάλμα: επιτρέπονται μόνο θετικοί "
                                "αριθμοί " + values[key])
        except AttributeError:
            return "Σφαλμα: μη έγκυρη τιμή"

        return ''

    def show_error(self, error):
        self.window.Element('error_box').Update(error)

    def show_offsets_error(self, error):
        # self.offsets_window.Element('offsets_error_box').Update(error)
        pass

    def export_configuration_to_file(self, values, file_path):
        with open(file_path, 'w', encoding='utf-8') as the_file:
            for key in values.keys():
                # write separators
                if key == 'header_diameter':
                    the_file.write(
                            '#' + " Διάμετρος κολεκτέρ " + '(mm)\n'
                    )
                elif key == 'head_to_head':
                    the_file.write(
                        '#' + " Απόσταση κέντρο-κέντρο " + '(mm)\n'
                    )
                elif key == 'header_exit_length':
                    the_file.write(
                        '#' +" Μήκος ελεύθερης εξόδου " + 'header (mm)\n'
                    )
                elif key == 'panel_width':
                    the_file.write(
                        '#' + " Πλάτος φύλλου " + '(mm)\n'
                    )
                elif key == 'panel_lenth':
                    the_file.write(
                        '#' + " Μήκος φύλλου " + '(mm)\n'
                    )
                the_file.write(key + '=' + str(values[key]) + '\n\n')

        self.show_error("Οι ρυθμίσεις αποθηκεύτηκαν στο "
                        "αρχείο:" + '\n' + self.output_file)

    def import_configuration_from_file(self, values, file_path):
        if path.isfile(file_path):
            with open(file_path, encoding='utf-8') as the_file:
                for line in the_file:
                    # skip comment lines
                    if line.startswith('#'):
                        continue
                    # store appropriate
                    for key in values.keys():
                        if line.startswith(key + '='):
                            values[key] = line.strip('\n').split('=')[1]
                            if key == 'is_horizontal':
                                values[key] = values[key] == 'true'
                            self.window.Element(key).Update(values[key])

        self.show_error("Οι ρυθμίσεις φορτώθηκαν από το αρχείο:" + '\n' +
                        file_path)

    def export_offsets_to_file(self):
        with open(self.OFFSETS_FILE, 'w', encoding='utf-8') as the_file:
            # write separators
            for key in self.offsets.keys():
                the_file.write(key+'=' + str(self.offsets[key]) + '\n')

    def import_offsets_from_file(self):
        # reset imported offsets to defaults
        imported_offsets = self.default_offsets.copy()

        # if custom offsets file is present in current directory then
        # import these offsets
        if path.isfile(self.OFFSETS_FILE):
            with open(self.OFFSETS_FILE, encoding='utf-8') as the_file:
                for line in the_file:
                    # skip comment lines
                    if line.startswith('#'):
                        continue
                    # store appropriate
                    for key in self.offsets.keys():
                        if line.startswith(key + '='):
                            imported_offsets[key] = float(
                                    line.strip('\n').split('=')[1]
                            )

            self.show_offsets_error("Τα "+'offsets'+"φορτώθηκαν από το "
                                    "αρχείο:" + '\n' + self.OFFSETS_FILE)

        return imported_offsets

    def fill_offsets_window(self):
        imported_offsets = self.import_offsets_from_file()

        for key in self.offsets.keys():
            self.offsets_window.Element(key).Update(imported_offsets[key])

    def run_offsets_window(self):
        # draw offsets window
        self.offsets_window = (sg.Window('Offsets',
                               keep_on_top=True)
                               .Layout(self.offsets_layout))
        self.offsets_window.Finalize()

        # initialize offsets
        self.fill_offsets_window()

        # offsets window event Loop
        while True:
            # get the event and current values
            event, values = self.offsets_window.Read()

            # user closes the window
            if event is None:
                break

            # format values
            for key, val in values.items():
                if self.is_positive_float(val):
                    values[key] = float(val)

            # check for errors in any event except 'reset', 'X', or 'OK'
            if event not in (None, 'reset_button'):
                self.show_offsets_error('')
                error_found = self.check_offsets_for_errors(values)
                if error_found != '':
                    self.show_offsets_error(error_found)
                    print(error_found)
                    continue

            # user presses 'OK button'
            if event == 'OK_button':
                self.export_offsets_to_file()

                self.show_offsets_error(
                        ("Τα "+'offsets'+" αποθηκεύτηκαν στο αρχείο:" +
                        '\n' + self.OFFSETS_FILE)
                )

                break

            # user presses 'reset' button
            if event == 'reset_button':
                self.fill_offsets_window()

            # if user modifies a value then store it
            if event in self.offsets.keys():
                self.offsets[event] = values[event]

            # DEBUG
            # print('\noffsets event: ')
            # pprint(event)
            # print('\noffsets values: ')
            # pprint(values)

        self.offsets_window.Close()

    def run(self):
        # draw main window
        self.window = sg.Window("Ρύθμιση Διάταξης").Layout(self.layout)

        # main window vent Loop
        while True:
            # get the event and current values
            event, values = self.window.Read()

            # set offsets
            self.offsets = self.import_offsets_from_file()

            # user closes the window
            if event is None:
                break

            # format values
            for key, val in values.items():
                if key not in ('absorber_info', 'is_horizontal'):
                    if self.is_positive_float(val):
                        values[key] = float(val)

            # check for errors in any event except 'reset', 'X', or 'OK'
            if event not in (None, 'load_button', 'offsets_button',
                             'save_button', 'absorber_info'):
                self.show_error('')
                error_found = self.check_for_errors(values)
                if error_found != '':
                    self.show_error(error_found)
                    continue

            # user presses 'save button'
            if event == 'save_button':
                self.show_error('')
                error_found = self.check_for_errors(values)
                if error_found != '':
                    self.show_error(error_found)
                    continue

                # disable buttons
                self.window.Element('save_button').Update(disabled=True)
                self.window.Element('send_button').Update(disabled=True)
                self.window.Element('load_button').Update(disabled=True)
                (self.window.Element('offsets_button')
                 .Update(disabled=True))

                # prompt user to supply file name
                self.output_file = sg.PopupGetFile(
                    title="Αποθήκευση ρυθμήσεων",
                    message=("Παρακαλώ εισάγετε την τοποθεσία του "
                             "παραγόμενου αρχείου"),
                    save_as=True,
                    default_path=(self.default_output_folder +
                                  self.guessed_name + '.dat'),
                    default_extension='dat',
                    file_types=(("Αρχείο ρυθμίσεων", '*.dat'),)
                )

                # if a name is defined then proceed to save
                if self.output_file:
                    # ensure correct file extension
                    if not self.output_file.endswith('.dat'):
                        self.output_file += '.dat'

                    # clean up save directory
                    files_were_moved = self.file_manager.prepare_dir(
                        path.basename(self.output_file),
                        path.dirname(self.output_file),
                        self.OLDS_DIR)

                    if files_were_moved:
                        pass

                    # create configuration DAT
                    self.export_configuration_to_file(
                            values, self.output_file
                    )

                # re-enable buttons
                self.window.Element('save_button').Update(disabled=False)
                self.window.Element('send_button').Update(disabled=False)
                self.window.Element('load_button').Update(disabled=False)
                (self.window.Element('offsets_button')
                 .Update(disabled=False))

            # user presses 'load button'
            if event == 'load_button':
                # disable buttons
                self.window.Element('save_button').Update(disabled=True)
                self.window.Element('send_button').Update(disabled=True)
                self.window.Element('load_button').Update(disabled=True)
                (self.window.Element('offsets_button')
                 .Update(disabled=True))

                # prompt user to supply file name
                self.input_file = sg.PopupGetFile(
                    title="Φόρτωση ρυθμήσεων",
                    message=("Παρακαλώ εισάγετε την τοποθεσία του "
                             "αρχείου προς φόρτωση"),
                    save_as=False,
                    default_path=(self.default_output_folder),
                    default_extension='dat',
                    file_types=(("Αρχείο ρυθμίσεων", '*.dat'),)
                )

                # if a name is defined then proceed to load
                if self.input_file:
                    # ensure correct file extension
                    if self.input_file.endswith('.dat'):
                        self.import_configuration_from_file(
                            values,
                            self.input_file
                        )
                    else:
                        self.show_error("Μη συμβατό αρχείο προς φόρτωση.")

                # re-enable buttons
                self.window.Element('save_button').Update(disabled=False)
                self.window.Element('send_button').Update(disabled=False)
                self.window.Element('load_button').Update(disabled=False)
                (self.window.Element('offsets_button')
                 .Update(disabled=False))

            # user presses 'offsets' button
            if event == 'offsets_button':
                # disable buttons
                self.window.Element('save_button').Update(disabled=True)
                self.window.Element('send_button').Update(disabled=True)
                self.window.Element('load_button').Update(disabled=True)
                (self.window.Element('offsets_button')
                 .Update(disabled=True))

                # open offsets window
                self.run_offsets_window()

                # re-enable buttons
                self.window.Element('save_button').Update(disabled=False)
                self.window.Element('send_button').Update(disabled=False)
                self.window.Element('load_button').Update(disabled=False)
                (self.window.Element('offsets_button')
                 .Update(disabled=False))

            # user presses 'send button'
            if event == 'send_button':
                # disable buttons
                self.window.Element('save_button').Update(disabled=True)
                self.window.Element('send_button').Update(disabled=True)
                self.window.Element('load_button').Update(disabled=True)
                (self.window.Element('offsets_button')
                 .Update(disabled=True))

                # make configuration
                self.configuration.make(values, self.offsets,
                                        self.CONFIG_FILE)

                # re-enable buttons
                self.window.Element('save_button').Update(disabled=False)
                self.window.Element('send_button').Update(disabled=False)
                self.window.Element('load_button').Update(disabled=False)
                (self.window.Element('offsets_button')
                 .Update(disabled=False))

            # set possible file name and set panel material
            if event == 'absorber_info':
                # format name
                guessed_name = (values['absorber_info']
                                .split('\n')[0]
                                .strip(',|.| |\t'))

                # format guessed name and drawing number
                for char in ['/', '\\', '|', '*']:
                    guessed_name = guessed_name.replace(char, '-')

                for char in ['\t', ':', '?', '<', '>']:
                    guessed_name = guessed_name.replace(char, '')

                if guessed_name != '':
                    self.guessed_name = guessed_name

            # DEBUG
            # print('\nevent: ')
            # pprint(event)
            # print('\nvalues: ')
            # pprint(values)

        self.window.Close()
