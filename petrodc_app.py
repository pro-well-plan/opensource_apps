import streamlit as st
import petrodc.usgs_eros as eros
import petrodc.npd as npd
import petrodc.ags as ags
import petrodc.deposits as petd
import pandas as pd
import base64


def add_petrodc_app():
    st.subheader('Petroleum Data Collector APP')

    st.write("This is a web based application to access and visualize petroleum-related data from"
             " public databases. This is part of the open source initiative by Pro Well Plan AS.")

    st.info('petrodc is a python package to get datasets from public sources. New sources are  \
                added as they are tested; suggestions and contributions of all kinds are very welcome.')

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown("[![Github](https://img.shields.io/badge/source-petrodc-green.svg?logo=github)]"
                    "(https://github.com/pro-well-plan/petrodc)")
    with c2:
        st.markdown("[![PyPI version](https://badge.fury.io/py/petrodc.svg)]"
                    "(https://badge.fury.io/py/petrodc)")

    database = st.selectbox(
        'Select the data source:',
        ('Topo-bathymetry', 'Wellbore data NPD', 'Athabasca well logs', 'Petroleum Deposits')
    )

    if database == 'Topo-bathymetry':
        elevation_app()

    if database == 'Wellbore data NPD':
        npd_app()

    if database == 'Athabasca well logs':
        st.set_option('deprecation.showPyplotGlobalUse', False)
        ags_app()

    if database == 'Petroleum Deposits':
        deposits_app()


def elevation_app():

    st.write("Request data from SRTM30. \
    Bathymetry / Topography (SRTM30) is a global bathymetry/topography data product distributed by the \
    USGS EROS data center. The data product has a resolution of 30 seconds (roughly 1 km).")

    elevation_type = st.radio("Select the app to use",
                              ['one single point', 'a whole area'])

    if elevation_type == 'a whole area':

        lat_min = st.number_input('Lat-min, [°]:', value=59.00, step=0.01)
        lat_max = st.number_input('Lat-max, [°]:', value=60.00, step=0.01)
        lon_min = st.number_input('Lon-min, [°]:', value=3.00, step=0.01)
        lon_max = st.number_input('Lon-max, [°]:', value=5.00, step=0.01)

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
        link = f'<a href="data:file/csv;base64,{b64}" download="npd_wellbore_data.csv">Download dataset</a>'
        st.markdown(link, unsafe_allow_html=True)


def ags_app():

    st.write("Get well logs data as dataframes from Special Report 006 Athabasca Oil Sands Data \
    McMurray/Wabiskaw Oil Sands Deposit (Alberta, Canada). By Alberta Geological Survey (AGS).")

    st.write("There are 2173 files in this database.")

    specific_file = st.number_input('Select the file', value=4, max_value=2173, step=1)

    if st.button("Show well logs"):
        data_dict = ags.get_las(specific_file)
        well_name = str(list(data_dict)[-1])
        st.write("Unique well identifier: " + well_name)

        # Get df
        df = data_dict[well_name]

        # Show plot
        fig = ags.plot_log(df)
        st.pyplot(fig)

        # Show dataset
        st.dataframe(df)
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings
        link = f'<a href="data:file/csv;base64,{b64}" download="athabasca_logs.csv">Download dataset</a>'
        st.markdown(link, unsafe_allow_html=True)


def deposits_app():
    country = st.selectbox('Country:', ['all'] + pet_deposit_countries)
    deposit_type = st.selectbox('Deposit type:', ['all', 'oil', 'gas', 'oil and gas'])

    data = petd.get_deposits(country, deposit_type)
    for item in data:
        item['lon'] = item.pop('long')
    st.map(pd.DataFrame(data))

    # Show dataset
    df = pd.DataFrame(data)
    st.dataframe(df)
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings
    link = f'<a href="data:file/csv;base64,{b64}" download="athabasca_logs.csv">Download dataset</a>'
    st.markdown(link, unsafe_allow_html=True)


pet_deposit_countries = ['Afghanistan', 'Albania', 'Algeria', 'Angola', 'Argentina', 'Australia', 'Austria',
                         'Azerbaijan', 'Bahrain', 'Bangladesh', 'Belarus', 'Benin', 'Bolivia', 'Bosnia-Herzegovina',
                         'Brazil', 'Brunei', 'Bulgaria', 'Burma', 'Cambodia', 'Cameroon', 'Canada', 'Chad', 'Chile',
                         'China', 'Colombia', 'Congo (Brazzaville)', 'Congo (Kinshasa)', "Cote d'Ivoire", 'Croatia',
                         'Cuba', 'Czech Republic', 'Denmark', 'Ecuador', 'Egypt', 'Eritrea', 'Ethiopia', 'France',
                         'Gabon', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Guatemala', 'Guyana', 'Hungary', 'India',
                         'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Japan', 'Jordan', 'Kazakhstan',
                         'Kuwait', 'Kyrgyzstan', 'Latvia',  'Libya', 'Lithuania', 'Macedonia', 'Madagascar', 'Malaysia',
                         'Mexico', 'Moldova', 'Mongolia', 'Morocco', 'Mozambique', 'Namibia', 'Netherlands',
                         'New Zealand', 'Niger', 'Nigeria', 'North Korea', 'Norway', 'Oman', 'Pakistan',
                         'Papua New Guinea', 'Peru', 'Philippines', 'Poland', 'Qatar', 'Romania',
                         'Russia', 'Saudi Arabia', 'Senegal', 'Serbia/Montenegro', 'Slovakia',
                         'Slovenia', 'Somalia', 'South Africa', 'South Korea', 'Spain', 'Sudan',
                         'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan',
                         'Tanzania', 'Thailand' 'Trinidad and Tobago', 'Tunisia', 'Turkey',
                         'Turkmenistan', 'Ukraine', 'United Arab Emirates', 'United Kingdom',
                         'United States of Ameri', 'Uzbekistan', 'Venezuela', 'Vietnam', 'Yemen']
