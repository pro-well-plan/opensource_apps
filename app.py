import streamlit as st
from well_profile_app import add_well_profile_app
from others import under_construction
from side_bar import add_side_bar, main_selection
from footer import add_footer


def main():
    st.image('https://user-images.githubusercontent.com/52009346/69100304-2eb3e800-0a5d-11ea-9a3a-8e502af2120b.png',
             use_column_width=True)

    selection = main_selection()

    if selection == 'Wellbore 3D':
        add_well_profile_app()
    else:
        under_construction()

    add_footer()

    add_side_bar()


if __name__ == '__main__':
    main()
