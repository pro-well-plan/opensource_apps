import streamlit as st
import pandas as pd
import well_profile as wp
import pwploads as pld


def add_pwploads_app():
    st.subheader('Load Cases APP')

    st.write("This is a web based application to generate load cases along pipes."
             " This is part of the open source initiative by Pro Well Plan AS.")

    st.info('pwploads is a python package for load cases calculations in order to develop modern \
            well designs easier and faster. New features are added as they are needed; '
            'suggestions and contributions of all kinds are very welcome.')

    st.markdown('[source code]'
                '(https://github.com/pro-well-plan/pwploads)')

    st.markdown('[python package]'
                '(https://pypi.org/project/pwploads/)')

    st.markdown('[documentation]'
                '(https://pwploads.readthedocs.io/en/latest/)')

    st.markdown('[About our Open Source initiative]'
                '(https://prowellplan.com/modern-drilling-organization/'
                'open-source-boosting-the-digital-transformation)')

    st.markdown('#### 1. Load the wellbore trajectory')

    file_type = st.selectbox("File format",
                             ['excel', 'csv'],
                             key='file_type')

    trajectory = None

    uploaded_file = st.file_uploader('Load well trajectory: ', type=["xlsx", "csv"])

    if uploaded_file:
        if file_type == 'excel':
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)

        trajectory = wp.load(df, units='metric')

    st.markdown('#### 2. Create a casing with the specifications you need')

    # Default Values
    od_pipe = 8.0
    id_pipe = 7.2
    length_pipe = 1500
    nominal_weight = 100
    grade = 'L-80'
    df_vme = 1.25
    df_burst = 1.1
    df_collapse = 1.1
    df_tension = 1.3
    df_compression = 1.3
    p_test = 4000
    f_ov = 0
    specs = False
    f_ov_status = False
    p_test_status = False
    v_avg = 0.3
    e = 29
    fric = 0.24
    a = 1.5
    cement = False
    rho_cem = 1.8
    displ_fluid = 1.3
    f_pre = 0.0
    p_res = 5800
    tvd_res = 2000
    rho_gas = 0.5
    rho_mud = 1.4
    conn_compression = 0.6
    conn_tension = 0.6
    df_conn_compression = 1.0
    df_conn_tension = 1.0

    if st.checkbox('Set Casing Dimensions'):
        od_pipe = st.number_input('OD, [in]:', value=8.0, step=0.1)
        id_pipe = st.number_input('ID, [in]:', value=7.2, step=0.1)
        length_pipe = st.number_input('Pipe length, [m]:', value=1500, min_value=10, step=100)

    if st.checkbox('Set Material Properties'):
        nominal_weight = st.number_input('Nominal weight, [kg/m]:', value=100, step=1)
        grade = st.selectbox("Steel grade:",
                             ['H-40', 'J-55', 'K-55', 'M-65', 'N-80', 'L-80', 'C-90', 'R-95', 'T-95',
                              'C-110', 'P-110', 'Q-125'], index=5)
        conn_compression = st.number_input('Connection compression strength, [%]:', value=60, step=1, min_value=0,
                                           max_value=100) / 100
        conn_tension = st.number_input('Connection tension strength, [%]:', value=60, step=1, min_value=0,
                                       max_value=100) / 100

    if st.checkbox('Set Design Factors'):
        df_vme = st.number_input('Von Mises:', value=1.25, step=0.1)
        df_burst = st.number_input('API - Burst:', value=1.1, step=0.1)
        df_collapse = st.number_input('API - Collapse:', value=1.1, step=0.1)
        df_tension = st.number_input('API - Tension:', value=1.3, step=0.1)
        df_compression = st.number_input('API - Compression:', value=1.3, step=0.1)
        df_conn_compression = st.number_input('Connection - Compression:', value=1.0, step=0.1)
        df_conn_tension = st.number_input('Connection - Tension:', value=1.0, step=0.1)

    casing = pld.Casing(od_pipe, id_pipe, length_pipe,
                        nominal_weight,
                        int(grade[2:])*1000,
                        df_tension,
                        df_compression,
                        df_burst,
                        df_collapse,
                        df_vme,
                        conn_compression,
                        conn_tension,
                        df_conn_compression,
                        df_conn_tension)

    st.markdown('#### 3. Set fluid')
    fluids_no = st.number_input('Number of fluids:', step=1, value=1)

    delta_tvd = float(length_pipe / fluids_no)

    rho_list = []
    tvd_list = []
    for x in range(fluids_no):
        st.write(' - fluid ' + str(x+1))
        rho_f = st.number_input('Fluid density, sg:', value=1.2, step=0.1, key='fluid' + str(x))
        rho_list.append(rho_f)
        tvd_f = st.number_input('Final Depth, m:', value=float(delta_tvd*(x+1)), step=100.0, key='tvd' + str(x))
        tvd_list.append(tvd_f)
    tvd_list = tvd_list[:-1]

    st.markdown('#### 4. Modify parameters for load cases')

    if st.checkbox('Running in hole'):
        specs = True

    if st.checkbox('Overpull'):
        f_ov_status = True
        specs = True

    if st.checkbox('Green Cement Pressure Test'):
        p_test_status = True
        cement = True

    if st.checkbox('Cementing'):
        cement = True
        displ_fluid = st.number_input('Displacement fluid density, sg:', value=1.3, step=0.1)
        f_pre = st.number_input('Pre-loading force, kN:', value=0, step=10)

    if st.checkbox('Displacement to Gas'):
        p_res = st.number_input('Reservoir Pressure, psi:', value=5800, step=100)
        tvd_res = st.number_input('Reservoir Depth (tvd), m:', value=2000, step=100)
        rho_gas = st.number_input('Gas density, sg:', value=0.5, step=0.1)
        rho_mud = st.number_input('Mud density, sg:', value=1.4, step=0.1)

    if p_test_status:
        p_test = st.number_input('Testing pressure, psi:', value=4000, step=100)

    if f_ov_status:
        f_ov = st.number_input('Overpull force, kN:', value=0, step=10)

    if specs:
        v_avg = st.number_input('Average running speed, m/s:', value=0.3, step=0.1)
        e = st.number_input("Young's modulus, psi x10^6:", value=29, step=1)
        fric = st.number_input('Sliding friction factor:', value=0.24, step=0.01)
        a = st.number_input('Ratio max speed / avg speed:', value=1.5, step=0.1)

    if cement:
        rho_cem = st.number_input('Cement density, sg:', value=1.8, step=0.1)

    if st.button('Generate plot'):

        if trajectory is not None:

            casing.add_trajectory(trajectory)
            e *= 1e6

            casing.overpull(tvd_fluid=tvd_list, rho_fluid=rho_list, v_avg=v_avg, e=e, fric=fric, a=a, f_ov=f_ov)
            casing.running(tvd_fluid=tvd_list, rho_fluid=rho_list, v_avg=v_avg, e=e, fric=fric, a=a)
            casing.green_cement(tvd_fluid_int=tvd_list, rho_fluid_int=rho_list,
                                rho_cement=rho_cem, p_test=p_test)
            casing.cementing(rho_cement=rho_cem, rho_fluid=displ_fluid, e=e, f_pre=f_pre)
            casing.displacement_gas(p_res=p_res, tvd_res=tvd_res, rho_gas=rho_gas, rho_mud=rho_mud, e=e)

            fig = casing.plot()

            st.plotly_chart(fig)

        else:
            st.warning('No trajectory loaded')

    st.write('More features will be added soon...')
