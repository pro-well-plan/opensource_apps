import streamlit as st
from well_profile_app import add_well_profile_app
from petrodc_app import add_petrodc_app
from pwptemp_app import add_pwptemp_app
from pwploads_app import add_pwploads_app
from torque_drag_app import add_torque_drag_app
from others import under_construction
from side_bar import add_side_bar, main_selection
from footer import add_footer


def main():
    st.image('https://user-images.githubusercontent.com/52009346/69100304-2eb3e800-0a5d-11ea-9a3a-8e502af2120b.png',
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

    if selection in ['Temperature Distribution', 'Load Cases']:
        under_construction()

    add_footer()

    add_side_bar()


if __name__ == '__main__':
    main()
