import streamlit as st
import clipboard

# --- НОВАЯ, БОЛЕЕ НАДЁЖНАЯ ФУНКЦИЯ ДЛЯ КОПИРОВАНИЯ ---
# Страница Входа

def login_page():
    st.header("Вход или Регистрация")
    # Поле для ввода имени (логина). Оно теперь единственное.
    username = st.text_input("Введите ваше имя (Например, Константинов Ярослав)")

    # Добавляем кнопку "Войти"
    if st.button("Войти / Зарегистрироваться"):
        # Новая проверка: просто смотрим, ввел ли пользователь имя.
        if username: # Если поле username не пустое
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            # st.rerun() перезагрузит страницу и покажет калькулятор.
            # Ваша функция get_user_state() сама создаст "личный блокнот", если нужно.
            st.rerun()
        else:
            # Если пользователь ничего не ввел, вежливо просим его это сделать.
            st.warning("Пожалуйста, введите имя, чтобы продолжить.")

# --- Данные о продуктах ---
PRODUCTS_DK = [
    "ДК", "Акт", "Трз", "Комбо/Кросс КК", "ЦП", "Смарт", "Кешбек", "ЖКУ", "БС",
    "Инвесткопилка", "БС со Стратегией", "Токенизация", "Накопительный Счет",
    "Вклад", "Детская Кросс", "Стикер Кросс", "Сим-Карта",
    "Селфи ДК", "Селфи КК"
]

PRODUCTS_KK = [
    "КК", "Акт", "Трз", "Кросс ДК", "ЦП", "Смарт", "Кешбек", "ЖКУ", "БС",
    "Инвесткопилка", "БС со Стратегией", "Токенизация", "Накопительный Счет",
    "Вклад", "Детская Кросс", "Стикер Кросс", "Сим-Карта",
    "Селфи ДК"
]

PRODUCTS_MP = [
    "МП", "ЦП", "Смарт", "Кешбек", "ЖКУ", "БС", "Инвесткопилка",
    "БС со Стратегией", "Токенизация", "Накопительный Счет", "Вклад",
    "Детская Кросс", "Стикер Кросс", "Сим-Карта", "Кросс ДК",
    "Селфи ДК", "Селфи КК"
]

PRODUCT_LISTS = {
    "ДК": PRODUCTS_DK,
    "КК": PRODUCTS_KK,
    "МП": PRODUCTS_MP
}

# --- Стили ---
# ИСПРАВЛЕННАЯ ВЕРСИЯ ФУНКЦИИ. СКОПИРУЙТЕ И ЗАМЕНИТЕ ЕЮ СТАРУЮ.
# ИСПРАВЛЕННАЯ ВЕРСИЯ ФУНКЦИИ СТИЛЕЙ. СКОПИРУЙТЕ И ЗАМЕНИТЕ ЕЮ СТАРУЮ.
def apply_styles():
    st.markdown("""
        <style>
            .main { background-color: #FFFFFF; }
            
            /* --- НОВЫЕ ПРАВИЛА ДЛЯ "КОРОБКИ" С КНОПКАМИ --- */
            
                
                /* 2. Ставим "коробку" ровно по центру с помощью магии auto-отступов */
                margin-left: auto;
                margin-right: auto;
                margin-top: 20px;

                /* 3. Ограничиваем максимальную ширину на очень больших экранах,
                   чтобы кнопки не были гигантскими. */
                max-width: 500px; 
            }
            
            /* --- НОВЫЕ ПРАВИЛА ДЛЯ САМИХ КНОПОК ВНУТРИ "КОРОБКИ" --- */
            

            /* --- ПРАВИЛА ДЛЯ МАЛЕНЬКИХ ЭКРАНОВ (ТЕЛЕФОНОВ) --- */
            /* Эта инструкция сработает, только если ширина экрана 600px или меньше */
            @media (max-width: 600px) {
                .main-menu-container {
                    /* На маленьких экранах делаем "коробку" чуть шире для удобства */
                    width: 95%; 
                }
            }

            /* --- Остальные стили для других элементов оставляем без изменений --- */
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
                background-color: [jg:пароль_(regexp)_150]
                border-color: #AAAAAA;
            }
            .stToggle { font-family: 'Calibri', sans-serif; color: #000000; }
            .report-text {
                font-family: 'Calibri', sans-serif;
                font-size: 16px;
                line-height: 1.8;
                border: 1px solid #DDDDDD;
                padding: 15px;
                border-radius: 8px;
                white-space: pre-wrap;
                background-color: #FAFAFA;
            }
        </style>
    """, unsafe_allow_html=True)

# --- Логика состояний (сессии) для МНОГИХ пользователей ---
def initialize_global_state():
    # Это создает "полку" для хранения блокнотов всех пользователей
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    if 'user_data' not in st.session_state:
        st.session_state['user_data'] = {}

def get_user_state():
    # Эта функция находит на "полке" личный блокнот текущего сотрудника
    username = st.session_state['username']
    if username not in st.session_state['user_data']:
        st.session_state['user_data'][username] = {
            'page': 'main',
            'toggles': {},
            'report_text': ""
        }
    return st.session_state['user_data'][username]

def logout():
    # Эта функция "закрывает сессию" - отправляет пользователя обратно к экрану входа
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.rerun()

# --- Функции для переключения страниц (НОВЫЕ ВЕРСИИ) ---
def go_to_page(page_name):
    # Теперь эта функция меняет страницу в ЛИЧНОМ блокноте пользователя
    user_state = get_user_state()
    user_state['toggles'] = {}
    user_state['page'] = page_name

def go_to_main():
    # То же самое для возврата на главную
    user_state = get_user_state()
    user_state['toggles'] = {}
    user_state['page'] = 'main'

def reset_all():
    # И сброс работает только для текущего пользователя
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
# НОВАЯ, НАДЕЖНАЯ ВЕРСИЯ ФУНКЦИИ main_page
def main_page():
    st.header("Выберите основной продукт")

    # 1. Создаем наш "умный стеллаж" из трёх колонок.
    # Мы делим ширину в пропорции 1:4:1.
    # Это значит, что центральная колонка будет в 4 раза шире боковых.
    # Боковые колонки будут пустыми "распорками".
    left_space, main_content, right_space = st.columns([1, 4, 1])

    # 2. Теперь мы говорим: "Всё, что дальше, клади в центральную колонку".
    with main_content:
        
        # 3. Создаем наши кнопки.
        # Ключевой параметр use_container_width=True заставляет кнопку
        # растянуться на ВСЮ ширину своей колонки.
        st.button(
            "ДК", 
            on_click=go_to_page, 
            args=('dk',), 
            use_container_width=True
        )
        
        st.button(
            "КК", 
            on_click=go_to_page, 
            args=('kk',), 
            use_container_width=True
        )
        
        st.button(
            "МП", 
            on_click=go_to_page, 
            args=('mp',), 
            use_container_width=True
        )
# Правильная версия страницы с продуктами
def product_submenu_page(product_type, product_list):
    # 1. Сначала получаем записную книжку текущего пользователя
    user_state = get_user_state()
    
    st.header(f"Дополнительные продукты для «{product_type}»")
    
    for product in product_list:
        # 2. Работаем с галочками из ЕГО книжки
        user_state['toggles'][product] = st.toggle(
            product,
            value=user_state['toggles'].get(product, False),
            key=f"{st.session_state.username}_{product_type}_{product}" # Уникальный ключ для каждого пользователя!
        )
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Сформировать отчет"):
            # 3. Генерируем отчет на основе ЕГО галочек
            user_state['report_text'] = generate_report_text(product_type, user_state['toggles'])
            user_state['page'] = 'report'
            st.rerun()
            
    with col2:
        st.button("Вернуться", on_click=go_to_main)

# НОВАЯ, ПОЛНОСТЬЮ ИСПРАВЛЕННАЯ ВЕРСИЯ report_page
def report_page():
    # 1. Получаем состояние текущего пользователя
    user_state = get_user_state()

    st.header("Сформированный отчет")
    
    # 2. Берем текст отчета
    report_text = user_state.get('report_text', "Отчет пуст.")
    
    # 3. Показываем текст отчета в блоке кода
    st.code(report_text)
    st.write("---")

    # 4. ВОТ ИСПРАВЛЕННЫЙ БЛОК КОПИРОВАНИЯ
    if st.button("Скопировать отчет"):
        clipboard.copy(report_text)
        st.success("Отчет скопирован в буфер обмена!")

    # 5. Кнопка "Сбросить"
    st.button("Сбросить", on_click=reset_all)


# --- Главная функция приложения ---
def main():
    apply_styles()
    initialize_global_state()

    # Сначала проверяем, вошел ли пользователь в систему
    if not st.session_state.get('logged_in'):
        login_page() # Если не вошел, показываем страницу входа
    else:
        # Если вошел, то показываем калькулятор
        
        # Добавим сбоку имя пользователя и кнопку "Выйти" для удобства
        st.sidebar.success(f"Вы вошли как: {st.session_state.username}")
        st.sidebar.button("Выйти", on_click=logout)

        # Получаем личную "записную книжку" текущего пользователя
        user_state = get_user_state()

        # А теперь показываем нужную страницу калькулятора
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
