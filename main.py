import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import random
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(page_title='Word Wise', page_icon='🤓', initial_sidebar_state='collapsed')

st.markdown("""
            <style>
            [data-testid="collapsedControl"] {
                display: none
            }
            .big-font {
                font-size:30px;
                font-weight: 600;
            }

            .title-big {
                font-size:50px;
                font-weight: 900;
                text-align: center;
            }
                                
            p {
                margin: 0rem;
            }

            .st-emotion-cache-uf99v8 {
                background: linear-gradient(45deg, #a9f4ff, #ecedc7);
            }

            [data-testid="collapsedControl"] {
                display: none
            }
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}    
            </style>
""", unsafe_allow_html=True)

st.markdown('<p class="title-big">Word-Wise</p>', unsafe_allow_html=True)

add_vertical_space(1)


if 'page' not in st.session_state:
    st.session_state.page = 1
if "words_and_definitions_old" not in st.session_state:
    st.session_state.words_and_definitions_old = {}

page = st.session_state.page


if page == 1:
    with st.form(clear_on_submit=True, key='Add_word'):
        col1, col2 = st.columns(2)
        word = col1.text_input('단어', key='word-input')
        definition = col2.text_input('뜻', key='definition-input')

            
        col1, col2, col3 = st.columns(3)
        if col2.form_submit_button('단어/뜻 리스트에 추가', use_container_width=1):
            st.session_state.words_and_definitions_old[word] = definition
            

    with st.expander('단어/뜻 리스트', expanded=False):
        for x in st.session_state.words_and_definitions_old:
            st.markdown(f'<p class="big-font">{x}</p>' + f'<p>{st.session_state.words_and_definitions_old[x]}</p>' , unsafe_allow_html=True)
            add_vertical_space(1)

    col1, col2, = st.columns(2)

    subjective = col1.checkbox('**주관식**(답을 스스로 작성)')

    if not subjective:
    
        col1a, col2a, col3a = st.columns(3)

        try:
            if len(st.session_state.words_and_definitions_old) <= 3:
                max_value_candidate_num = 3 
            elif len(st.session_state.words_and_definitions_old) == 4:
                max_value_candidate_num = 4
            else:
                max_value_candidate_num = 5
            
            candidate_num = col1a.number_input('**답 후보 개수**', min_value=2,max_value=len(st.session_state.words_and_definitions_old), value=max_value_candidate_num)
        except Exception as e: pass
    definition_based = col2.checkbox('**뜻 기반**(뜻을 보고 단어를 맞춤)')

    if st.button('게임 시작', use_container_width=1):
        if len(st.session_state.words_and_definitions_old) < 3:
            st.warning('단어와 뜻을 3개 이상 작성해주십시오.')
        else:
            if definition_based == True: st.session_state.words_and_definitions = {value: key for key, value in st.session_state.words_and_definitions_old.items()}
            else: st.session_state.words_and_definitions = st.session_state.words_and_definitions_old

            if subjective is not True:
                st.session_state.candidate_num = candidate_num
                result = f'''
                {subjective}  
                {candidate_num}  
                {definition_based}  
                '''
            else:
                result = f'''
                {subjective}  
                {definition_based}  
                '''

            if subjective == True: st.session_state.subjective = True

            elif subjective == False: st.session_state.subjective = False

            st.session_state.page = 2
            st.rerun()

# Word Based
if page == 2:
    st.divider()

    # 딕셔너리 선언
    words_and_definitions = st.session_state.words_and_definitions
    
    definitions = []

    if 'question_list' not in st.session_state:
        st.session_state.question_list = list(words_and_definitions.keys())

    try:
        question = random.choice(st.session_state.question_list)

        st.session_state.question = question

    
        for x in words_and_definitions:
            definitions.append(words_and_definitions[x])
        random.shuffle(definitions)

        st.session_state.definitions = definitions

        st.switch_page('C:/Users/yg201/바탕 화면/PyProject/AI-Streamlit/WordWise/pages/quiz.py')

    except IndexError:
        st.markdown("""
                    <style>         
                    p{
                        margin: 0px 0px 1rem;
                    } 
                    h3 {
                        margin: 0rem;
                    }
                    </style>
        """, unsafe_allow_html=True)

        st.success('단어 맞추기가 끝났습니다.')
        st.header('결과')
        

        correct_or_wrong = st.session_state.correct_or_wrong
        for x in correct_or_wrong:
            if correct_or_wrong[x] == 'Correct':
                st.subheader(f":blue[**{x}**: {correct_or_wrong[x]}]")
                
            else:
                with stylable_container(
                    key='Wrong',
                    css_styles='''
{
padding: 0.5rem 0px 0rem;
}'''
                ):
                    st.subheader(f":red[**{x}**: {correct_or_wrong[x]}]")
                st.write(f'''The answer is **{words_and_definitions[x]}**''')

        if st.button('홈으로 돌아가기'):
            st.session_state.page = 1
            del st.session_state.definitions, st.session_state.question, st.session_state.correct_or_wrong, st.session_state.question_list
            st.rerun()
