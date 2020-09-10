import streamlit as st
import petrodc.usgs_eros as eros
import petrodc.npd as npd
import petrodc.ags as ags
import pandas as pd
import base64


def add_petrodc_app():
    st.subheader('Petroleum Data Collector APP')

    st.write("This is a web based application to access and visualize petroleum-related data from"
             " public databases.")

    st.info('petrodc is a python package to get datasets from public sources. New sources are  \
                added as they are tested; suggestions and contributions of all kinds are very welcome.')

    st.markdown('[source code]'
                '(https://github.com/pro-well-plan/petrodc)')

    st.markdown('[python package]'
                '(https://pypi.org/project/petrodc/)')

    database = st.selectbox(
        'Select the data source:',
        ('Topo-bathymetry', 'Wellbore data NPD', 'Athabasca well logs')
    )

    if database == 'Topo-bathymetry':
        elevation_app()

    if database == 'Wellbore data NPD':
        npd_app()

    if database == 'Athabasca well logs':
        ags_app()


def elevation_app():

    st.write("Request data from SRTM30. \
    Bathymetry / Topography (SRTM30) is a global bathymetry/topography data product distributed by the \
    USGS EROS data center. The data product has a resolution of 30 seconds (roughly 1 km).")

    elevation_type = st.radio("Select the app to use",
                              ['one single point', 'a whole area'])

    if elevation_type == 'a whole area':

        lat_min = st.number_input('lat-min:', value=59.00, step=0.01)
        lat_max = st.number_input('lat-min:', value=60.00, step=0.01)
        lon_min = st.number_input('lon-min:', value=3.00, step=0.01)
        lon_max = st.number_input('lon-min:', value=5.00, step=0.01)

        points = {'lat': [lat_min, lat_min, lat_max, lat_max],
                  'lon': [lon_min, lon_max, lon_min, lon_max]}

        st.map(pd.DataFrame(points))

        loaded_data = None

        if st.button('Generate 3D surface'):
            loaded_data = eros.elevation(lat=(lat_min, lat_max), lon=(lon_min, lon_max))
            fig = loaded_data.plot()
            st.plotly_chart(fig)

        if st.button("Show dataset"):
            if loaded_data is None:
                loaded_data = eros.elevation(lat=(lat_min, lat_max), lon=(lon_min, lon_max))
            st.dataframe(loaded_data.df)
            csv = loaded_data.df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # some strings
            link = f'<a href="data:file/csv;base64,{b64}" download="elevation_data.csv">Download dataset</a>'
            st.markdown(link, unsafe_allow_html=True)

    else:

        lat = st.number_input('lat:', value=57.00, step=0.01)
        lon = st.number_input('lon:', value=2.50, step=0.01)

        if st.button('Calculate'):
            elevation = eros.point_elev(lat, lon)
            st.write('The elevation for that location is ' + str(elevation) + ' meters')


def npd_app():

    st.write("Get wellbore data from NPD Database.")

    npd_dataset = ['oil samples',
                   'NPD ID',
                   'lithostratigraphy',
                   'history',
                   'drilling mud',
                   'drill stem tests',
                   'documents',
                   'cores',
                   'core photos',
                   'coordinates',
                   'casing and leak off',
                   'exploration',
                   'development',
                   'shallow']

    select_npd_dataset = st.radio("Select the dataset:", npd_dataset)

    if st.button("Show the selected dataset"):
        dataset_no = npd_dataset.index(select_npd_dataset) + 1
        df = npd.wellbore(dataset_no)
        st.dataframe(df)
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings
        link = f'<a href="data:file/csv;base64,{b64}" download="elevation_data.csv">Download dataset</a>'
        st.markdown(link, unsafe_allow_html=True)


def ags_app():

    st.write("Get well logs data as dataframes from Special Report 006 Athabasca Oil Sands Data \
    McMurray/Wabiskaw Oil Sands Deposit (Alberta, Canada). By Alberta Geological Survey (AGS).")

    st.write("There are 2173 files in this database.")

    specific_file = st.number_input('Select the file', value=4, max_value=2173, step=1)

    if st.button("Show dataset"):
        data_dict = ags.get_las(specific_file)
        well_name = str(list(data_dict)[-1])
        st.write("Unique well identifier: " + well_name)
        df = data_dict[well_name]
        st.dataframe(df)
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings
        link = f'<a href="data:file/csv;base64,{b64}" download="elevation_data.csv">Download dataset</a>'
        st.markdown(link, unsafe_allow_html=True)
