import requests
from collections import Counter

def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании текста: {e}")
        return None

def count_word_frequencies_optimized(text, words_to_count):
    if text is None:
        return {}

    cleaned_text = ''.join(char.lower() if char.isalnum() or char.isspace() else ' ' for char in text)
    words_in_text = cleaned_text.split() 
    text_word_counts = Counter(words_in_text)

    frequencies = {}
    for word in words_to_count:
        lower_word = word.lower()
        frequencies[word] = text_word_counts.get(lower_word, 0) 

    return frequencies

def main():
    words_file = "words.txt"
    url = "https://eng.mipt.ru/why-mipt/"

    words_to_count = []
    try:
        with open(words_file, 'r', encoding='utf-8') as file:
            for line in file:
                word = line.strip()
                if word: 
                    words_to_count.append(word)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{words_file}' не найден.")
        return
    except Exception as e:
        print(f"Ошибка при чтении файла '{words_file}': {e}")
        return

    # Скачивание текста один раз, в цикле оно вызывало постояно и нагружало
    # def count_word_frequencies(url, word):
    # text = get_text(url) - эта строка каждый раз делала многократные сетевые запросы
    
    page_text = get_text(url)

    frequencies = {}
    if page_text:
        frequencies = count_word_frequencies_optimized(page_text, words_to_count)
    else:
        print("Не удалось получить текст для анализа. Подсчет частот невозможен.")

    print(frequencies)

if __name__ == "__main__":
    main()