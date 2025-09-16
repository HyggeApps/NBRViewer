from honeybee.model import Model as HBModel
import streamlit as st

fp = f'tests/HBJSON TERMICO.hbjson'
model = HBModel.from_hbjson(fp)

st.write(model)