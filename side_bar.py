import streamlit as st


def main_selection():
    st.sidebar.title('Open Source Apps')
    selection = st.sidebar.radio("Select the app to use",
                                 ['Wellbore 3D',
                                  'Data Collector',
                                  'Torque & Drag',
                                  'Temperature Distribution',
                                  'Load Cases'
                                  ])

    return selection


def add_side_bar():
    # Content in sidebar

    st.sidebar.image('https://www.visinnovasjon.no/wp-content/uploads/2018/10/prowellplan.png',
                     use_column_width=True)

    st.sidebar.write('_________________')

    st.sidebar.markdown('[Know more about our open source projects]'
                        '(https://prowellplan.com/modern-drilling-organization/open-source-boosting-the-'
                        'digital-transformation)')

    st.sidebar.write('_________________')
    st.sidebar.write()
    st.sidebar.markdown('[Well planning for professionals]'
                        '(https://prowellplan.com)')

    st.sidebar.image('https://prowellplan.com/imager/files/776/imac-compare_95a4de7dde4d2447564bbc200e9a931e.webp',
                     use_column_width=True)