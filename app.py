import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import json
import os

DATA_FILE = 'data.json'

# Función para cargar datos desde JSON
def cargar_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return pd.DataFrame(json.load(f))
    else:
        return pd.DataFrame({'Ambiente': ["COCINA"], 'Tarea': ["DESINFECTAR"], 'Responsable': ["ANDY"]})

# Función para guardar datos en JSON
def guardar_datos(df):
    df.to_json(DATA_FILE, orient='records', indent=4)

# Página principal con tabla editable
def main():
    st.title('TAREAS DE LA CASA')

    # Cargar datos
    df = cargar_datos()

    # Formulario para agregar nuevos elementos
    with st.form(key='add_form'):
        ambiente = st.text_input('Ambiente')
        tarea = st.text_input('Tarea')
        responsable = st.text_input('Responsable')
        submit_button = st.form_submit_button(label='Agregar')

    if submit_button and ambiente and tarea and responsable:
        new_data = {'Ambiente': ambiente, 'Tarea': tarea, 'Responsable': responsable}
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        guardar_datos(df)
        st.success('Nueva tarea agregada.')

    # Configurar la tabla editable
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination()
    gb.configure_default_column(editable=True)
    grid_options = gb.build()

    # Mostrar la tabla editable
    grid_response = AgGrid(df, gridOptions=grid_options, editable=True, height=300)

    # Botón para guardar los cambios en la tabla
    if st.button('Guardar cambios'):
        updated_df = pd.DataFrame(grid_response['data'])
        guardar_datos(updated_df)
        st.success('Datos guardados correctamente.')

# Página para mostrar los datos guardados
def mostrar_datos():
    st.title('Datos guardados')
    df = cargar_datos()
    st.table(df)

# Navegación entre páginas
page = st.sidebar.selectbox('Selecciona una página', ['Editar datos', 'Mostrar datos'])

if page == 'Editar datos':
    main()
else:
    mostrar_datos()