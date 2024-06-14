# Python In-built packages
from pathlib import Path
import PIL

# External packages
import streamlit as st

# Local Modules
import settings
import helper

# Setting page layout
st.set_page_config(
    page_title="肇事动物检测系统",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("肇事动物检测系统")
st.caption("使用改进的RT-DETR模型对肇事动物图片进行检测")

# Sidebar
st.sidebar.header("模型配置")

# Model Options
model_type0 = st.sidebar.radio(
    "请选择任务类型", ['目标检测'])
model_type = st.sidebar.selectbox(
    '请选择检测模型', ('改进的RT-DETR', 'YOLOv8', 'RT-DETR-r18')
)

confidence = st.sidebar.slider(
            '请滑动选择模型的置信度', min_value=0.0, max_value=1.0, value=0.5)

# Selecting Detection Or Segmentation
if model_type == '改进的RT-DETR':
    from ultralytics import RTDETR
    model_path = Path('wights/best.pt')
    # Load Pre-trained ML Model
    try:
        model=RTDETR('weights/best.pt')
    except Exception as ex:
        st.error(f"Unable to load model. Check the specified path: {model_path}")
        st.error(ex)

elif model_type == 'YOLOv8':
    from ultralytics import YOLO
    model_path = Path('wights/yolov8.pt')
    # Load Pre-trained ML Model
    try:
        model=YOLO('weights/yolov8.pt')
    except Exception as ex:
        st.error(f"Unable to load model. Check the specified path: {model_path}")
        st.error(ex)

elif model_type == 'RT-DETR-r18':
    from ultralytics import YOLO
    model_path = Path('wights/RT-DETR.pt')
    # Load Pre-trained ML Model
    try:
        model=RTDETR('weights/RT-DETR.pt')
    except Exception as ex:
        st.error(f"Unable to load model. Check the specified path: {model_path}")
        st.error(ex)


st.sidebar.header("图片配置")
source_radio = st.sidebar.radio(
    "请选择资源类型", settings.SOURCES_LIST)

source_img = None
# If image is selected
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "请上传一张图片...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_img is None:
                default_image_path = str(settings.DEFAULT_IMAGE)
                default_image = PIL.Image.open(default_image_path)
                st.image(default_image_path, caption="默认图片",
                         use_column_width=True)
            else:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="上传的图片",
                         use_column_width=True)
        except Exception as ex:
            st.error("打开图片时发生错误.")
            st.error(ex)

    with col2:
        if source_img is None:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            default_detected_image = PIL.Image.open(
                default_detected_image_path)
            st.image(default_detected_image_path, caption='检测结果',
                     use_column_width=True)
        else:
            if model_type == '改进的RT-DETR':
                model=RTDETR('weights/best.pt')
            elif model_type == 'YOLOv8':
                model=YOLO('weights/yolov8.pt')
            elif model_type == 'RT-DETR-r18':
                model=RTDETR('weights/RT-DETR.pt')
            res = model.predict(uploaded_image,
                                conf=confidence
                                )
            boxes = res[0].boxes
            res_plotted = res[0].plot()[:, :, ::-1]
            st.image(res_plotted, caption='检测结果',
                         use_column_width=True)

else:
    st.error("请上传有效的类型!")
