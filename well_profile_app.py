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

    st.markdown('[source code]'
                '(https://github.com/pro-well-plan/well_profile)')

    st.markdown('[python package]'
                '(https://pypi.org/project/well-profile/)')

    st.markdown('[About our Open Source initiative]'
                '(https://prowellplan.com/modern-drilling-organization/open-source-boosting-the-digital-transformation)')

    building_preference = st.selectbox(
            'Select the way to start:',
            ('Load existing trajectory', 'Create a new trajectory')
        )

    units = st.selectbox(
        'Select the system of units',
        ('metric', 'english')
    )

    if units == 'metric':
        length_units = 'm'
    else:
        length_units = 'ft'

    if building_preference == 'Create a new trajectory':

        profile = st.selectbox(
            'Select a well profile type',
            ('Vertical', 'J-type', 'S-type', 'Horizontal single curve', 'Horizontal double curve')
        )

        # Create a vertical well
        if profile == 'Vertical':
            profile = 'V'
            param_dict = set_parameters(profile, length_units)
            traj = wp.get(param_dict['mdt'], cells_no=param_dict['cells_no'], units=units,
                          set_start=param_dict['start'])

            data_and_plot(traj)

        # Create a J-type well
        if profile == 'J-type':
            profile = 'J'
            param_dict = set_parameters(profile, length_units)
            traj = wp.get(param_dict['mdt'],
                          cells_no=param_dict['cells_no'],
                          profile=profile,
                          build_angle=param_dict['build_angle'],
                          kop=param_dict['kop'],
                          eob=param_dict['eob'],
                          units=units,
                          set_start=param_dict['start'])

            data_and_plot(traj)

        # Create a S-type well
        if profile == 'S-type':
            profile = 'S'
            param_dict = set_parameters(profile, length_units)
            traj = wp.get(param_dict['mdt'],
                          cells_no=param_dict['cells_no'],
                          profile=profile,
                          build_angle=param_dict['build_angle'],
                          kop=param_dict['kop'],
                          eob=param_dict['eob'],
                          sod=param_dict['sod'],
                          eod=param_dict['eod'],
                          units=units,
                          set_start=param_dict['start'])

            data_and_plot(traj)

        # Create a horizontal single curve well
        if profile == 'Horizontal single curve':
            profile = 'H1'
            param_dict = set_parameters(profile, length_units)
            traj = wp.get(param_dict['mdt'],
                          cells_no=param_dict['cells_no'],
                          profile=profile,
                          kop=param_dict['kop'],
                          eob=param_dict['eob'],
                          units=units,
                          set_start=param_dict['start'])

            data_and_plot(traj)

        # Create a horizontal double curve well
        if profile == 'Horizontal double curve':
            profile = 'H2'
            param_dict = set_parameters(profile, length_units)

            traj = wp.get(param_dict['mdt'],
                          cells_no=param_dict['cells_no'],
                          profile=profile,
                          build_angle=param_dict['build_angle'],
                          kop=param_dict['kop'],
                          eob=param_dict['eob'],
                          kop2=param_dict['kop2'],
                          eob2=param_dict['eob2'],
                          units=units,
                          set_start=param_dict['start'])

            data_and_plot(traj)

    if building_preference == 'Load existing trajectory':

        st.set_option('deprecation.showfileUploaderEncoding', False)
        wells_no = st.number_input('Number of files:', step=1, value=1)

        wellbores_data = []
        wellbores_names = []

        for x in range(wells_no):

            st.write('_________________')

            well_name = st.text_input('Set name:', value='well ' + str(x+1))

            start = {'north': 0, 'east': 0}

            if st.checkbox('Set coordinates of initial point:', key='set_start' + str(x)):
                start_north = st.number_input("Initial point, North, " + length_units, value=0, step=1,
                                              key='initial_north' + str(x))
                start_east = st.number_input("Initial point, East, " + length_units, value=0, step=1,
                                             key='initial_east' + str(x))
                start = {'north': start_north, 'east': start_east}

            file_type = st.selectbox("File format",
                                     ['excel', 'csv'],
                                     key='file_type' + str(x))

            uploaded_file = st.file_uploader('Load file ' + str(x+1), type=["xlsx", "csv"])

            if uploaded_file:
                if file_type == 'excel':
                    df = pd.read_excel(uploaded_file)
                else:
                    df = pd.read_csv(uploaded_file)

                trajectory = wp.load(df, units=units, set_start=start)
                wellbores_data.append(trajectory)
                wellbores_names.append(well_name)

                if st.checkbox("Show loaded data", value=False, key='raw_load'+str(x)):
                    st.dataframe(df, width=1000)

                if st.checkbox("Show converted data", value=False, key='conv_load'+str(x)):
                    st.dataframe(trajectory.df())
                    csv = trajectory.df().to_csv(index=False)
                    b64 = base64.b64encode(csv.encode()).decode()  # some strings
                    link = f'<a href="data:file/csv;base64,{b64}" download="wellpath.csv">Download dataset</a>'
                    st.markdown(link, unsafe_allow_html=True)

        dark = st.checkbox("Activate Dark Mode", value=False)

        if st.button('Generate 3D plot'):

            if len(wellbores_data) == 0:
                st.warning('No data loaded')
            else:
                fig = wellbores_data[0].plot(add_well=wellbores_data[1:], names=wellbores_names, dark_mode=dark)
                st.plotly_chart(fig)


def data_and_plot(trajectory):

    if st.checkbox("Show values", value=False):
        st.dataframe(trajectory.df())
        csv = trajectory.df().to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings
        link = f'<a href="data:file/csv;base64,{b64}" download="wellpath.csv">Download dataset</a>'
        st.markdown(link, unsafe_allow_html=True)

    dark = st.checkbox("Activate Dark Mode", value=False)
    fig = trajectory.plot(dark_mode=dark)

    if st.button("Generate 3D plot"):
        st.plotly_chart(fig)


def set_parameters(profile, length_units):
    mdt = st.number_input("Final depth, " + length_units, value=3000, step=100)
    cells_no = st.number_input("Number of cells", value=100, step=1)
    start_north = st.number_input("Initial point, North, " + length_units, value=0, step=1)
    start_east = st.number_input("Initial point, East, " + length_units, value=0, step=1)
    start_depth = st.number_input("Initial point, Depth, " + length_units, value=0, step=1)
    start = {'north': start_north, 'east': start_east, 'depth': start_depth}
    result = {'mdt': mdt, 'cells_no': cells_no, 'start': start}
    s_build_angle, s_kop2, s_eob2, s_sod, s_eod = False, False, False, False, False

    if profile != 'V':
        kop = st.number_input("Kick-off point, " + length_units, value=1000, step=100)
        eob = st.number_input("End of build, " + length_units, value=1500, step=100)
        result['kop'] = kop
        result['eob'] = eob

    if profile == 'J':
        s_build_angle = True

    if profile == 'S':
        s_build_angle = True
        s_sod = True
        s_eod = True

    if profile == 'H2':
        s_build_angle = True
        s_kop2 = True
        s_eob2 = True

    if s_build_angle:
        build_angle = st.number_input("Build angle, °", value=45, step=1)
        result['build_angle'] = build_angle
    if s_kop2:
        kop2 = st.number_input("Kick-off point 2, " + length_units, value=2000, step=100)
        result['kop2'] = kop2
    if s_eob2:
        eob2 = st.number_input("End of build 2, " + length_units, value=2500, step=100)
        result['eob2'] = eob2
    if s_sod:
        sod = st.number_input("Start of drop, " + length_units, value=2500, step=100)
        result['sod'] = sod
    if s_eod:
        eod = st.number_input("End of drop, " + length_units, value=3000, step=100)
        result['eod'] = eod

    return result
