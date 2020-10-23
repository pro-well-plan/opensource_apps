import lasio
import streamlit as st
import petrodc.ags as ags
import SessionState


def add_well_logs_app():
    session_state = SessionState.get(name="", logs_list=None, df=None)
    uploaded_file = st.file_uploader('Load las file', type=["las"])
    if uploaded_file:
        string = uploaded_file.read().decode()
        number = len(string)

        if number > 0:
            df_file = lasio.read(string).df()
            session_state.df = df_file
            session_state.logs_list = list(session_state.df.columns)
        logs = st.multiselect('Select the logs to be included',
                              session_state.logs_list,
                              default=session_state.logs_list[:4])

        if len(logs) == 1:
            st.warning('Please select at least two logs')
        if len(logs) > 1:
            df_final = session_state.df[logs]
            fig = ags.plot_log(df_final)
            st.pyplot(fig)
