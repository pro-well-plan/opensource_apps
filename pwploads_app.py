import streamlit as st
import pandas as pd
import well_profile as wp
import pwploads as pld


def add_pwploads_app():
    st.subheader('Load Cases APP')

    st.write("This is a web based application to generate load cases along pipes."
             " This is part of the open source initiative by Pro Well Plan AS.")

    st.info('pwploads is a python package for load cases calculations in order to develop modern \
            well designs easier and faster. New features are added as they are needed; '
            'suggestions and contributions of all kinds are very welcome.')

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown("[![Github](https://img.shields.io/badge/source-pwploads-green.svg?logo=github)]"
                    "(https://github.com/pro-well-plan/pwploads)")
    with c2:
        st.markdown("[![PyPI version](https://badge.fury.io/py/pwploads.svg)]"
                    "(https://badge.fury.io/py/pwploads)")
    with c3:
        st.markdown("[![Documentation Status](https://readthedocs.org/projects/pwploads/badge/?version=latest)]"
                    "(http://pwploads.readthedocs.io/?badge=latest)")
    with c4:
        st.markdown("[![Build Status](https://www.travis-ci.org/pro-well-plan/pwploads.svg?branch=master)]"
                    "(https://www.travis-ci.org/pro-well-plan/pwploads)")

    st.markdown('#### 1. Load the wellbore trajectory')

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

        trajectory = wp.load(df, equidistant=False, set_info={'units': 'metric'})

    st.markdown('#### 2. Create a casing with the specifications you need')

    df = {'pipe': {'tension': 1.1, 'compression': 1.1, 'burst': 1.1, 'collapse': 1.1, 'triaxial': 1.25},
          'connection': {'tension': 1.0, 'compression': 1.0}}

    pipe = {'od': 8,
            'id': 7.2,
            'shoeDepth': 1500,
            'tocMd': 1000,
            'weight': 100,
            'yield': 80000,
            'top': 200,
            'e': 29e6}

    settings = {'densities': {'mud': 1.2,
                              'cement': 1.8,
                              'cementDisplacingFluid': 1.3,
                              'gasKick': 0.5,
                              'completionFluid': 1.8},
                'tripping': {'slidingFriction': 0.24,
                             'speed': 0.3,
                             'maxSpeedRatio': 1.5},
                'production': {'resPressure': 5800,
                               'resTvd': 2000,
                               'fluidDensity': 1.7,
                               'packerFluidDensity': 1.3,
                               'packerTvd': 1450,
                               'perforationsTvd': 1600,
                               'poisson': 0.3},
                'forces': {'overpull': 0,
                           'preloading': 0},
                'testing': {'cementingPressure': 4000}}

    # Default Values
    grade = 'L-80'
    conn_compression = 0.6
    conn_tension = 0.6

    if st.checkbox('Set Casing Dimensions'):
        pipe['od'] = st.number_input('OD, [in]:', value=8.0, step=0.1)
        pipe['id'] = st.number_input('ID, [in]:', value=7.2, step=0.1)
        pipe['shoeDepth'] = st.number_input('Shoe depth, [m]:', value=1500, min_value=10, step=100)
        pipe['top'] = st.number_input('Top depth MD, [m]:', value=1500, min_value=10, step=100)

    if st.checkbox('Set Material Properties'):
        pipe['weight'] = st.number_input('Nominal weight, [kg/m]:', value=100, step=1)
        grade = st.selectbox("Steel grade:",
                             ['H-40', 'J-55', 'K-55', 'M-65', 'N-80', 'L-80', 'C-90', 'R-95', 'T-95',
                              'C-110', 'P-110', 'Q-125'], index=5)
        conn_compression = st.number_input('Connection compression strength, [%]:', value=60, step=1, min_value=0,
                                           max_value=100) / 100
        conn_tension = st.number_input('Connection tension strength, [%]:', value=60, step=1, min_value=0,
                                       max_value=100) / 100

    if st.checkbox('Set Design Factors'):
        df['pipe']['triaxial'] = st.number_input('Von Mises:', value=1.25, step=0.1)
        df['pipe']['burst'] = st.number_input('API - Burst:', value=1.1, step=0.1)
        df['pipe']['collapse'] = st.number_input('API - Collapse:', value=1.1, step=0.1)
        df['pipe']['tension'] = st.number_input('API - Tension:', value=1.3, step=0.1)
        df['pipe']['compression'] = st.number_input('API - Compression:', value=1.3, step=0.1)
        df['connection']['compression'] = st.number_input('Connection - Compression:', value=1.0, step=0.1)
        df['connection']['tension'] = st.number_input('Connection - Tension:', value=1.0, step=0.1)

    pipe['yield'] = int(grade[2:])*1000
    casing = pld.Casing(pipe,
                        conn_compression,
                        conn_tension,
                        df)

    st.markdown('#### 3. Set parameters')

    if st.checkbox('Set densities, sg'):

        settings['densities']['mud'] = st.number_input('Mud:', value=1.2, step=0.1)
        settings['densities']['cement'] = st.number_input('Cement:', value=1.8, step=0.1)
        settings['densities']['cementDisplacingFluid'] = st.number_input('Displacing fluid (cementing):', value=1.3,
                                                                         step=0.1)
        settings['densities']['gasKick'] = st.number_input('Gas kick:', value=0.5, step=0.1)
        settings['densities']['completionFluid'] = st.number_input('Completion fluid:', value=1.8, step=0.1)

    if st.checkbox('Set tripping parameters'):

        settings['tripping']['slidingFriction'] = st.number_input('Sliding friction factor:', value=0.24, step=0.01)
        settings['tripping']['speed'] = st.number_input('Sliding friction factor, m/s:', value=0.3, step=0.1)
        settings['tripping']['maxSpeedRatio'] = st.number_input('Max / Avg speed ratio:', value=1.5, step=0.1)

    if st.checkbox('Set production parameters'):

        settings['production']['resPressure'] = st.number_input('Reservoir pressure, psi:', value=5800, step=100)
        settings['production']['resTvd'] = st.number_input('Reservoir depth (tvd), m:', value=2000, step=100)
        settings['production']['fluidDensity'] = st.number_input('Production fluid density, sg:', value=1.7, step=0.1)
        settings['production']['packerFluidDensity'] = st.number_input('Packer fluid density, sg:', value=1.3, step=0.1)
        settings['production']['packerTvd'] = st.number_input('Packer depth (tvd), m:', value=1450, step=100)
        settings['production']['perforationsTvd'] = st.number_input('Depth (tvd) of perforations:', value=1600,
                                                                    step=100)
    if st.checkbox('Set additional forces'):

        settings['forces']['overpull'] = st.number_input('Overpull, kN:', value=0, step=10)
        settings['forces']['preloading'] = st.number_input('Preload, kN:', value=0, step=10)

    if st.checkbox('Set testing'):

        settings['testing']['cementingPressure'] = st.number_input('Cementing Pressure test, psi:', value=4000,
                                                                   step=100)

    plots = {'Triaxial Envelope': 'vme', 'Load Profiles': 'pressureDiff', 'Safety Factors (Axial)': 'axial',
             'Safety Factors (Burst)': 'burst', 'Safety Factors (Collapse)': 'collapse'}
    plot_type = st.selectbox("Generate Plot",
                             ['None']+list(plots.keys()))

    if plot_type != 'None':
        if trajectory is not None:

            casing.add_trajectory(trajectory.trajectory)

            casing.run_loads(settings)

            fig = casing.plot(plot_type=plots[plot_type])

            st.plotly_chart(fig)

        else:
            st.warning('No trajectory loaded')

    st.write('More features will be added soon...')
