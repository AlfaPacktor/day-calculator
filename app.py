import streamlit as st
import time
from datetime import datetime, timedelta

# ИСПРАВЛЕННАЯ Страница Входа
def login_page():
    st.header("Добро пожаловать!")
    username = st.text_input("Введите ваше имя (Например, Константинов Ярослав")

    if st.button("Войти"):
        if username:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            # Устанавливаем время входа (timestamp)
            st.session_state['login_time'] = time.time()
            st.rerun()
        else:
            st.warning("Пожалуйста, введите имя, чтобы продолжить.")

# --- Данные о продуктах ---
PRODUCTS_DK = [
    "ДК", "Акт", "Трз", "Комбо/Кросс КК Одобрено", "Комбо/Кросс КК Выдано", "Трз.", "ЦП", "Гос.Уведомления", "Смарт", "Кешбек", "ЖКУ", "БС",
    "Инвесткопилка", "БС со Стратегией", "Токенизация", "Накопительный Счет",
    "Вклад", "Детская Кросс", "Сим-Карта", "Перевод Пенсии",
    "Селфи ДК", "Селфи КК"
]

PRODUCTS_KK = [
    "КК", "Акт", "Трз", "Кросс ДК", "ЦП", "Гос.Уведомления", "Смарт", "Кешбек", "ЖКУ", "БС",
    "Инвесткопилка", "БС со Стратегией", "Токенизация", "Накопительный Счет",
    "Вклад", "Детская Кросс", "Стикер Кросс", "Сим-Карта", "Перевод Пенсии",
    "Селфи ДК"
]

PRODUCTS_MP = [
    "МП", "ЦП", "Гос.Уведомления", "Смарт", "Кешбек", "ЖКУ", "БС", "Инвесткопилка",
    "БС со Стратегией", "Токенизация", "Накопительный Счет", "Вклад",
    "Детская Кросс", "Стикер Кросс", "Сим-Карта", "Перевод Пенсии", "Кросс ДК",
    "Селфи ДК", "Селфи КК"
]

PRODUCT_LISTS = {
    "ДК": PRODUCTS_DK,
    "КК": PRODUCTS_KK,
    "МП": PRODUCTS_MP
}

# --- Стили ---
def apply_styles():
    st.markdown("""
        <style>
            .main { background-color: #FFFFFF; }
            
            div.stButton > button {
                height: 50px;
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                background-color: #FFFFFF;
                color: #000000;
                font-family: 'Calibri', sans-serif;
                font-size: 16px;
                text-align: center;
            }
            div.stButton > button:hover {
                background-color: #F0F0F0;
                border-color: #AAAAAA;
            }
            .stToggle { font-family: 'Calibri', sans-serif; color: #000000; }
            .session-info {
                background-color: #F8F9FA;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 10px;
                font-size: 14px;
                color: #666;
            }
        </style>
    """, unsafe_allow_html=True)

# --- Функция проверки сессии ---
def check_session_validity():
    """Проверяет, не истекла ли сессия (24 часа)"""
    if 'login_time' not in st.session_state:
        return False
    
    current_time = time.time()
    login_time = st.session_state.get('login_time', 0)
    
    # 24 часа = 24 * 60 * 60 = 86400 секунд
    session_duration = 24 * 60 * 60
    
    if current_time - login_time > session_duration:
        # Сессия истекла
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.session_state.pop('login_time', None)
        return False
    
    return True

def get_session_time_left():
    """Возвращает оставшееся время сессии в читаемом формате"""
    if 'login_time' not in st.session_state:
        return "Неизвестно"
    
    current_time = time.time()
    login_time = st.session_state.get('login_time', 0)
    session_duration = 24 * 60 * 60
    
    time_left = session_duration - (current_time - login_time)
    
    if time_left <= 0:
        return "Сессия истекла"
    
    hours = int(time_left // 3600)
    minutes = int((time_left % 3600) // 60)
    
    return f"{hours}ч {minutes}мин"

# --- Логика состояний ---
def initialize_global_state():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    if 'user_data' not in st.session_state:
        st.session_state['user_data'] = {}
    if 'login_time' not in st.session_state:
        st.session_state['login_time'] = None

def get_user_state():
    username = st.session_state['username']
    if username not in st.session_state['user_data']:
        st.session_state['user_data'][username] = {
            'page': 'main',
            'toggles': {},
            'report_text': ""
        }
    return st.session_state['user_data'][username]

def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.session_state.pop('login_time', None)
    st.rerun()

def extend_session():
    """Продлевает сессию на 24 часа"""
    st.session_state['login_time'] = time.time()
    st.success("Сессия продлена на 24 часа!")
    time.sleep(1)
    st.rerun()

# --- Функции для переключения страниц ---
def go_to_page(page_name):
    user_state = get_user_state()
    user_state['toggles'] = {}
    user_state['page'] = page_name

def go_to_main():
    user_state = get_user_state()
    user_state['toggles'] = {}
    user_state['page'] = 'main'

def reset_all():
    user_state = get_user_state()
    user_state['page'] = 'main'
    user_state['toggles'] = {}
    user_state['report_text'] = ""

# --- Логика генерации отчета ---
def generate_report_text(main_product, toggles):
    product_list = PRODUCT_LISTS.get(main_product.upper())
    if not product_list:
        return ""
    report_lines = [f"{product} {'+' if toggles.get(product, False) else '-'}" for product in product_list]
    return "\n".join(report_lines)

# --- Компонент информации о сессии ---
def display_session_info():
    time_left = get_session_time_left()
    login_time = datetime.fromtimestamp(st.session_state.get('login_time', 0))
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.markdown(f'<div class="session-info">👤 Пользователь: {st.session_state["username"]}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="session-info">⏰ Осталось времени: {time_left}</div>', unsafe_allow_html=True)
    
    with col3:
        if st.button("Продлить", help="Продлить сессию на 24 часа"):
            extend_session()

# --- Страницы приложения ---
def main_page():
    st.header("Выберите основной продукт")

    left_space, main_content, right_space = st.columns([1, 4, 1])

    with main_content:
        st.button("ДК", on_click=go_to_page, args=('dk',), use_container_width=True)
        st.button("КК", on_click=go_to_page, args=('kk',), use_container_width=True)
        st.button("МП", on_click=go_to_page, args=('mp',), use_container_width=True)

def product_submenu_page(product_type, product_list):
    user_state = get_user_state()
    
    st.header(f"Дополнительные продукты для «{product_type}»")
    
    for product in product_list:
        user_state['toggles'][product] = st.toggle(
            product,
            value=user_state['toggles'].get(product, False),
            key=f"{st.session_state['username']}_{product_type}_{product}"
        )
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Сформировать отчет"):
            user_state['report_text'] = generate_report_text(product_type, user_state['toggles'])
            user_state['page'] = 'report'
            st.rerun()
            
    with col2:
        st.button("Вернуться", on_click=go_to_main)

def report_page():
    user_state = get_user_state()

    st.header("Сформированный отчет")
    
    report_text = user_state.get('report_text', "Отчет пуст.")
    
    st.text_area(
        label="Отчет для копирования:", 
        value=report_text, 
        height=300,
        help="Выделите текст и нажмите Ctrl+C (или Cmd+C), чтобы скопировать"
    )
    
    st.info("💡 Выделите текст выше и используйте Ctrl+C (Windows) или Cmd+C (Mac) для копирования")

    st.button("Сбросить", on_click=reset_all)

# --- Главная функция приложения ---
def main():
    apply_styles()
    initialize_global_state()

    # Проверяем валидность сессии
    if st.session_state.get('logged_in', False) and not check_session_validity():
        st.warning("Ваша сессия истекла. Пожалуйста, войдите снова.")
        time.sleep(2)
        st.rerun()

    if not st.session_state.get('logged_in', False):
        login_page()
    else:
        # Отображаем информацию о сессии
        display_session_info()
        
        # Кнопка выхода
        if st.button("Выйти", help="Завершить сессию"):
            logout()

        user_state = get_user_state()

        if user_state['page'] == 'main':
            main_page()
        elif user_state['page'] == 'dk':
            product_submenu_page("ДК", PRODUCTS_DK)
        elif user_state['page'] == 'kk':
            product_submenu_page("КК", PRODUCTS_KK)
        elif user_state['page'] == 'mp':
            product_submenu_page("МП", PRODUCTS_MP)
        elif user_state['page'] == 'report':
            report_page()

if __name__ == "__main__":
    main()
