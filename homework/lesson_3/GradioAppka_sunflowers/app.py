from fastai.vision.all import *
from pathlib import Path
import gradio as gr

# ----------------------------
# Načtení modelu
# ----------------------------
learn = load_learner(Path('model_cleansplit.pkl'))
categories = learn.dls.vocab
print("Třídy modelu:", categories)

# ----------------------------
# Funkce pro klasifikaci obrázku
# ----------------------------
def classify_image(img):
    pred, idx, probs = learn.predict(img)
    return dict(zip(categories, map(float, probs)))  # přímo float pravděpodobnosti

# ----------------------------
# Gradio komponenty
# ----------------------------
image_input = gr.Image(type="pil", label="Nahrát obrázek")
output_label = gr.Label(label="Predikce")
examples = ["test_flower.jpg"]  # pokud chceš mít ukázkový obrázek

# ----------------------------
# Vytvoření interface a spuštění
# ----------------------------
intf = gr.Interface(
    fn=classify_image,
    inputs=image_input,
    outputs=output_label,
    examples=examples,
    live=False
)

intf.launch(share=True)  # veřejný dočasný odkaz, jen pro test
