import streamlit as st
import petrodc.usgs_eros as eros
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
        'Select a well profile type',
        ('Topo-bathymetry', 'Wellbore data NPD', 'Athabasca well logs')
    )

    if database == 'Topo-bathymetry':
        elevation_app()


def elevation_app():

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
