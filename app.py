import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard

# ИСПРАВЛЕННАЯ Страница Входа
def login_page():
    st.header("Добро пожаловать!")
    username = st.text_input("Введите ваше имя (Например, Константинов Ярослав)")

    if st.button("Войти"):
        if username:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
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
        </style>
    """, unsafe_allow_html=True)

# --- Логика состояний ---
def initialize_global_state():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    if 'user_data' not in st.session_state:
        st.session_state['user_data'] = {}

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
    
    # Заголовок и кнопка копирования в одной строке
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.subheader("📋 Отчет для копирования:")
    
    with col2:
        # Красивая кнопка копирования от st-copy-to-clipboard
        if st_copy_to_clipboard(report_text, before_copy_label="📋 Копировать", after_copy_label="✅ Скопировано!"):
            st.success("Отчет скопирован в буфер обмена!")
    
    # Блок с кодом (также имеет встроенный значок копирования)
    st.code(report_text, language=None)
    
    st.info("💡 Используйте кнопку '📋 Копировать' выше или значок копирования в правом углу блока")

    st.button("Сбросить", on_click=reset_all)

# --- Главная функция приложения ---
def main():
    apply_styles()
    initialize_global_state()

    if not st.session_state.get('logged_in', False):
        login_page()
    else:
        st.write(f"Вы вошли как: {st.session_state['username']}")
        st.button("Выйти", on_click=logout)

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
