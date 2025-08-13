import asyncio
import os

import streamlit as st
from celeste_core import ImageArtifact, Provider, list_models
from celeste_core.enums.capability import Capability
from celeste_core.enums.capability import Capability as Cap
from celeste_core.models.registry import list_models as list_models_core
from celeste_image_edit import create_image_editor

st.title("Celeste Image Edit")

# Derive providers that have IMAGE_EDIT capability
PROVIDERS = sorted(
    {m.provider for m in list_models_core(capability=Cap.IMAGE_EDIT)},
    key=lambda p: p.value,
)

with st.sidebar:
    image_edit_provider = st.selectbox(
        "Select provider", [p.name for p in PROVIDERS], key="provider"
    )

    models = list_models(
        provider=Provider[image_edit_provider], capability=Capability.IMAGE_EDIT
    )
    display = [m.display_name or m.id for m in models]
    id_by_display = {d: models[i].id for i, d in enumerate(display)}
    selected_display = st.selectbox("Select model", display, key="model")

image_editor = create_image_editor(
    provider=Provider[image_edit_provider], model=id_by_display[selected_display]
)

uploaded_file = st.file_uploader(
    "Choose an image", type=["jpg", "jpeg", "png"]
) or st.selectbox(
    "Or select from data",
    [f"data/{f}" for f in os.listdir("data") if f.endswith((".jpg", ".png"))],
)
if uploaded_file:
    image_data = (
        uploaded_file.read()
        if hasattr(uploaded_file, "read")
        else open(uploaded_file, "rb").read()
    )
    st.image(image_data)
    image = ImageArtifact(data=image_data)

prompt = st.text_input("Edit prompt", value="Put the image in black and white")

if st.button("Edit Image") and uploaded_file:
    with st.spinner("Editing..."):
        output = asyncio.run(image_editor.edit_image(prompt=prompt, image=image))
        if output and output.data:
            st.image(output.data, caption="Edited Image")
