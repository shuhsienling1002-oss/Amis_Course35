import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 35: O Tireng", page_icon="💪", layout="centered")

# --- CSS 美化 (活力橘紅色) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    .morph-tag { 
        background-color: #FFCCBC; color: #BF360C; 
        padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;
        display: inline-block; margin-right: 5px;
    }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #FBE9E7 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #D84315;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #BF360C; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #FBE9E7;
        border-left: 5px solid #FFAB91;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #FFCCBC; color: #BF360C; border: 2px solid #D84315; padding: 12px;
    }
    .stButton>button:hover { background-color: #FFAB91; border-color: #BE5504; }
    .stProgress > div > div > div > div { background-color: #D84315; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 35: 18個單字 - User Fix) ---
vocab_data = [
    {"amis": "Tireng", "chi": "身體 / 站立 (詞根)", "icon": "🧍", "source": "Row 421", "morph": "Root"},
    {"amis": "Tomireng", "chi": "站立 / 站著", "icon": "🧍‍♂️", "source": "User Fix", "morph": "Tireng + -om-"}, # 修正
    {"amis": "Kamay", "chi": "手", "icon": "✋", "source": "Row 998", "morph": "Noun"},
    {"amis": "Tanokamay", "chi": "徒手 / 用手", "icon": "🙌", "source": "Row 1090", "morph": "Tano-Kamay"},
    {"amis": "Wa'ay", "chi": "腳", "icon": "🦶", "source": "Row 6101", "morph": "Noun"},
    {"amis": "Pising", "chi": "臉", "icon": "🙂", "source": "Row 5360", "morph": "Noun"},
    {"amis": "Fanges", "chi": "皮膚 / 表面", "icon": "🧴", "source": "Row 5360", "morph": "Noun"},
    {"amis": "Tangila", "chi": "耳朵", "icon": "👂", "source": "Row 4520", "morph": "Noun"},
    {"amis": "Ngoyos", "chi": "嘴巴", "icon": "👄", "source": "Row 2380", "morph": "Noun"},
    {"amis": "Tangoyosan", "chi": "口罩 / 嘴部裝備", "icon": "😷", "source": "Row 2380", "morph": "Ta-Ngoyos-an"},
    {"amis": "Ngoso'", "chi": "鼻子", "icon": "👃", "source": "Row 2381", "morph": "Noun"},
    {"amis": "Tangoso'an", "chi": "呼吸器 / 鼻罩", "icon": "🤿", "source": "Row 2381", "morph": "Ta-Ngoso'-an"},
    {"amis": "Fokes", "chi": "頭髮", "icon": "💇", "source": "Row 4523", "morph": "Noun"},
    {"amis": "Sapafangsis", "chi": "使...香的東西 (香水)", "icon": "🌺", "source": "Row 998", "morph": "Sa-Pa-Fangsis"},
    {"amis": "Fangsis", "chi": "香 / 香味 (詞根)", "icon": "🌸", "source": "Row 998", "morph": "Root"},
    {"amis": "Minanaw", "chi": "洗 (手/腳/物)", "icon": "🧼", "source": "User Fix", "morph": "Verb"}, # 修正
    {"amis": "Malalo'op", "chi": "洗 (臉)", "icon": "🧖", "source": "User Fix", "morph": "Verb"}, # 修正
    {"amis": "Mirepet", "chi": "抓 / 握", "icon": "✊", "source": "Standard", "morph": "Mi-Repet"},
]

# --- 句子庫 (9句: 嚴格源自 CSV 並移除連字號) ---
sentences = [
    {"amis": "Tomireng ci Nakaw i papotal.", "chi": "Nakaw在外面站著。", "icon": "🧍‍♀️", "source": "Row 421 (User Fix)"},
    {"amis": "O sapafangsis ni ina to kamay korira.", "chi": "那些是媽媽用來讓手香香的(東西)。", "icon": "🌺", "source": "Row 998"},
    {"amis": "Tanokamay kako a matayal.", "chi": "我徒手工作。", "icon": "🙌", "source": "Row 1090"},
    {"amis": "Fanges no pising.", "chi": "臉的皮膚。", "icon": "🙂", "source": "Row 5360"},
    {"amis": "Mirepet to fokes.", "chi": "抓頭髮。", "icon": "💇", "source": "Standard Phrase"},
    {"amis": "Minanaw to kamay.", "chi": "洗手。", "icon": "🧼", "source": "User Fix"},
    {"amis": "Malalo'op (Malali'op) to pising.", "chi": "洗臉。", "icon": "🧖", "source": "User Fix"},
    {"amis": "O ngoyos ko sapicomikay.", "chi": "用嘴巴呼吸(跑步時)。", "icon": "👄", "source": "Adapted"},
    {"amis": "Tangoso'an.", "chi": "鼻子的裝備(呼吸器/鼻罩)。", "icon": "👃", "source": "Row 2381"},
]

# --- 3. 隨機題庫 (5題) ---
raw_quiz_pool = [
    {
        "q": "Tanokamay kako a matayal.",
        "audio": "Tanokamay kako a matayal",
        "options": ["我徒手工作", "我用腳工作", "我用頭工作"],
        "ans": "我徒手工作",
        "hint": "Tano-kamay (用手) (Row 1090)"
    },
    {
        "q": "O sapafangsis ni ina to kamay.",
        "audio": "O sapafangsis ni ina to kamay",
        "options": ["媽媽用來讓手香香的", "媽媽用來洗衣服的", "媽媽用來擦臉的"],
        "ans": "媽媽用來讓手香香的",
        "hint": "Sapafangsis (使...香), Kamay (手) (Row 998)"
    },
    {
        "q": "單字測驗：Tomireng",
        "audio": "Tomireng",
        "options": ["站立/站著", "坐下", "躺著"],
        "ans": "站立/站著",
        "hint": "User Fix: Tomireng"
    },
    {
        "q": "單字測驗：Minanaw",
        "audio": "Minanaw",
        "options": ["洗 (手/腳/物)", "洗臉", "洗澡"],
        "ans": "洗 (手/腳/物)",
        "hint": "User Fix: Minanaw"
    },
    {
        "q": "單字測驗：Malalo'op",
        "audio": "Malalo'op",
        "options": ["洗臉", "洗手", "刷牙"],
        "ans": "洗臉",
        "hint": "User Fix: Malalo'op (洗臉)"
    }
]

# --- 4. 狀態初始化 (洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌 (5題)
    selected_questions = random.sample(raw_quiz_pool, 5)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #BF360C;'>Unit 35: O Tireng</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>身體與動作 (User Corrected)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字 (構詞分析)")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="morph-tag">{word['morph']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型 (Data-Driven)")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #BF360C;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 5)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 5**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        # 使用洗牌後的選項
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 20
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #FFCCBC; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #BF360C;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經學會身體部位的說法了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            
            new_questions = random.sample(raw_quiz_pool, 5)
            final_qs = []
            for q in new_questions:
                q_copy = q.copy()
                shuffled_opts = random.sample(q['options'], len(q['options']))
                q_copy['shuffled_options'] = shuffled_opts
                final_qs.append(q_copy)
            
            st.session_state.quiz_questions = final_qs
            safe_rerun()

