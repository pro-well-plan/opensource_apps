import streamlit as st


def add_pwploads_app():
    st.subheader('Load Cases APP')

    st.write("This is a web based application to generate load cases along pipes.")

    st.info('pwploads is a python package for load cases calculations in order to develop modern \
            well designs easier and faster. New features are added as they are needed; '
            'suggestions and contributions of all kinds are very welcome.')

    st.markdown('[source code]'
                '(https://github.com/pro-well-plan/pwploads)')

    st.markdown('[python package]'
                '(https://pypi.org/project/pwploads/)')
