import gradio as gr

def predict_churn(age, total_purchase, account_manager, years, num_sites):

    new_data = pd.DataFrame({
        "Age": [age],
        "Total_Purchase": [total_purchase],
        "Account_Manager": [account_manager],
        "Years": [years],
        "Num_Sites": [num_sites]
    })

    # Ajouter la constante comme pendant l'entraînement
    new_data = sm.add_constant(new_data, has_constant="add")

    proba = logit_model.predict(new_data)[0]

    prediction = "Churn" if proba >= 0.5 else "Pas de churn"

    return prediction, round(float(proba), 3)


with gr.Blocks() as demo:

    gr.Markdown("# Prédiction du churn")

    age = gr.Number(label="Âge")
    total_purchase = gr.Number(label="Total purchase")
    account_manager = gr.Radio(choices=[0, 1], label="Account manager")
    years = gr.Number(label="Années")
    num_sites = gr.Number(label="Nombre de sites")

    bouton = gr.Button("Prédire")

    prediction = gr.Textbox(label="Prédiction")
    probabilite = gr.Number(label="Probabilité de churn")

    bouton.click(
        fn=predict_churn,
        inputs=[age, total_purchase, account_manager, years, num_sites],
        outputs=[prediction, probabilite]
    )

demo.launch()
