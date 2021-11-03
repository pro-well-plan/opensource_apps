import streamlit as st
import well_profile as wp
import pandas as pd
import base64


def add_well_profile_app():
    st.subheader('WELLBORE 3D APP')

    st.write("This is a web based application to create, manipulate and visualize 3D wellbore trajectory data,"
             " based on well_profile. This is part of the open source initiative by Pro Well Plan AS.")

    st.info('well_profile is a python package to generate or load wellbore profiles in 3D. Features are added \
            as they are needed; suggestions and contributions of all kinds are very welcome.')

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown("[![Github](https://img.shields.io/badge/source-well_profile-green.svg?logo=github)]"
                    "(https://github.com/pro-well-plan/well_profile)")
    with c2:
        st.markdown("[![PyPI version](https://badge.fury.io/py/well-profile.svg)]"
                    "(https://badge.fury.io/py/well-profile)")
    with c3:
        st.markdown("[![Documentation Status](https://readthedocs.org/projects/well_profile/badge/?version=latest)]"
                    "(http://well_profile.readthedocs.io/?badge=latest)")
    with c4:
        st.markdown("[![Build Status](https://www.travis-ci.org/pro-well-plan/well_profile.svg?branch=master)]"
                    "(https://www.travis-ci.org/pro-well-plan/well_profile)")

    st.markdown('<iframe src="https://ghbtns.com/github-btn.html?user=pro-well-plan&repo=well_profile&type=star&'
                'count=true" frameborder="0" scrolling="0" width="160" height="25" title="GitHub"></iframe>',
                unsafe_allow_html=True)

    building_preference = st.selectbox(
            'Select the way to start:',
            ('Load existing trajectory', 'Create shape-based trajectory', 'Create trajectory from 2 points')
        )

    if building_preference == 'Create trajectory from 2 points':

        st.markdown('### Set kick-off point:')
        kop_depth = st.number_input("tvd", value=100, step=10)

        st.markdown('### Set target point:')
        c1, c2, c3 = st.columns(3)
        with c1:
            target_north = st.number_input("north", value=500, step=10)
        with c2:
            target_east = st.number_input("east", value=800, step=10)
        with c3:
            target_depth = st.number_input("tvd", value=800, step=10)

        show_data, dark, color = settings()
        traj = wp.two_points({'kickoff': {'north': 0, 'east': 0, 'tvd': kop_depth},
                              'target': {'north': target_north, 'east': target_east, 'tvd': target_depth}})

        data_and_plot(traj, show_data, dark, color)

    if building_preference == 'Create shape-based trajectory':

        units = 'metric'
        length_units = 'm'

        profile = st.selectbox(
            'Select a well profile type',
            ('Vertical', 'J-type', 'S-type', 'Horizontal single curve', 'Horizontal double curve')
        )

        show_data, dark, color = settings()
        # Create a vertical well
        if profile == 'Vertical':
            profile = 'V'
            param_dict = set_parameters(profile, length_units)
            traj = wp.get(param_dict['mdt'], points=100, set_info={'units': units},
                          set_start=param_dict['start'])

            data_and_plot(traj, show_data, dark, color)

        # Create a J-type well
        if profile == 'J-type':
            profile = 'J'
            param_dict = set_parameters(profile, length_units)
            traj = wp.get(param_dict['mdt'],
                          points=100,
                          profile=profile,
                          build_angle=param_dict['build_angle'],
                          kop=param_dict['kop'],
                          eob=param_dict['eob'],
                          set_info={'units': units},
                          set_start=param_dict['start'])

            data_and_plot(traj, show_data, dark, color)

        # Create a S-type well
        if profile == 'S-type':
            profile = 'S'
            param_dict = set_parameters(profile, length_units)
            traj = wp.get(param_dict['mdt'],
                          points=100,
                          profile=profile,
                          build_angle=param_dict['build_angle'],
                          kop=param_dict['kop'],
                          eob=param_dict['eob'],
                          sod=param_dict['sod'],
                          eod=param_dict['eod'],
                          set_info={'units': units},
                          set_start=param_dict['start'])

            data_and_plot(traj, show_data, dark, color)

        # Create a horizontal single curve well
        if profile == 'Horizontal single curve':
            profile = 'H1'
            param_dict = set_parameters(profile, length_units)
            traj = wp.get(param_dict['mdt'],
                          profile=profile,
                          kop=param_dict['kop'],
                          eob=param_dict['eob'],
                          set_info={'units': units},
                          set_start=param_dict['start'])

            data_and_plot(traj, show_data, dark, color)

        # Create a horizontal double curve well
        if profile == 'Horizontal double curve':
            profile = 'H2'
            param_dict = set_parameters(profile, length_units)

            traj = wp.get(param_dict['mdt'],
                          points=100,
                          profile=profile,
                          build_angle=param_dict['build_angle'],
                          kop=param_dict['kop'],
                          eob=param_dict['eob'],
                          kop2=param_dict['kop2'],
                          eob2=param_dict['eob2'],
                          set_info={'units': units},
                          set_start=param_dict['start'])

            data_and_plot(traj, show_data, dark, color)

    if building_preference == 'Load existing trajectory':

        st.set_option('deprecation.showfileUploaderEncoding', False)

        c1, c2 = st.columns(2)

        with c1:
            wells_no = st.number_input('Number of files:', step=1, value=1)

        wellbores_data = []
        wellbores_names = []

        with c2:
            units = st.selectbox(
                'System of units',
                ('metric', 'english')
            )

        if units == 'metric':
            length_units = 'm'
        else:
            length_units = 'ft'

        for x in range(wells_no):

            st.write('_________________')

            c1, c2 = st.columns(2)
            with c1:
                well_name = st.text_input('Set name:', value='well ' + str(x+1))
            with c2:
                file_type = st.selectbox("File format",
                                         ['excel', 'csv'],
                                         key='file_type' + str(x))

            start = {'north': 0, 'east': 0}

            uploaded_file = st.file_uploader('Load file ' + str(x+1), type=["xlsx", "csv"])

            if uploaded_file:
                if file_type == 'excel':
                    df = pd.read_excel(uploaded_file)
                else:
                    df = pd.read_csv(uploaded_file)

                if st.checkbox('Set initial point:', key='set_start' + str(x)):
                    c1, c2 = st.columns(2)
                    with c1:
                        start_north = st.number_input("north, " + length_units, value=0, step=10,
                                                      key='initial_north' + str(x))
                    with c2:
                        start_east = st.number_input("east, " + length_units, value=0, step=10,
                                                     key='initial_east' + str(x))
                    start = {'north': start_north, 'east': start_east}
                trajectory = wp.load(df, equidistant=False, set_info={'units': units}, set_start=start)
                wellbores_data.append(trajectory)
                wellbores_names.append(well_name)

                c1, c2 = st.columns(2)
                with c1:
                    if st.checkbox("Show loaded data", value=False, key='rawLoad' + str(x)):
                        st.dataframe(df, width=1000)

                with c2:
                    if st.checkbox("Show converted data", value=False, key='convLoad'+str(x)):
                        st.dataframe(trajectory.df())
                        csv = trajectory.df().to_csv(index=False)
                        b64 = base64.b64encode(csv.encode()).decode()  # some strings
                        link = f'<a href="data:file/csv;base64,{b64}" download="wellpath.csv">Download dataset</a>'
                        st.markdown(link, unsafe_allow_html=True)

                interp_pt = st.number_input("Data at MD depth (" + length_units + ")", value=0.0, step=10.0,
                                            key='interp' + str(x), min_value=0.0,
                                            max_value=float(trajectory.trajectory[-1]['md']))

                if interp_pt != 0:
                    st.write(trajectory.get_point(interp_pt))

        if len(wellbores_data) >= 1:
            st.write('-----------------')
            style = {'units': units}

            c1, c2, c3 = st.columns(3)

            with c1:
                st.write('')
                st.write('')
                st.write('')
                style['darkMode'] = st.checkbox("Dark Mode", value=False)
            with c2:
                plot_type = st.selectbox('Plot type:',
                                         ('3d',
                                          'top',
                                          'vs'))
            with c3:
                color = st.selectbox('Color by:',
                                     ('None',
                                      'Dogleg Severity (dls)',
                                      'Dogleg (dl)',
                                      'Inclination (inc)',
                                      'Azimuth (azi)',
                                      'Measured Depth (md)',
                                      'True Vertical Depth (tvd)'))

            color_data = {'None': None,
                          'Dogleg Severity (dls)': 'dls',
                          'Dogleg (dl)': 'dl',
                          'Inclination (inc)': 'inc',
                          'Azimuth (azi)': 'azi',
                          'Measured Depth (md)': 'md',
                          'True Vertical Depth (tvd)': 'tvd'}

            style['color'] = color_data[color]
            style['size'] = 2
            if color_data[color] is not None:
                style['size'] = st.slider('Marker size:', min_value=1, max_value=8, value=2, step=1)

        if len(wellbores_data) == 0:
            st.warning('No data loaded')
        else:
            if plot_type == 'vs':
                c1, c2 = st.columns(2)
                with c1:
                    xaxis = st.selectbox('X axis:',
                                         ('md',
                                          'tvd',
                                          'north',
                                          'east',
                                          'dl',
                                          'dls',
                                          'inc',
                                          'azi'))
                with c2:
                    yaxis = st.selectbox('Y axis:',
                                         ('inc',
                                          'azi',
                                          'dl',
                                          'dls',
                                          'md',
                                          'tvd',
                                          'north',
                                          'east'))
            else:
                xaxis = yaxis = None
            fig = wellbores_data[0].plot(plot_type=plot_type,
                                         x_axis=xaxis,
                                         y_axis=yaxis,
                                         add_well=wellbores_data[1:],
                                         names=wellbores_names,
                                         style=style)
            st.plotly_chart(fig)


def settings():
    st.write('-----------------')

    c1, c2, c3 = st.columns(3)
    show_data = False
    with c1:
        st.write('##')
        if st.checkbox("Show values", value=False):
            show_data = True
    with c2:
        st.write('##')
        dark = st.checkbox("Activate Dark Mode", value=False)
    with c3:
        color = st.selectbox('Color by:',
                             ('None',
                              'Dogleg Severity (dls)',
                              'Dogleg (dl)',
                              'Inclination (inc)',
                              'Azimuth (azi)',
                              'Measured Depth (md)',
                              'True Vertical Depth (tvd)'))

    return show_data, dark, color


def data_and_plot(trajectory, show_data, dark, color):

    if show_data:
        st.dataframe(trajectory.df())
        csv = trajectory.df().to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings
        link = f'<a href="data:file/csv;base64,{b64}" download="wellpath.csv">Download dataset</a>'
        st.markdown(link, unsafe_allow_html=True)

    color_data = {'None': None,
                  'Dogleg Severity (dls)': 'dls',
                  'Dogleg (dl)': 'dl',
                  'Inclination (inc)': 'inc',
                  'Azimuth (azi)': 'azi',
                  'Measured Depth (md)': 'md',
                  'True Vertical Depth (tvd)': 'tvd'}

    marker_size = 2
    if color_data[color] is not None:
        marker_size = st.slider('Marker size:', min_value=1, max_value=8, value=2, step=1)

    style = {'darkMode': dark, 'color': color_data[color], 'size': marker_size}

    fig = trajectory.plot(style=style)

    st.plotly_chart(fig)


def set_parameters(profile, length_units):
    mdt = st.number_input("Final depth, " + length_units, value=3000, step=100)

    st.write('Surface location')
    c1, c2, c3 = st.columns(3)
    with c1:
        start_north = st.number_input("north, " + length_units, value=0, step=10)
    with c2:
        start_east = st.number_input("east, " + length_units, value=0, step=10)
    with c3:
        start_depth = st.number_input("tvd, " + length_units, value=0, step=10)

    start = {'north': start_north, 'east': start_east, 'depth': start_depth}
    result = {'mdt': mdt, 'start': start}

    if profile != 'V':
        c1, c2 = st.columns(2)
        with c1:
            result['kop'] = st.number_input("Kick-off point, " + length_units, value=1000, step=100)
        with c2:
            result['eob'] = st.number_input("End of build, " + length_units, value=1500, step=100)

    if profile == 'J':
        result['build_angle'] = st.number_input("Build angle, °", value=45, step=1)

    if profile == 'S':
        c1, c2, c3 = st.columns(3)
        with c1:
            result['build_angle'] = st.number_input("Build angle, °", value=45, step=1)
        with c2:
            result['sod'] = st.number_input("Kick-off point 2, " + length_units, value=2000, step=100)
        with c3:
            result['eod'] = st.number_input("End of build 2, " + length_units, value=2500, step=100)

    if profile == 'H2':
        c1, c2, c3 = st.columns(3)
        with c1:
            result['build_angle'] = st.number_input("Build angle, °", value=45, step=1)
        with c2:
            result['kop2'] = st.number_input("Start of drop, " + length_units, value=2500, step=100)
        with c3:
            result['eob2'] = st.number_input("End of drop, " + length_units, value=3000, step=100)

    return result
