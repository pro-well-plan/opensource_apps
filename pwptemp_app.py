import streamlit as st


def add_pwptemp_app():
    st.subheader('Well Temperature APP')

    st.write("This is a web based application to generate well temperature distributions.")

    st.info('pwptemp is a python package for easy calculation of the temperature distribution along  \
             the well. New features are added as they are needed; '
            'suggestions and contributions of all kinds are very welcome.')

    st.markdown('[source code]'
                '(https://github.com/pro-well-plan/pwptemp)')

    st.markdown('[python package]'
                '(https://pypi.org/project/pwptemp/)')
