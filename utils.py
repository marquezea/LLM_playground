import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from openai import OpenAI
import google.generativeai as genai
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from huggingface_hub import InferenceClient
import boto3
import anthropic
import os
import requests
import base64
import json
import tiktoken
from groq import Groq
from langchain_ollama.llms import OllamaLLM

MODELS = {
    'GPT 4o mini': {
        'model': "gpt-4o-mini",
        'provider':'OpenAI',
        'price_in_token': 0.00015,
        'price_out_token': 0.0006,
        'max_tokens': 128000
    },
    'GPT 4o': {
        'model': "gpt-4o",
        'provider':'OpenAI',
        'price_in_token': 0.005,
        'price_out_token': 0.015,
        'max_tokens': 128000
    },
    'Claude Sonnet': {
        'model': "claude-3-5-sonnet-20240620",
        'provider':'Anthropic',
        'price_in_token': 0.003,
        'price_out_token': 0.015,
        'max_tokens': 200000
    },
    'Claude Haiku': {
        'model': "claude-3-haiku-20240307",
        'provider':'Anthropic',
        'price_in_token': 0.00025,
        'price_out_token': 0.00125,
        'max_tokens': 200000
    },
    'Gemini 1.5 Flash': {
        'model': "gemini-1.5-flash",
        'provider':'Google',
        'price_in_token': 0.00035,
        'price_out_token': 0.00105,
        'max_tokens': 128000
    },
    'Gemini 1.5 Pro': {
        'model': "gemini-1.5-pro",
        'provider':'Google',
        'price_in_token': 0.0035,
        'price_out_token': 0.0105,
        'max_tokens': 128000
    },
    'Mistral Large': {
        'model': "mistral-large-latest",
        'provider':'Mistral',
        'price_in_token': 0.003,
        'price_out_token': 0.009,
        'max_tokens': 128000
    },
    'Mistral Nemo': {
        'model': "open-mistral-nemo",
        'provider':'Mistral',
        'price_in_token': 0.0003,
        'price_out_token': 0.0003,
        'max_tokens': 128000
    },
    "HF Mistral-7B-Instruct-v0.1":{
        'model': "mistralai/Mistral-7B-Instruct-v0.1",
        'provider':'HuggingFace',
        'price_in_token': 0.0003,
        'price_out_token': 0.0006,
        'max_tokens': 1024
    },
    "Groq Llama 3.1 8B Insta":{
        'model': "llama3-8b-8192",
        'provider':'Groq',
        'price_in_token': 0.0003,
        'price_out_token': 0.0006,
        'max_tokens': 8092
    }
}

IMAGE_MODELS = {
    'DALL-E 3': {
        'model': 'dall-e-3',
        'operation_mode': 'sync',
        'provider': 'OpenAI',
        'resolutions': ['1024x1024','1792x1024','1024x1792'],
        'supported_quality': ['standard','hd']
    },
    'DALL-E 2': {
        'model': 'dall-e-2',
        'operation_mode': 'sync',
        'provider': 'OpenAI',
        'resolutions': ['256x256', '512x512', '1024x1024'],
        'supported_quality': ['standard']
    },
    'Stability D3': {
        'model': 'Stable Difusion 3',
        'operation_mode': 'sync',
        'provider': 'Stability',
        'resolutions': ['1:1','16:9','21:9','2:3','3:2','4:5','5:4','9:16','9:21'],
        'supported_quality': ['sd3-medium','sd3-large-turbo','sd3-large']
    },
    'Leonardo': {
        'model': 'Leonardo Free',
        'operation_mode': 'async',
        'provider': 'Leonardo',
        'resolutions': ['768,768','768,1024','1024,768','1024,1024'],
        'supported_quality': ['DYNAMIC','PHOTOGRAPHY']
    },
}

def getImageClient(model, model_engine):
    provider = IMAGE_MODELS[model]['provider']
    if provider == 'OpenAI':
        return OpenAI()
    elif provider == 'Stability':
        return requests
    elif provider == 'Leonardo':
        return requests
    else:
        raise ValueError(f"Provider {provider} not supported")

def generateImage(model, client, model_engine, prompt, resolution, quality):
    provider = IMAGE_MODELS[model]['provider']
    if provider == 'OpenAI':
        return client.images.generate(
            model=model_engine,
            prompt=prompt,
            size=resolution,
            quality=quality,
            n=1,
            response_format="b64_json",
        )
    elif provider == 'Stability':
        return requests.post(
            f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
            headers={
                "authorization": f"Bearer {os.environ["STABILITY_API_KEY"]}",
                "accept": "image/*"
            },
            files={"none": ''},
            data={
                "prompt": f"{prompt}",
                "output_format": "jpeg",
                "aspect_ratio": resolution,
                "model": quality,
            },
        )
    elif provider == 'Leonardo':
        return requests.post(
            f"https://cloud.leonardo.ai/api/rest/v1/generations",
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": f"Bearer {os.environ["LEONARDO_API_KEY"]}"
            },
            json={
                "alchemy": True,
                "prompt": f"{prompt}",
                "width": int(resolution.split(',')[0]),
                "height": int(resolution.split(',')[1]),
                "num_images": 1,
                "presetStyle": quality,
                "photoReal": True,
            },
        )
    else:
        raise ValueError(f"Provider {provider} not supported")

def getImageResponse(model, response):
    provider = IMAGE_MODELS[model]['provider']
    if provider == 'OpenAI':
        b64_image = response.data[0].b64_json
        return base64.b64decode(b64_image)
    elif provider == 'Stability':
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(str(response.json()))
    else:
        raise ValueError(f"Provider {provider} not supported")

def getLLMClient(model, model_engine):
    provider = MODELS[model]['provider']
    if provider == 'OpenAI':
        return OpenAI()
    elif provider == 'Anthropic':
        return anthropic.Anthropic()
    elif provider == 'Google':
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        return genai.GenerativeModel(model_engine)
    elif provider == 'Mistral':
        return MistralClient(api_key=os.environ["MISTRAL_API_KEY"])
    elif provider == 'HuggingFace':
        return InferenceClient(
            model_engine,
            token=os.environ["HFINF_API_KEY"],
        )
    elif provider == 'Groq':
        return Groq(api_key=os.environ.get("GROQ_API_KEY"))
    elif provider == 'localhost':
        return OllamaLLM(
            model=model_engine,
            temperature=0.9,
        )
    else:
        raise ValueError(f"Provider {provider} not supported")

def chatCompletion(model, client, model_engine):
    provider = MODELS[model]['provider']
    try:
        if provider == 'OpenAI':
            return client.chat.completions.create(
                model=model_engine,
                max_tokens=st.session_state['max_tokens'],
                temperature=st.session_state['temperature'],
                messages=st.session_state.messages
            )
        elif provider == 'Anthropic':
            messages = st.session_state.messages
            anthropic_messages = [{'role':message['role'], 'content':[{'type':'text', 'text': message['content']}]} for message in messages[1:]]
            return client.messages.create(
                    model=model_engine,
                    max_tokens=st.session_state['max_tokens'],
                    temperature=st.session_state['temperature'],
                    system=messages[0]['content'], ## the system message is the first message in the session
                    messages=anthropic_messages ## the rest of the messages are the user messages
                )
        elif provider == 'Google':
            messages = st.session_state.messages
            google_messages = []
            for message in messages[:-1]:
                if message['role'] == 'assistant':
                    google_messages.append({'role': 'model', 'parts': message['content']})
                else:
                    google_messages.append({'role':message['role'], 'parts': message['content']})
            chat = client.start_chat(
                history=google_messages
            )
            return chat.send_message(st.session_state.messages[-1:][0]['content'])
        elif provider == 'Mistral':
            messages = st.session_state.messages
            mistral_messages = []
            for message in messages:
                mistral_messages.append(ChatMessage(role=message['role'], content=message['content']))
            return client.chat(
                model=model_engine,
                messages=mistral_messages
            )
        elif provider == 'HuggingFace':
            return client.chat_completion(
                messages=st.session_state.messages[1:],
                max_tokens=st.session_state['max_tokens'],
                stream=False,
            )
        elif provider == 'Groq':
            return client.chat.completions.create(
                messages=st.session_state.messages[1:],
                model=model_engine,
            )
        elif provider == 'localhost':
            return client.invoke(st.session_state.messages[-1]['content'])
        else:
            raise ValueError(f"Provider {provider} not supported") 
    except Exception as e:
        raise ValueError(f"Error invoking '{provider}' LLM API. {e}")

def simplePrompt(model, client, model_engine, prompt):
    provider = MODELS[model]['provider']
    try:
        if provider == 'OpenAI':
            message = [{"role":"user", "content":prompt}]
            return client.chat.completions.create(
                model=model_engine,
                max_tokens=st.session_state['max_tokens'],
                temperature=st.session_state['temperature'],
                messages=message
            )
        elif provider == 'Anthropic':
            anthropic_messages = [{'role':'user', 'content':[{'type':'text', 'text': prompt}]}]
            return client.messages.create(
                    model=model_engine,
                    max_tokens=st.session_state['max_tokens'],
                    temperature=st.session_state['temperature'],
                    messages=anthropic_messages
                )
        elif provider == 'Google':
            chat = client.start_chat()
            return chat.send_message(prompt)
        elif provider == 'Mistral':
            mistral_messages = [ChatMessage(role='user', content=prompt)]
            return client.chat(
                model=model_engine,
                messages=mistral_messages
            )
        elif provider == 'HuggingFace':
            return client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=st.session_state['max_tokens'],
                stream=False,
            )
        elif provider == 'Groq':
            return client.chat.completions.create(
                messages=[{"role":"user", "content":prompt}],
                model=model_engine,
            )
        elif provider == 'localhost':
            return client.invoke([{"role":"user", "content":prompt}])
        else:
            raise ValueError(f"Provider {provider} not supported") 
    except Exception as e:
        raise ValueError(f"Error invoking '{provider}' LLM API. {e}")

def getResponse(model, response):
    provider = MODELS[model]['provider']
    if provider == 'OpenAI':
        return response.choices[0].message.content
    elif provider == 'Anthropic':
        return response.content[0].text
    elif provider == 'Google':
        return response.text
    elif provider == 'Mistral':
        return response.choices[0].message.content
    elif provider == 'HuggingFace':
        return response.choices[0].message.content
    elif provider == 'Groq':
        return response.choices[0].message.content
    elif provider == 'localhost':
        return response
    else:
        raise ValueError(f"Provider {provider} not supported")

def verbose(title, value):
    if st.session_state['verbose']:
        st.write(f"{title}: {value}")

def updateUsage(model, response):
    provider = MODELS[model]['provider']
    if provider == 'OpenAI':
        completion = response.usage.completion_tokens
        prompt = response.usage.prompt_tokens
    elif provider == 'Anthropic':
        completion = response.usage.output_tokens
        prompt = response.usage.input_tokens
    elif provider == 'Google':
        completion = response.usage_metadata.candidates_token_count
        prompt = response.usage_metadata.prompt_token_count
    elif provider == 'Mistral':
        completion = response.usage.completion_tokens
        prompt = response.usage.prompt_tokens
    elif provider == 'HuggingFace':
        completion = response['usage']['completion_tokens']
        prompt = response['usage']['prompt_tokens']
    elif provider == 'Groq':
        completion = response.usage.completion_tokens
        prompt = response.usage.prompt_tokens
    elif provider == 'localhost':
        completion = 0
        prompt = 0
    else:
        raise ValueError(f"Provider {provider} not supported")
    
    session_usage = st.session_state.usage
    session_usage[model]['in'] += prompt
    session_usage[model]['out'] += completion
    session_usage[model]['cost'] = session_usage[model]['in'] * MODELS[model]['price_in_token'] / 1000 + session_usage[model]['out'] * MODELS[model]['price_out_token'] / 1000
    st.session_state.usage = session_usage

def countTokens(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    return len(tokens)

def getTokens():
    session_usage = st.session_state.usage
    in_tokens = sum([v['in'] for v in session_usage.values()])
    out_tokens = sum([v['out'] for v in session_usage.values()])
    return in_tokens + out_tokens

def getCost():
    session_usage = st.session_state.usage
    cost = sum([v['cost'] for v in session_usage.values()])
    return cost

def clear_messages():
    skill_prompt = [k['prompt'] for k in st.session_state.settings['skills'] if k['name'] == st.session_state['sel_skill']][0]
    st.session_state["messages"] = [{"role": "assistant", "content": skill_prompt}]

def load_settings(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def initialize():
    st.set_page_config(layout="wide")
    st.markdown("""
        <style>
        .metric-border {
            border: 2px solid #ffffff;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
        }
        </style>
        """, unsafe_allow_html=True)    
    if "settings" not in st.session_state:
        st.session_state['settings'] = load_settings('settings.json')
    if "sel_skill" not in st.session_state:
        st.session_state['sel_skill'] = 'default'
    if "verbose" not in st.session_state:
        st.session_state['verbose'] = False
    if "usage" not in st.session_state:
        st.session_state.usage = {model_title:{'in':0, 'out':0, 'cost':0} for model_title,_ in MODELS.items()}
    if "messages" not in st.session_state:
        clear_messages()
    if "selected_model" not in st.session_state:
        st.session_state["selected_model"] = MODELS["GPT 4o mini"]['model']
    if "selected_img_model" not in st.session_state:
        st.session_state["selected_img_model"] = IMAGE_MODELS["DALL-E 2"]['model']
    if "openai_api_key" not in st.session_state:
        st.session_state["openai_api_key"] = os.getenv("OPENAI_API_KEY")
    if "max_tokens" not in st.session_state:
        st.session_state['max_tokens'] = 4000
    if "temperature" not in st.session_state:
        st.session_state['temperature'] = 0.0
    if "resolution" not in st.session_state:
        st.session_state['resolution'] = "1024x1024"
    if "operation_mode" not in st.session_state:
        st.session_state['operation_mode'] = "sync"
    if "image_id" not in st.session_state:
        st.session_state['image_id'] = ""
    if "quality" not in st.session_state:
        st.session_state['quality'] = "standard"
    if "voice" not in st.session_state:
        st.session_state['voice'] = "alloy"
    if "voice_speed" not in st.session_state:
        st.session_state['voice_speed'] = "1.0"

def display_sidebar(
        display_model=True,
        display_image_model=False,
        display_verbose=True,
        display_max_tokens=True,
        display_temperature=True,
        display_usage=True,
        display_resolution=False,
        display_quality=False,
        display_voice=False,
        display_voice_speed=False,
        display_skills=True,
    ):
    with st.sidebar:
        if display_model:
            st.session_state["selected_model"] = st.radio("Select Model", [model_title for model_title,_ in MODELS.items()], index=0)
        if display_image_model:
            st.session_state["selected_img_model"] = st.radio("Select Image Model", [model_title for model_title,_ in IMAGE_MODELS.items()], index=0)
            st.session_state['operation_mode'] = IMAGE_MODELS[st.session_state.selected_img_model]['operation_mode']
        if display_verbose:
            st.session_state['verbose'] = st.sidebar.checkbox("Verbose", value=st.session_state['verbose'])
        if display_skills:
            skills = [k['name'] for k in st.session_state.settings['skills']]
            st.session_state['sel_skill'] = st.sidebar.selectbox("Skill", skills, index=0, on_change=clear_messages)
        if display_max_tokens:
            limit_tokens = [v['max_tokens'] for k,v in MODELS.items() if k == st.session_state["selected_model"]][0]
            st.session_state['max_tokens'] = st.sidebar.slider("Max Tokens", min_value=1000, max_value=limit_tokens, value=min(st.session_state['max_tokens'],limit_tokens), step=1000)
        if display_temperature:
            st.session_state['temperature'] = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=st.session_state['temperature'], step=0.1)
        if display_resolution:
            resolutions = IMAGE_MODELS[st.session_state.selected_img_model]['resolutions']
            st.session_state['resolution'] = st.selectbox("Resolution", resolutions, index=0)
        if display_quality:
            supported_quality = IMAGE_MODELS[st.session_state.selected_img_model]['supported_quality']
            st.session_state['quality'] = st.selectbox("Quality", supported_quality, index=0)
        if display_voice:
            st.session_state['voice'] = st.selectbox("Voice", ["alloy", "echo", "fable", "onyx", "nova", "shimmer"], index=0)
        if display_voice_speed:
            st.session_state['voice_speed'] = st.selectbox("Voice Speed", ["0.75", "1.0", "1.25", "1.5"], index=1)
        if display_usage:
            with st.container(border=True):
                st.write("### :orange[API Consumption]")	
                col1,col2 = st.columns([1,2])
                col1.markdown(f"## :gray[Tokens]")
                col2.markdown(f"## {getTokens()}")
                col3,col4 = st.columns([1,2])
                col3.markdown(f"## :gray[Cost]")
                col4.markdown(f"## USD {getCost():.6f}")