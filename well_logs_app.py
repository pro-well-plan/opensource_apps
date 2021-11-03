import lasio
import streamlit as st
import petrodc.ags as ags
import SessionState
import base64


def add_well_logs_app():

    st.subheader('Visualizing well logs')

    st.write("This simple app allows you to visualize any LAS file you upload below. This is part of the open"
             " source initiative by Pro Well Plan AS.")

    st.markdown('[About our Open Source initiative]'
                '(https://prowellplan.com/modern-drilling-organization/open-source-boosting-the-digital-transformation)')

    session_state = SessionState.get(name="", logs_list=None, df=None)      # record log_list and df when it is created
    uploaded_file = st.file_uploader('Load a LAS file', type=["las"])

    if uploaded_file:
        string = uploaded_file.read().decode()
        number = len(string)

        if number > 0:
            df_file = lasio.read(string).df()
            df_file.index.name = 'DEPT'
            df_file['MD '+'(ref)'] = df_file.index.values
            session_state.df = df_file
            session_state.logs_list = list(session_state.df.columns)
        logs = st.multiselect('Select the logs to be included',
                              session_state.logs_list,
                              default=session_state.logs_list[:4])

        if len(logs) == 1:
            st.warning('Please select at least two logs')
        else:
            df_final = session_state.df[logs]
            fig = ags.plot_log(df_final)
            st.plotly_chart(fig)

            st.dataframe(df_final)
            csv = df_final.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # some strings
            link = f'<a href="data:file/csv;base64,{b64}" download="well_logs_data.csv">Download dataset</a>'
            st.markdown(link, unsafe_allow_html=True)
