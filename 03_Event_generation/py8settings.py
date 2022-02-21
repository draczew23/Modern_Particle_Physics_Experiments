#PP: file obtained from https://indico.bnl.gov/event/9153/sessions/3928/
import os, sys
from ipywidgets import interact, Layout
import ipywidgets as wgs

def find_dir(name, path='/usr/share/'):
    for root, dirs, files in os.walk(path):
        if name in dirs:
            return os.path.join(root, name)
    return ''

def find_procs():
    all_procs  = []
    xml_dir    = find_dir('xmldoc')
    if xml_dir == '': return all_procs
    idx_file   = open(xml_dir+'/Index.xml', 'r')
    proc_files = []
    # Find all files to look for processes.
    for line in idx_file:
        if 'Processes' in line:
            if 'ProcessSelection' in line :
                continue
            if 'Interfaces to External' in line :
                break
            if 'button' in line :
                break
            frst, scnd = line.find('href='), line.find('>')
            proc_files.append(xml_dir+'/'+line[frst+6:scnd-1]+'.xml')
    idx_file.close()
    # Search the files for processes.
    for proc_file in proc_files:
        proc_file = open(proc_file, 'r')
        for line in proc_file:
            frst, scnd = line.find('flag name='), line.find(' default')
            if frst > 0 and scnd > 0:
                all_procs.append(line[frst+11:scnd-1])
        proc_file.close()
    proc_classes = {}
    # Sort into process classes.
    excl_classes = ['SigmaProcess', 'Higgs']
    for proc in all_procs:
        proc_name  = proc[proc.find(':'):]
        if 'all' in proc_name or '2' in proc_name:
            proc_class = proc[:proc.find(':')]
            if proc_class not in proc_classes:
                if proc_class not in excl_classes:
                    proc_classes[proc_class] = []
    for proc in all_procs:
        proc_name  = proc[proc.find(':'):]
        if 'all' in proc_name or '2' in proc_name:
            proc_class = proc[:proc.find(':')]
            if proc_class in proc_classes:
                if proc not in proc_classes[proc_class]:
                    proc_classes[proc_class].append(proc)
    return proc_classes

def write_pythia_settings(pythia, settings, values, all_procs_list = []):
    if isinstance(pythia, str):
        #cmnd_file = open(pythia, "a+")
        cmnd_file = open(pythia, 'r')
        new_stngs = ''
        for line in cmnd_file:
            append = True
            for i in range(len(all_procs_list)):
                if all_procs_list[i] in line:
                    append = False
                    break
            if append:
                for i in range(len(values)):
                    if settings[i] in line:
                        append = False
                        break
            if append:
                new_stngs += line
        cmnd_file.close()
        for i in range(len(values)):
            new_stngs += (settings[i]+' = '+str(values[i])+'\n')
        cmnd_file = open(pythia, 'w')
        cmnd_file.write(new_stngs)
        cmnd_file.close()
    else:
        # Switch off all processes to be safe.
        for i in range(len(all_procs_list)):
            pythia.readString(all_procs_list[i]+' = off')
        for i in range(len(values)):
            pythia.readString(settings[i]+' = '+str(values[i]))

def beam_settings(pythia):
    # Setup the options for the menus.
    beam_ids       = ['p', 'pbar', 'n', 'nbar', 'pi+', 'pi-', 'pi0', \
                      'Pomeron', 'gamma', 'e-', 'e+', 'mu-', 'mu+']
    id_convert     = {'p': 2212, 'pbar': -2212, 'n': 2112, \
                      'nbar': -2112, 'pi+': 211, 'pi-': -211, 'pi0': 111, \
                      'Pomeron': 990, 'gamma': 22, 'e-': 11, 'e+': -11, \
                      'mu-': 13, 'mu+': -13}
    frame_types    = ['1: beams collide in CM frame, set Beams:eCM', \
                      '2: back-to-back beams with different energies, set Beams:eA and Beams:eB', \
                      '3: not back-to-back beams, set Beams:pxA through Beams:pzB', \
                      '4: Les Houches Event File input, set Beams:LHEF below']
    types_convert  = {frame_types[0] : 1, frame_types[1] : 2, \
                      frame_types[2] : 3, frame_types[3] : 4}
    style          = {'description_width': 'initial'}
    layout         = Layout(width='750px')
    message        = 'You can now set the parameters for the incoming beams:'
    settings       = []
    # Setup the menus.
    settings.append('Beams:idA')
    w_idA    = wgs.Dropdown(options=beam_ids, value='e-', \
                            description='beam A id  ['+settings[-1]+']', \
                            style=style, layout=layout)
    settings.append('Beams:idB')
    w_idB    = wgs.Dropdown(options=beam_ids, value='p', \
                            description='beam B id  ['+settings[-1]+']', \
                            style=style, layout=layout)
    settings.append('Beams:frameType')
    w_frame  = wgs.Dropdown(options=frame_types, value=frame_types[1], \
                            description='beam frame type  ['+settings[-1]+']', \
                            style=style, layout=layout)
    settings.append('Beams:eCM')
    w_eCM    = wgs.FloatText(value=14000.0, \
                             description='CMS energy for Beams:frameType = 1' \
                                         '  ['+settings[-1]+']', \
                             style=style, layout=layout, disabled=False)
    settings.append('Beams:eA')
    w_eA     = wgs.FloatText(value=27.5, \
                             description='beam A energy for Beams:frameType = 2' \
                                         '  ['+settings[-1]+']', \
                             style=style, layout=layout, disabled=False)
    settings.append('Beams:eB')
    w_eB     = wgs.FloatText(value=820.0, \
                             description='beam B energy for Beams:frameType = 2' \
                                         '  ['+settings[-1]+']', \
                             style=style, layout=layout, disabled=False)
    settings.append('Beams:pxA')
    w_pxA    = wgs.FloatText(value=0.0, \
                             description='beam A x-momentum for Beams:frameType = 3' \
                                         '  ['+settings[-1]+']', \
                             style=style, layout=layout, disabled=False)
    settings.append('Beams:pyA')
    w_pyA    = wgs.FloatText(value=0.0, \
                             description='beam A y-momentum for Beams:frameType = 3' \
                                         '  ['+settings[-1]+']', \
                             style=style, layout=layout, disabled=False)
    settings.append('Beams:pzA')
    w_pzA    = wgs.FloatText(value=7000.0, \
                             description='beam A z-momentum for Beams:frameType = 3' \
                                         '  ['+settings[-1]+']', \
                             style=style, layout=layout, disabled=False)
    settings.append('Beams:pxB')
    w_pxB    = wgs.FloatText(value=0.0, \
                             description='beam B x-momentum for Beams:frameType = 3' \
                                         '  ['+settings[-1]+']', \
                             style=style, layout=layout, disabled=False)
    settings.append('Beams:pyB')
    w_pyB    = wgs.FloatText(value=0.0, \
                             description='beam B y-momentum for Beams:frameType = 3' \
                                         '  ['+settings[-1]+']', \
                             style=style, layout=layout, disabled=False)
    settings.append('Beams:pzB')
    w_pzB    = wgs.FloatText(value=-7000.0, \
                             description='beam B z-momentum for Beams:frameType = 3' \
                                         '  ['+settings[-1]+']', \
                             style=style, layout=layout, disabled=False)
    settings.append('Beams:LHEF')
    w_lhef   = wgs.Text(value='void', placeholder='Type something', \
                        description='name of Les Houches Event File for Beams:frameType = 4' \
                                         '  ['+settings[-1]+']', \
                        style=style, layout=layout, disabled=False)
    def apply_pythia_settings(idA, idB, frame, eCM, eA, eB, pxA, pyA, pzA, \
                              pxB, pyB, pzB, lhef):
        values       = [id_convert[idA], id_convert[idB], types_convert[frame], \
                        eCM, eA, eB, pxA, pyA, pzA, pxB, pyB, pzB, lhef]
        write_pythia_settings(pythia, settings, values)
    print (message)
    interact(apply_pythia_settings, idA = w_idA, idB = w_idB, frame = w_frame, \
             eCM = w_eCM, eA = w_eA, eB = w_eB, pxA = w_pxA, pyA = w_pyA, \
             pzA = w_pzA, pxB = w_pxB, pyB = w_pyB, pzB = w_pzB, lhef = w_lhef)

def basic_settings(pythia):
    # Setup the options for the process selection.
    all_procs      = find_procs()
    all_procs_list = []
    for proc_class in all_procs.keys():
        all_procs_list += all_procs[proc_class]
    base_proc      = 'WeakBosonExchange'
    base_sproc     = 'WeakBosonExchange:all'
    style          = {'description_width': 'initial'}
    layout         = Layout(width='750px')
    message        = 'You can now select the number of events, settings ' \
                     + 'for the random seed, and processes:'
    settings       = []
    # Setup the menus.
    settings.append('Main:numberOfEvents')
    w_nEvt   = wgs.IntText(value=100, description='# of events  ['+settings[-1]+']', \
                           style=style, layout=layout, disabled=False)
    settings.append('Random:setSeed')
    w_rndm   = wgs.Checkbox(value=False, description='allow user random seed  ['+settings[-1]+']', \
                            style=style, layout=layout, disabled=False)
    settings.append('Random:seed')
    w_rndms  = wgs.IntText(value=-1, description='user random see number (max=900000000)  ['+settings[-2]+']', \
                           style=style, layout=layout, disabled=False)
    w_bprocs = wgs.Select(options=sorted(all_procs.keys()), value=base_proc, \
                          rows=4, description='Process Class', \
                          style=style, layout=layout, disabled=False)
    w_sprocs = wgs.SelectMultiple(options=all_procs[base_proc], \
                                  value=[base_sproc], \
                                  rows=4, description='Processes', \
                                  style=style, layout=layout, disabled=False)
    def update_sprocs_options(*args):
        w_sprocs.options = all_procs[w_bprocs.value]
    w_bprocs.observe(update_sprocs_options, 'value')
    def apply_pythia_settings(nEvt, rndm, rndms, bprocs, sprocs):
        values       = [nEvt, rndm, rndms]
        if values[1]: values[1] = 'on'
        else: values[1] = 'off'
        all_settings = []
        for i in range(len(settings)):
            all_settings.append(settings[i])
        for proc in sprocs:
            all_settings.append(proc)
            values.append('on')
        write_pythia_settings(pythia, all_settings, values, all_procs_list)
    print (message)
    interact(apply_pythia_settings, nEvt = w_nEvt, rndm = w_rndm, \
             rndms = w_rndms, bprocs = w_bprocs, sprocs = w_sprocs)

def onoff_settings(pythia):
    # Setup the checkboxes.
    style              = {'description_width': 'initial'}
    layout             = Layout(width='500px')
    message            = 'You can switch on/off different parts of the simulation:'
    settings, selectrs = [], []
    settings.append('PartonLevel:MPI')
    selectrs.append(wgs.Checkbox(value=True, description='multi-parton interactions  ['+settings[-1]+']', \
                                 style=style, layout=layout, disabled=False))
    settings.append('PartonLevel:ISR')
    selectrs.append(wgs.Checkbox(value=True, description='initial-state radiation  ['+settings[-1]+']', \
                                 style=style, layout=layout, disabled=False))
    settings.append('PartonLevel:FSR')
    selectrs.append(wgs.Checkbox(value=True, description='final-state radiation  ['+settings[-1]+']', \
                                 style=style, layout=layout, disabled=False))
    settings.append('PartonLevel:Remnants')
    selectrs.append(wgs.Checkbox(value=True, description='beam remnants  ['+settings[-1]+']', \
                                 style=style, layout=layout, disabled=False))
    settings.append('HadronLevel:all')
    selectrs.append(wgs.Checkbox(value=True, description='hadronization  ['+settings[-1]+']', \
                                 style=style, layout=layout, disabled=False))
    def apply_pythia_settings(s1, s2, s3, s4, s5):
        values = [s1, s2, s3, s4, s5]
        for i in range(len(values)):
            if values[i]: values[i] = 'on'
            else: values[i] = 'off'
        write_pythia_settings(pythia, settings, values)
    print (message)
    interact(apply_pythia_settings, s1 = selectrs[0], s2 = selectrs[1], \
             s3 = selectrs[2], s4 = selectrs[3], s5 = selectrs[4])

def pscuts_settings(pythia, n_finalstate):
    # Setup the selecters.
    style              = {'description_width': 'initial'}
    layout             = Layout(width='750px')
    message            = 'You can now select the phase-space cuts for ' \
                         + str(n_finalstate) + ' final-state particles:'
    settings, selectrs = [], []
    settings.append('PhaseSpace:mHatMin')
    selectrs.append(wgs.FloatText(value=4.0, description='minimum invariant mass in GeV'
                                                         '  ['+settings[-1]+']', \
                                  style=style, layout=layout, disabled=False))
    settings.append('PhaseSpace:mHatMax')
    selectrs.append(wgs.FloatText(value=-1.0, description='maximum invariant mass in GeV'
                                                          '  ['+settings[-1]+']', \
                                  style=style, layout=layout, disabled=False))
    if n_finalstate == 2:
        settings.append('PhaseSpace:pTHatMin')
        selectrs.append(wgs.FloatText(value=1.0, description='minimum invariant pT in GeV'
                                                             '  ['+settings[-1]+']', \
                                      style=style, layout=layout, disabled=False))
        settings.append('PhaseSpace:pTHatMax')
        selectrs.append(wgs.FloatText(value=-1.0, description='maximum invariant pT in GeV'
                                                              '  ['+settings[-1]+']', \
                                      style=style, layout=layout, disabled=False))
        settings.append('PhaseSpace:Q2Min')
        selectrs.append(wgs.FloatText(value=1.0, description='minimum DIS variable Q^2 = - tHat in GeV^2'
                                                             '  ['+settings[-1]+']', \
                                      style=style, layout=layout, disabled=False))
    elif n_finalstate == 3:
        settings.append('PhaseSpace:pTHat3Min')
        selectrs.append(wgs.FloatText(value=0.0, description='minimum invariant pT in GeV for highest pT parton'
                                                             '  ['+settings[-1]+']', \
                                      style=style, layout=layout, disabled=False))
        settings.append('PhaseSpace:pTHat3Max')
        selectrs.append(wgs.FloatText(value=-1.0, description='maximum invariant pT in GeV for highest pT parton'
                                                             '  ['+settings[-1]+']', \
                                      style=style, layout=layout, disabled=False))
        settings.append('PhaseSpace:pTHat5Min')
        selectrs.append(wgs.FloatText(value=0.0, description='minimum invariant pT in GeV for lowest pT parton'
                                                             '  ['+settings[-1]+']', \
                                      style=style, layout=layout, disabled=False))
        settings.append('PhaseSpace:pTHat5Max')
        selectrs.append(wgs.FloatText(value=-1.0, description='maximum invariant pT in GeV for lowest pT parton'
                                                              '  ['+settings[-1]+']', \
                                      style=style, layout=layout, disabled=False))
    def apply_pythia_settings_two(s1, s2):
        values = [s1, s2]
        write_pythia_settings(pythia, settings, values)
    def apply_pythia_settings_five(s1, s2, s3, s4, s5):
        values = [s1, s2, s3, s4, s5]
        write_pythia_settings(pythia, settings, values)
    def apply_pythia_settings_six(s1, s2, s3, s4, s5, s6):
        values = [s1, s2, s3, s4, s5, s6]
        write_pythia_settings(pythia, settings, values)
    print (message)
    if n_finalstate == 2:
        interact(apply_pythia_settings_five, s1 = selectrs[0], s2 = selectrs[1], \
                 s3 = selectrs[2], s4 = selectrs[3], s5 = selectrs[4])
    elif n_finalstate == 3:
        interact(apply_pythia_settings_six, s1 = selectrs[0], s2 = selectrs[1], \
                 s3 = selectrs[2], s4 = selectrs[3], s5 = selectrs[4], \
                 s6 = selectrs[5])
    else:
        interact(apply_pythia_settings_two, s1 = selectrs[0], s2 = selectrs[1])

def shower_settings(pythia, dire_defaults=False):
    # Setup the selecters.
    style              = {'description_width': 'initial'}
    layout             = Layout(width='750px')
    message            = 'You can now set the main shower parameters:'
    defaults           = [ 0.1365, 0.5, 0.1365, 0.2 ]
    if dire_defaults:
        defaults       = [ 0.1201, 0.9, 0.1201, 0.9 ]
    settings, selectrs = [], []
    settings.append('TimeShower:alphaSvalue')
    selectrs.append(wgs.FloatText(value=defaults[0], \
                                  description='alphaS(m_Z) for final-state shower (0.06 - 0.25)'
                                              '  ['+settings[-1]+']', \
                                  style=style, layout=layout, disabled=False))
    settings.append('TimeShower:pTmin')
    selectrs.append(wgs.FloatText(value=defaults[1], \
                                  description='cutoff in pT/GeV for final-state shower (0.1 - 2.0)'
                                              '  ['+settings[-1]+']', \
                                  style=style, layout=layout, disabled=False))
    settings.append('SpaceShower:alphaSvalue')
    selectrs.append(wgs.FloatText(value=defaults[2], \
                                  description='alphaS(m_Z) for initial-state shower (0.06 - 0.25)'
                                              '  ['+settings[-1]+']', \
                                  style=style, layout=layout, disabled=False))
    settings.append('SpaceShower:pTmin')
    selectrs.append(wgs.FloatText(value=defaults[3], \
                                  description='cutoff in pT/GeV for initial-state shower (0.1 - 10.0)'
                                              '  ['+settings[-1]+']', \
                                  style=style, layout=layout, disabled=False))
    def apply_pythia_settings(s1, s2, s3, s4):
        values = [s1, s2, s3, s4]
        write_pythia_settings(pythia, settings, values)
    print (message)
    interact(apply_pythia_settings, s1 = selectrs[0], s2 = selectrs[1], \
             s3 = selectrs[2], s4 = selectrs[3])

def fragmentation_settings(pythia, dire_defaults=False):
    # Setup the selecters.
    style              = {'description_width': 'initial'}
    layout             = Layout(width='750px')
    message            = 'You can now set the main fragmentation parameters:'
    defaults           = [ 0.68, 0.98, 0.335, 0.217 ]
    if dire_defaults:
        defaults       = [ 0.9704, 1.0809, 0.2952, 0.2046 ]
    settings, selectrs = [], []
    settings.append('StringZ:aLund')
    selectrs.append(wgs.FloatText(value=defaults[0], \
                                  description='a parameter of the fragmentation function (0.0 - 2.0)'
                                              '  ['+settings[-1]+']', \
                                  style=style, layout=layout, disabled=False))
    settings.append('StringZ:bLund')
    selectrs.append(wgs.FloatText(value=defaults[1], \
                                  description='b parameter of the fragmentation function (0.2 - 2.0)'
                                              '  ['+settings[-1]+']', \
                                  style=style, layout=layout, disabled=False))
    settings.append('StringPT:sigma')
    selectrs.append(wgs.FloatText(value=defaults[2], \
                                  description='width sigma in GeV in the fragmentation (0.0 - 1.0)'
                                              '  ['+settings[-1]+']', \
                                  style=style, layout=layout, disabled=False))
    settings.append('StringFlav:probStoUD')
    selectrs.append(wgs.FloatText(value=defaults[3], \
                                  description='suppression of s quark production to u or d (0.0 - 1.0)'
                                              '  ['+settings[-1]+']', \
                                  style=style, layout=layout, disabled=False))
    def apply_pythia_settings(s1, s2, s3, s4):
        values = [s1, s2, s3, s4]
        write_pythia_settings(pythia, settings, values)
    print (message)
    interact(apply_pythia_settings, s1 = selectrs[0], s2 = selectrs[1], \
             s3 = selectrs[2], s4 = selectrs[3])

def more_settings(pythia, settings):
    cmnd_file = open(pythia, 'a')
    for i in range(len(settings)):
        cmnd_file.write(settings[i]+'\n')
    cmnd_file.close()

    
class PDF(object):
    def __init__(self, pdf, size=(200,200)):
        self.pdf = pdf
        self.size = size
    def _repr_html_(self):
        return '<iframe src={0} width={1[0]} height={1[1]}></iframe>'.format(self.pdf, self.size)
    def _repr_latex_(self):
        return r'\includegraphics[width=1.0\textwidth]{{{0}}}'.format(self.pdf)