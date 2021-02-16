import streamlit as st
from well_profile_app import add_well_profile_app
from petrodc_app import add_petrodc_app
from pwptemp_app import add_pwptemp_app
from pwploads_app import add_pwploads_app
from torque_drag_app import add_torque_drag_app
from well_logs_app import add_well_logs_app
from others import under_construction
from side_bar import add_side_bar, main_selection
from footer import add_footer


def main():
    st.set_page_config(
        page_title="PWP - Open Source",
        page_icon='https://user-images.githubusercontent.com/52009346/93438445-9c26e400-f8cd-11ea-9183-b6df80ddd318.png'
    )

    st.image('https://github.com/pro-well-plan/opensource_apps/raw/master/resources/pwp-bgd.gif',
             use_column_width=True)

    selection = main_selection()

    if selection == 'Wellbore 3D':
        add_well_profile_app()

    if selection == 'Data Collector':
        add_petrodc_app()

    if selection == 'Temperature Distribution':
        add_pwptemp_app()

    if selection == 'Load Cases':
        add_pwploads_app()

    if selection == 'Torque & Drag':
        add_torque_drag_app()

    if selection == 'Visualize Well Logs':
        add_well_logs_app()

    add_footer()

    add_side_bar()


if __name__ == '__main__':
    main()
