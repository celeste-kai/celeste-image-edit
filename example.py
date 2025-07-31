import streamlit as st
import os
from pathlib import Path
import asyncio

from celeste_image_edit import create_image_editor
from celeste_image_edit.core.enums import ImageEditProvider, GoogleEditModel, OpenAIEditModel, ReplicateEditModel
from celeste_image_edit.core.types import Image

st.title("Celeste Image Edit")

PROVIDER_MODEL_MAP = {
    ImageEditProvider.GOOGLE.name: GoogleEditModel,
    ImageEditProvider.OPENAI.name: OpenAIEditModel,
    ImageEditProvider.REPLICATE.name: ReplicateEditModel
}

with st.sidebar:
    image_edit_provider = st.selectbox(
        "Select provider",
        [p.name for p in list(ImageEditProvider)],
        format_func=lambda x: ImageEditProvider[x].name,
        key="provider"
    )

    image_edit_model = st.selectbox(
        "Select model",
        [m.name for m in PROVIDER_MODEL_MAP[image_edit_provider]],
        key="model"
    )

model_enum = PROVIDER_MODEL_MAP[image_edit_provider]
image_editor = create_image_editor(
    provider=ImageEditProvider[image_edit_provider].value,
    model=model_enum[image_edit_model].value
)

uploaded_file = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png']) or st.selectbox("Or select from data", [f"data/{f}" for f in os.listdir("data") if f.endswith(('.jpg', '.png'))])
if uploaded_file:
    image_data = uploaded_file.read() if hasattr(uploaded_file, 'read') else open(uploaded_file, 'rb').read()
    st.image(image_data)
    image = Image(data=image_data)

prompt = st.text_input("Edit prompt", value="Put the image in black and white")

if st.button("Edit Image") and uploaded_file:
    with st.spinner("Editing..."):
        output = asyncio.run(image_editor.edit_image(prompt=prompt, image=image))
        if output and output.data:
            st.image(output.data, caption="Edited Image")
