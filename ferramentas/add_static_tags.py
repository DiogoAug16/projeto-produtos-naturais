import re
import os
from pathlib import Path

def add_static_tags(file_path):
    with open(file_path, 'r+', encoding='utf-8') as f:
        content = f.read()
        
        if '{% load static %}' not in content:
            content = content.replace('<!DOCTYPE html>', '{% load static %}\n<!DOCTYPE html>')
        
        replacements = [
            (r'(src|href)=["\'](images/.*?)["\']', r'\1="{% static \'\2\' %}"'),
            (r'(src|href)=["\'](img/.*?)["\']', r'\1="{% static \'\2\' %}"'),
            (r'(src|href)=["\'](css/.*?)["\']', r'\1="{% static \'\2\' %}"'),
            (r'(src|href)=["\'](js/.*?)["\']', r'\1="{% static \'\2\' %}"'),
            (r'url\(["\']?(images/.*?)["\']?\)', r'url({% static \'\1\' %})'),
            (r'url\(["\']?(img/.*?)["\']?\)', r'url({% static \'\1\' %})'),
            (r'url\(["\']?(css/.*?)["\']?\)', r'url({% static \'\1\' %})'),
            (r'url\(["\']?(js/.*?)["\']?\)', r'url({% static \'\1\' %})'),
        ]
        
        data_setbg_pattern = r'data-setbg=["\'](img/.*?\.(jpg|jpeg|png|gif|webp))["\']'
        data_setbg_replacement = r'data-setbg="{% static "\1" %}"'
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        content = re.sub(data_setbg_pattern, data_setbg_replacement, content)

        content = content.replace(r"\'", "'")

        f.seek(0)
        f.write(content)
        f.truncate()

def process_directory(directory):
    for path in Path(directory).rglob('*.html'):
        print(f"Processando: {path}")
        try:
            add_static_tags(path)
        except Exception as e:
            print(f"Erro ao processar {path}: {str(e)}")

if __name__ == "__main__":
    templates_dir = os.path.join(os.getcwd(), 'templates')
    if os.path.exists(templates_dir):
        process_directory(templates_dir)
        print("Processamento concluído!")
    else:
        print(f"Diretório não encontrado: {templates_dir}")
