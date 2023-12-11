import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from bs4 import BeautifulSoup
import requests
import re
import wikipedia


def eliminar_etiquetas(texto):
    # Utiliza una expresión regular para encontrar y eliminar las etiquetas
    return re.sub(r'<.*?>', '', texto)


def google_answering(consulta):
    base_url = 'https://www.google.com/search?q='
    url = base_url + consulta

    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/80.0.3987.149 Safari/537.36'}

    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Intenta encontrar la respuesta en distintos elementos HTML
        answer_elements = soup.find_all(['div', 'span'], class_=[
                                        'Z0LcW t2b5Cf', 'hgKElc', 'wob_t q8U8x'])

        for element in answer_elements:
            if element:
                if 'wob_t' in str(element):
                    answer = eliminar_etiquetas(str(element)) + 'ºC'
                    return answer
                else:
                    answer = eliminar_etiquetas(str(element))
                    return answer

        # Configura el idioma de búsqueda para Wikipedia en español
        wikipedia.set_lang('es')
        try:
            # Intenta buscar la respuesta en Wikipedia
            answer = wikipedia.summary(consulta, sentences=3)
            if answer:
                return answer
        except wikipedia.exceptions.PageError as e:
            print(f"Error al buscar la respuesta.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return 'ERROR'


def consulta(consulta, model, tokenizer, device):
    user_input = consulta

    # Utiliza la función para obtener la respuesta
    respuesta = responder_pregunta_o_conversacion(
        user_input, model, tokenizer, device)

    print(f"{respuesta}")

    # Guardar la respuesta en respuesta.txt
    with open('respuesta.txt', 'a', encoding='utf-8') as f:
        f.write(respuesta + '\n')


def responder_pregunta_o_conversacion(input_text, model, tokenizer, device):
    # Verifica si el input contiene una pregunta (termina con "?")
    es_pregunta = input_text.strip().endswith('?')

    if es_pregunta:
        # Si es una pregunta, utiliza google_answering para obtener la respuesta
        respuesta = google_answering(input_text)
    else:
        # Si es una conversación, ejecuta una ronda del chatbot
        with torch.no_grad():
            user_inputs_ids = tokenizer.encode(
                input_text + tokenizer.eos_token, return_tensors="pt")
            user_inputs_ids = user_inputs_ids.to(device)
            chat_history = model.generate(
                user_inputs_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
            step_model_answer = tokenizer.decode(
                chat_history[:, user_inputs_ids.shape[-1]:][0], skip_special_tokens=True)
            respuesta = step_model_answer

    return respuesta
