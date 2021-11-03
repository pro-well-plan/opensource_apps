import streamlit as st
import well_profile as wp
import pwptemp.drilling2 as ptd
import pandas as pd


def add_pwptemp_app():
    st.subheader('Well Temperature APP')

    st.write("This is a web based application to generate well temperature distributions."
             " This is part of the open source initiative by Pro Well Plan AS.")

    st.info('pwptemp is a python package for easy calculation of the temperature distribution along  \
             the well. New features are added as they are needed; '
            'suggestions and contributions of all kinds are very welcome.')

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown("[![Github](https://img.shields.io/badge/source-pwptemp-green.svg?logo=github)]"
                    "(https://github.com/pro-well-plan/pwptemp)")
    with c2:
        st.markdown("[![PyPI version](https://badge.fury.io/py/pwptemp.svg)]"
                    "(https://badge.fury.io/py/pwptemp)")
    with c3:
        st.markdown("[![Documentation Status](https://readthedocs.org/projects/pwptemp/badge/?version=latest)]"
                    "(http://pwptemp.readthedocs.io/?badge=latest)")
    with c4:
        st.markdown("[![Build Status](https://www.travis-ci.org/pro-well-plan/pwptemp.svg?branch=master)]"
                    "(https://www.travis-ci.org/pro-well-plan/pwptemp)")

    inputs = set_default_values()

    trajectory = load_trajectory()

    op_time = st.number_input("Operational time, h", value=2.0, step=1.0)

    if st.checkbox('Set operational parameters', value=False):
        inputs['temp_inlet'] = st.number_input("Fluid inlet temperature, °C", value=20, step=1)
        inputs['q'] = st.number_input("Circulation rate, lpm", value=794.933, step=10.0)
        inputs['rpm'] = st.number_input("RPM", value=100, step=1)
        inputs['tbit'] = st.number_input("Torque on bit, kN*m", value=1.35, step=1.0)
        inputs['wob'] = st.number_input("Torque on bit (kN*m)", value=22.41, step=1.0)
        inputs['rop'] = st.number_input("ROP, m/h", value=14.4, step=1.0)
        inputs['an'] = st.number_input("Area of the nozzles (in2)", value=3100, step=100)

    if st.checkbox('Set densities', value=False):
        inputs['rho_fluid'] = st.number_input("Fluid density, sg", value=1.2, step=0.1)
        inputs['rho_pipe'] = st.number_input("Pipe density, sg", value=7.8, step=0.1)
        inputs['rho_csg'] = st.number_input("Casing density, sg", value=7.8, step=0.1)
        inputs['rho_riser'] = st.number_input("Riser density, sg", value=7.8, step=0.1)
        inputs['rho_seawater'] = st.number_input("Seawater density, sg", value=1.03, step=0.1)
        inputs['rho_cem'] = st.number_input("Cement density, sg", value=2.7, step=0.1)
        inputs['pipe_od'] = st.number_input("Pipe OD, in", value=4.5, step=0.1)
        inputs['pipe_id'] = st.number_input("Pipe ID, in", value=4.0, step=0.1)

    if st.checkbox('Set parameters for offshore case', value=False):
        inputs['water_depth'] = st.number_input("Water depth, m", value=0, step=10)
        inputs['riser_od'] = st.number_input("Riser OD, in", value=21.0, step=0.1)
        inputs['riser_id'] = st.number_input("Riser ID, in", value=17.716, step=0.1)
        inputs['th_grad_seawater'] = st.number_input("Seawater thermal gradient ,°C/m, in", value=0.0238, step=0.01)

    # Adding casings
    csg_no = st.number_input("Number of casings", value=0, step=1)
    casings = add_casings(csg_no)
    if len(casings) == 0:
        casings = None

    #plot_type = st.multiselect('Select the plots you want to generate',
                               #['MD vs Temperature', 'Temperature behavior'], ['MD vs Temperature'])

    if st.button('Run'):

        if trajectory is None:
            st.warning('No wellbore trajectory loaded')

        else:
            temp_object = ptd.calc_temp(op_time, trajectory, casings, set_inputs=inputs)

            st.plotly_chart(ptd.plot_distribution(temp_object))

    st.write('More features will be added soon...')


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

        trajectory = wp.load(df)

        trajectory.md = [point['md'] for point in trajectory.trajectory]
        trajectory.tvd = [point['tvd'] for point in trajectory.trajectory]
        trajectory.inclination = [point['inc'] for point in trajectory.trajectory]
        trajectory.azimuth = [point['azi'] for point in trajectory.trajectory]

    return trajectory


def set_default_values():
    inputs = {'temp_inlet': 20,
              'q': 794.933,
              'rpm': 100,
              'tbit': 1.35,
              'wob': 22.41,
              'rop': 14.4,
              'an': 3100,
              'rho_fluid': 1.2,
              'rho_pipe': 7.8,
              'rho_csg': 7.8,
              'rho_riser': 7.8,
              'rho_seawater': 1.03,
              'rho_cem': 2.7,
              'pipe_od': 4.5,
              'pipe_id': 4.0,
              'water_depth': 0,
              'riser_od': 21.0,
              'riser_id': 17.716,
              'th_grad_seawater': 0.0238,
              }

    return inputs
