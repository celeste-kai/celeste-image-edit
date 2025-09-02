import asyncio
import os

import streamlit as st
from celeste_core import ImageArtifact, Provider, list_models
from celeste_core.enums.capability import Capability
from celeste_image_edit import create_image_editor


async def main() -> None:
    st.set_page_config(page_title="Celeste Image Edit", page_icon="✏️", layout="wide")
    st.title("✏️ Celeste Image Edit")

    # Get providers that support image editing
    providers = sorted(
        {m.provider for m in list_models(capability=Capability.IMAGE_EDIT)},
        key=lambda p: p.value,
    )

    with st.sidebar:
        st.header("⚙️ Configuration")
        provider = st.selectbox(
            "Provider:", [p.value for p in providers], format_func=str.title
        )
        models = list_models(
            provider=Provider(provider), capability=Capability.IMAGE_EDIT
        )
        model_names = [m.display_name or m.id for m in models]
        selected_idx = st.selectbox(
            "Model:", range(len(models)), format_func=lambda i: model_names[i]
        )
        model = models[selected_idx].id

    st.markdown(f"*Powered by {provider.title()}*")

    # Image input
    uploaded_file = st.file_uploader(
        "Choose an image", type=["jpg", "jpeg", "png"]
    ) or st.selectbox(
        "Or select from data",
        [f"data/{f}" for f in os.listdir("data") if f.endswith((".jpg", ".png"))]
        if os.path.exists("data")
        else [],
    )

    if uploaded_file:
        image_data = (
            uploaded_file.read()
            if hasattr(uploaded_file, "read")
            else open(uploaded_file, "rb").read()
        )
        st.image(image_data, caption="Original Image", use_container_width=True)
        image = ImageArtifact(data=image_data)

        prompt = st.text_area(
            "Edit prompt:",
            "Put the image in black and white",
            height=80,
            placeholder="Describe how to edit the image...",
        )

        if st.button("✏️ Edit Image", type="primary", use_container_width=True):
            if not prompt.strip():
                st.error("Please enter an edit prompt.")
            else:
                image_editor = create_image_editor(Provider(provider), model=model)

                with st.spinner("Editing..."):
                    output = await image_editor.edit_image(prompt=prompt, image=image)
                    if output and output.data:
                        st.success("✅ Image edited successfully!")
                        st.image(
                            output.data,
                            caption="Edited Image",
                            use_container_width=True,
                        )

                        # Show metadata
                        with st.expander("📊 Details"):
                            st.write(f"**Provider:** {provider}")
                            st.write(f"**Model:** {model}")
                            st.write(f"**Prompt:** {prompt}")
                            if output.metadata:
                                st.json(output.metadata)
                    else:
                        st.error("Failed to edit image. Please try again.")

    st.markdown("---")
    st.caption("Built with Streamlit • Powered by Celeste")


if __name__ == "__main__":
    asyncio.run(main())
