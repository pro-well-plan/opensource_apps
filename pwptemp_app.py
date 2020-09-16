import streamlit as st
import well_profile as wp
import pwptemp.drilling as ptd
import pandas as pd


def add_pwptemp_app():
    st.subheader('Well Temperature APP')

    st.write("This is a web based application to generate well temperature distributions.")

    st.info('pwptemp is a python package for easy calculation of the temperature distribution along  \
             the well. New features are added as they are needed; '
            'suggestions and contributions of all kinds are very welcome.')

    st.markdown('[source code]'
                '(https://github.com/pro-well-plan/pwptemp)')

    st.markdown('[python package]'
                '(https://pypi.org/project/pwptemp/)')

    '''trajectory = load_trajectory()

    inputs = {'tin': 20,
              'q': 794.933,
              'rpm': 100,
              'tbit': 1.35,
              'wob': 22.41,
              'rop': 14.4,
              'an': 3100,
              'rhof': 1.2,
              'rhod': 7.8,
              'rhoc': 7.8,
              'rhor': 7.8,
              'rhow': 1.03,
              'rhocem': 2.7,
              'ddo': 4.5,
              'ddi': 4.0,
              'wd': 0,
              'dro': 21.0,
              'dri': 17.716,
              'wtg': 0.0238,
              }

    op_time = st.number_input("Operational time, h", value=2, step=1)

    if st.checkbox('Set operational parameters', value=False):
        inputs['tin'] = st.number_input("Fluid inlet temperature, °C", value=20, step=1)
        inputs['q'] = st.number_input("Circulation rate, lpm", value=794.933, step=10.0)
        inputs['rpm'] = st.number_input("RPM", value=100, step=1)
        inputs['tbit'] = st.number_input("Torque on bit, kN*m", value=1.35, step=1.0)
        inputs['wob'] = st.number_input("Torque on bit (kN*m)", value=22.41, step=1.0)
        inputs['rop'] = st.number_input("ROP, m/h", value=14.4, step=1.0)
        inputs['an'] = st.number_input("Area of the nozzles (in2)", value=3100, step=100)

    if st.checkbox('Set densities', value=False):
        inputs['rhof'] = st.number_input("Fluid density, sg", value=1.2, step=0.1)
        inputs['rhod'] = st.number_input("Pipe density, sg", value=7.8, step=0.1)
        inputs['rhoc'] = st.number_input("Casing density, sg", value=7.8, step=0.1)
        inputs['rhor'] = st.number_input("Riser density, sg", value=7.8, step=0.1)
        inputs['rhow'] = st.number_input("Seawater density, sg", value=1.03, step=0.1)
        inputs['rhocem'] = st.number_input("Cement density, sg", value=2.7, step=0.1)
        inputs['ddo'] = st.number_input("Pipe OD, in", value=4.5, step=0.1)
        inputs['ddi'] = st.number_input("Pipe ID, in", value=4.0, step=0.1)

    if st.checkbox('Set parameters for offshore case', value=False):
        inputs['wd'] = st.number_input("Water depth, m", value=0, step=10)
        inputs['dro'] = st.number_input("Riser OD, in", value=21.0, step=0.1)
        inputs['dri'] = st.number_input("Riser ID, in", value=17.716, step=0.1)
        inputs['wtg'] = st.number_input("Seawater thermal gradient ,°C/m, in", value=0.0238, step=0.01)

    # Adding casings
    csg_no = st.number_input("Number of casings", value=0, step=1)
    casings = add_casings(csg_no)

    plot_type = st.multiselect('Select the plots you want to generate',
                               ['MD vs Temperature', 'Temperature behavior'], ['MD vs Temperature'])

    if st.button('Run'):

        if trajectory is None:
            st.warning('No wellbore trajectory loaded')

        else:
            temp_object = ptd.temp(trajectory, op_time, change_input=inputs)

            if 'MD vs Temperature' in plot_type:
                st.plotly_chart(temp_object.plot())

            if 'Temperature behavior' in plot_type:
                st.plotly_chart(temp_object.behavior().plot())'''


def add_casings(csg_no):
    csgs = []
    for x in range(csg_no):
        st.markdown('#### Set dimensions for casing ' + str(x + 1))
        csg_od = st.number_input("Casing " + str(x + 1) + " OD, in")
        csg_id = st.number_input("Casing " + str(x + 1) + " ID, in")
        csg_depth = st.number_input("Casing " + str(x + 1) + " depth, m")
        csgs.append({'od': csg_od, 'id': csg_id, 'depth': csg_depth})
    return csgs


def load_trajectory():
    trajectory = None
    file_type = st.selectbox("File format",
                             ['excel', 'csv'],
                             )

    uploaded_file = st.file_uploader('Load file ', type=["xlsx", "csv"])

    if uploaded_file:
        if file_type == 'excel':
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)

        trajectory = wp.load(df, grid_length=50)

    return trajectory


def set_default_values():
    inputs = {'tin': 20,
              'q': 794.933,
              'rpm': 100,
              'tbit': 1.35,
              'wob': 22.41,
              'rop': 14.4,
              'an': 3100,
              'rhof': 1.2,
              'rhod': 7.8,
              'rhoc': 7.8,
              'rhor': 7.8,
              'rhow': 1.03,
              'rhocem': 2.7,
              'ddo': 4.5,
              'ddi': 4.0,
              'wd': 0,
              'dro': 21.0,
              'dri': 17.716,
              'wtg': 0.0238,
              }

    return inputs
