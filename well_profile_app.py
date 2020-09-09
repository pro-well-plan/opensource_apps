import streamlit as st
import well_profile as wp
import pandas as pd
import base64


def add_well_profile_app():
    st.subheader('WELLBORE 3D APP')

    st.write("This is a web based application to create, manipulate and visualize 3D wellbore trajectory data, "
             "based on well_profile.")

    st.info('well_profile is a python package to generate or load wellbore profiles in 3D. Features are added \
            as they are needed; suggestions and contributions of all kinds are very welcome.')

    st.markdown('[source code]'
                        '(https://github.com/pro-well-plan/well_profile)')

    st.markdown('[python package]'
                        '(https://pypi.org/project/well-profile/)')

    building_preference = st.selectbox(
            'Select the way to start:',
            ('Load from excel file', 'Create a new trajectory')
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
            mdt = st.number_input("Final depth, " + length_units, value=3000, step=100)
            profile = 'V'
            traj = wp.get(mdt, grid_length=10, units=units)

            data_and_plot(traj)

        # Create a J-type well
        if profile == 'J-type':
            mdt = st.number_input("Final depth, " + length_units, value=3000, step=100)
            kop = st.number_input("Kick-off point, " + length_units, value=1000, step=100)
            eob = st.number_input("End of build, " + length_units, value=1500, step=100)
            build_angle = st.number_input("Build angle, °", value=45, step=1)
            profile = 'J'
            traj = wp.get(mdt,
                          grid_length=10,
                          profile=profile,
                          build_angle=build_angle,
                          kop=kop,
                          eob=eob,
                          units=units)

            data_and_plot(traj)

        # Create a S-type well
        if profile == 'S-type':
            mdt = st.number_input("Final depth, " + length_units, value=3000, step=100)
            kop = st.number_input("Kick-off point, " + length_units, value=1000, step=100)
            eob = st.number_input("End of build, " + length_units, value=1500, step=100)
            build_angle = st.number_input("Build angle, °", value=45, step=1)
            sod = st.number_input("Start of drop, " + length_units, value=2500, step=100)
            eod = st.number_input("End of drop, " + length_units, value=3000, step=100)
            profile = 'S'
            traj = wp.get(mdt,
                          grid_length=10,
                          profile=profile,
                          build_angle=build_angle,
                          kop=kop,
                          eob=eob,
                          sod=sod,
                          eod=eod,
                          units=units)

            data_and_plot(traj)

        # Create a horizontal single curve well
        if profile == 'Horizontal single curve':
            mdt = st.number_input("Final depth, " + length_units, value=3000, step=100)
            kop = st.number_input("Kick-off point, " + length_units, value=1000, step=100)
            eob = st.number_input("End of build, " + length_units, value=1500, step=100)
            build_angle = st.number_input("Build angle, °", value=45, step=1)
            profile = 'H1'
            traj = wp.get(mdt,
                          grid_length=10,
                          profile=profile,
                          build_angle=build_angle,
                          kop=kop,
                          eob=eob,
                          units=units)

            data_and_plot(traj)

        # Create a horizontal double curve well
        if profile == 'Horizontal double curve':
            mdt = st.number_input("Final depth, " + length_units, value=3000, step=100)
            kop = st.number_input("Kick-off point, " + length_units, value=1000, step=100)
            eob = st.number_input("End of build, " + length_units, value=1500, step=100)
            build_angle = st.number_input("Build angle, °", value=45, step=1)
            kop2 = st.number_input("Kick-off point 2, " + length_units, value=2000, step=100)
            eob2 = st.number_input("End of build 2, " + length_units, value=2500, step=100)
            profile = 'H2'
            traj = wp.get(mdt,
                          grid_length=10,
                          profile=profile,
                          build_angle=build_angle,
                          kop=kop,
                          eob=eob,
                          kop2=kop2,
                          eob2=eob2,
                          units=units)

            data_and_plot(traj)

    if building_preference == 'Load from excel file':

        st.set_option('deprecation.showfileUploaderEncoding', False)
        wells_no = st.number_input('Number of files:', step=1, value=1)

        wellbores_data = []
        wellbores_names = []

        for x in range(wells_no):

            well_name = st.text_input('Set name:', value='well ' + str(x+1))

            file_type = st.selectbox("File format",
                                     ['excel', 'csv'],
                                     key='file_type' + str(x))

            uploaded_file = st.file_uploader('Load file ' + str(x+1), type=["xlsx", "csv"])

            if uploaded_file:
                if file_type == 'excel':
                    df = pd.read_excel(uploaded_file)
                else:
                    df = pd.read_csv(uploaded_file)

                trajectory = wp.load(df, grid_length=10, units=units)
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

        if st.button('Generate 3D plot'):

            fig = wellbores_data[0].plot(add_well=wellbores_data[1:], names=wellbores_names)
            st.plotly_chart(fig)


def data_and_plot(trajectory):
    fig = trajectory.plot()

    if st.checkbox("Show values", value=False):
        st.dataframe(trajectory.df())
        csv = trajectory.df().to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings
        link = f'<a href="data:file/csv;base64,{b64}" download="wellpath.csv">Download dataset</a>'
        st.markdown(link, unsafe_allow_html=True)

    if st.button("Generate 3D plot"):
        st.plotly_chart(fig)
