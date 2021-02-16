import streamlit as st
import torque_drag as td
import pandas as pd
import well_profile as wp


def add_torque_drag_app():
    st.subheader('Torque and Drag APP')

    st.write("This is a web based application to calculate drag forces and torque along the well."
             " This is part of the open source initiative by Pro Well Plan AS.")

    st.info('torque_drag is a python package for Torque & Drag calculations. New features are  \
                added as they are needed; suggestions and contributions of all kinds are very welcome.')

    st.markdown('[source code]'
                '(https://github.com/pro-well-plan/torque_drag)')

    st.markdown('[python package]'
                '(https://pypi.org/project/torque_drag/)')

    st.markdown('[About our Open Source initiative]'
                '(https://prowellplan.com/modern-drilling-organization/open-source-boosting-the-digital-transformation)')

    file_type = st.selectbox("File format",
                             ['excel', 'csv'],
                             key='file_type')

    trajectory = None

    uploaded_file = st.file_uploader('Load well trajectory: ', type=["xlsx", "csv"])

    if uploaded_file:
        if file_type == 'excel':
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)

        trajectory = wp.load(df, units='metric')

        trajectory.md = [point['md'] for point in trajectory.trajectory]
        trajectory.tvd = [point['tvd'] for point in trajectory.trajectory]
        trajectory.inclination = [point['inc'] for point in trajectory.trajectory]
        trajectory.azimuth = [point['azi'] for point in trajectory.trajectory]

    # Set default parameters
    od_pipe = 4.5
    id_pipe = 4.0
    od_annular = 5.0
    length_pipe = 2000
    rhof = 1.3
    rhod = 7.8
    wob = 0
    tbit = 0

    if st.checkbox('Set parameters:'):

        if st.checkbox('Pipe parameters:'):
            od_pipe = st.number_input('Pipe OD, [in]:', value=4.5, step=0.1)
            id_pipe = st.number_input('Pipe ID, [in]:', value=4.0, step=0.1)
            od_annular = st.number_input('Annular OD, [in]:', value=5.0, step=0.1)
            length_pipe = st.number_input('Pipe length, [m]:', value=2000, min_value=10, step=100)

        if st.checkbox('Densities:'):
            rhof = st.number_input('Fluid density, [sg]:', value=1.3, step=0.1)
            rhod = st.number_input('Pipe density, [sg]:', value=7.8, step=0.1)

        if st.checkbox('Operational parameters:'):
            wob = st.number_input('Weight on bit, [kN]:', value=0, step=1)
            tbit = st.number_input('Torque on bit, [kN*m]:', value=0, step=1)

    st.write('Plot:')
    plot_dg = st.checkbox('Drag force', value=True)
    plot_tq = st.checkbox('Torque')

    if trajectory is not None:

        dimensions = {'od_pipe': od_pipe, 'id_pipe': id_pipe, 'length_pipe': length_pipe, 'od_annular': od_annular}

        densities = {'rhof': rhof, 'rhod': rhod}

        result = td.calc(trajectory, dimensions, densities, case='all', torque_calc=True, wob=wob, tbit=tbit)

        if plot_dg:
            fig = result.plot()
            st.plotly_chart(fig)

        if plot_tq:
            fig = result.plot(plot_case='Torque')
            st.plotly_chart(fig)

    else:
        st.warning('No data loaded')
