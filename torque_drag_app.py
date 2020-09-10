import streamlit as st


def add_torque_drag_app():
    st.subheader('Torque and Drag APP')

    st.write("This is a web based application to calculate drag forces and torque along the well")

    st.info('torque_drag is a python package for Torque & Drag calculations. New features are  \
                added as they are needed; suggestions and contributions of all kinds are very welcome.')

    st.markdown('[source code]'
                '(https://github.com/pro-well-plan/torque_drag)')

    st.markdown('[python package]'
                '(https://pypi.org/project/torque_drag/)')
