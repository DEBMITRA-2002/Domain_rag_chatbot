import streamlit as st

from rag_pipeline import RAGPipeline


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="DocuMind | RAG Chatbot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(
            circle at top left,
            rgba(99, 102, 241, 0.18),
            transparent 35%
        ),
        radial-gradient(
            circle at bottom right,
            rgba(139, 92, 246, 0.12),
            transparent 35%
        ),
        #0b1020;
    color: #f8fafc;
}


/* Hide Streamlit default branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* Main container */

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* =========================================================
   HERO
   ========================================================= */

.hero-box {
    padding: 35px;
    border-radius: 25px;
    background: linear-gradient(
        135deg,
        #1e293b,
        #312e81
    );
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 20px 50px rgba(0,0,0,0.35);
    margin-bottom: 30px;
}

.hero-title {
    font-size: 46px;
    font-weight: 800;
    color: #a78bfa;
    letter-spacing: -1px;
    margin-bottom: 10px;
}

.hero-text {
    font-size: 18px;
    color: #cbd5e1;
    line-height: 1.6;
}


/* =========================================================
   HEADINGS
   ========================================================= */

h1,
h2,
h3 {
    color: #f8fafc !important;
}


/* =========================================================
   FILE UPLOADER
   ========================================================= */

[data-testid="stFileUploader"] {
    background: rgba(30, 41, 59, 0.70);
    border: 1px dashed rgba(167, 139, 250, 0.65);
    border-radius: 18px;
    padding: 12px;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: none;
    padding: 0.7rem 1rem;
    font-weight: 700;
    color: white;

    background: linear-gradient(
        135deg,
        #6366f1,
        #8b5cf6
    );

    transition: all 0.2s ease;
}

.stButton > button:hover {
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.35);
    transform: translateY(-2px);
}


/* =========================================================
   CHAT MESSAGES
   ========================================================= */

[data-testid="stChatMessage"] {
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(30,41,59,0.65);
}


/* =========================================================
   CHAT INPUT
   ========================================================= */

[data-testid="stChatInput"] {
    border-radius: 16px;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0f172a,
        #111827
    );

    border-right: 1px solid rgba(255,255,255,0.08);
}


/* =========================================================
   SOURCE CARDS
   ========================================================= */

.source-box {
    background: #111827;
    border: 1px solid rgba(167,139,250,0.25);
    border-radius: 12px;
    padding: 12px;
    margin: 6px 0;
}

.source-title {
    font-weight: 700;
    color: #ddd6fe;
}

.source-page {
    color: #94a3b8;
    font-size: 13px;
    margin-top: 3px;
}


/* =========================================================
   DOCUMENT CARDS
   ========================================================= */

.document-card {
    padding: 18px;
    border-radius: 16px;
    background: rgba(30,41,59,0.70);
    border: 1px solid rgba(167,139,250,0.18);
    margin-bottom: 10px;
}

.document-title {
    font-size: 17px;
    font-weight: 700;
    color: #f8fafc;
}

.document-status {
    color: #86efac;
    font-size: 13px;
    margin-top: 5px;
}


/* =========================================================
   STATUS BOX
   ========================================================= */

.status-box {
    padding: 15px 18px;
    border-radius: 14px;
    background: rgba(30,41,59,0.70);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 15px;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "rag_pipeline" not in st.session_state:

    st.session_state.rag_pipeline = RAGPipeline()


if "processed_files" not in st.session_state:

    st.session_state.processed_files = []


if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("📚 DocuMind")

    st.caption(
        "Domain-Specific Retrieval-Augmented Generation"
    )

    st.divider()

    st.subheader("⚙️ Workspace")

    if st.session_state.processed_files:

        st.success(
            "🟢 Documents Ready"
        )

        st.caption(
            f"{len(st.session_state.processed_files)} "
            "document(s) loaded"
        )

    else:

        st.info(
            "⚪ No documents loaded"
        )

    st.divider()

    if st.button(
        "🔄 Clear Conversation",
        use_container_width=True
    ):

        st.session_state.chat_history = []

        st.rerun()

    st.divider()

    st.caption(
        "FAISS • Sentence Transformers • Groq"
    )


# =========================================================
# HERO SECTION
# =========================================================

st.markdown(
    '<div class="hero-box">'
    '<div class="hero-title">📚 DocuMind</div>'
    '<div class="hero-text">'
    'Ask questions about your PDF documents and get '
    'grounded answers with document and page references.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# DOCUMENT UPLOAD
# =========================================================

st.subheader("📄 Your Documents")

uploaded_files = st.file_uploader(
    "Upload one or more PDF documents",
    type=["pdf"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)


# =========================================================
# SELECTED FILES
# =========================================================

if uploaded_files:

    st.markdown(
        f"""
        <div class="status-box">
            📚 <strong>{len(uploaded_files)}</strong>
            PDF file(s) selected
        </div>
        """,
        unsafe_allow_html=True
    )

    for file in uploaded_files:

        st.write(
            f"📄 {file.name}"
        )


    # =====================================================
    # PROCESS DOCUMENTS
    # =====================================================

    if st.button(
        "⚡ Process Documents",
        use_container_width=True
    ):

        with st.spinner(
            "🔄 Reading documents and building knowledge base..."
        ):

            try:

                chunks = (
                    st.session_state
                    .rag_pipeline
                    .load_pdfs(uploaded_files)
                )

                st.session_state.processed_files = [
                    file.name
                    for file in uploaded_files
                ]

                st.session_state.chat_history = []

                st.success(
                    "✅ Knowledge base created successfully!"
                )

                st.info(
                    f"📦 {len(chunks)} text chunks indexed."
                )

            except Exception as e:

                st.error(
                    f"❌ Error while processing documents: {e}"
                )


# =========================================================
# KNOWLEDGE BASE
# =========================================================

if st.session_state.processed_files:

    st.divider()

    st.subheader("📚 Knowledge Base")

    number_of_columns = min(
        len(st.session_state.processed_files),
        3
    )

    columns = st.columns(
        number_of_columns
    )

    for index, file_name in enumerate(
        st.session_state.processed_files
    ):

        with columns[index % number_of_columns]:

            st.markdown(
                f"""
                <div class="document-card">

                    <div class="document-title">
                        📄 {file_name}
                    </div>

                    <div class="document-status">
                        ● Ready for Questions
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# CHAT SECTION
# =========================================================

if st.session_state.processed_files:

    st.divider()

    st.subheader(
        "💬 Ask Your Documents"
    )


    # =====================================================
    # CHAT HISTORY
    # =====================================================

    for chat in st.session_state.chat_history:

        # User message
        with st.chat_message(
            "user",
            avatar="👤"
        ):

            st.write(
                chat["question"]
            )


        # Assistant message
        with st.chat_message(
            "assistant",
            avatar="🤖"
        ):

            st.write(
                chat["answer"]
            )


            # ---------------------------------------------
            # SOURCES
            # ---------------------------------------------

            if chat["sources"]:

                with st.expander(
                    "📚 Sources & References"
                ):

                    displayed_sources = set()

                    for source in chat["sources"]:

                        source_key = (
                            source["source"],
                            source["page"]
                        )

                        if source_key not in displayed_sources:

                            displayed_sources.add(
                                source_key
                            )

                            st.markdown(
                                f"""
                                <div class="source-box">

                                    <div class="source-title">
                                        📄 {source["source"]}
                                    </div>

                                    <div class="source-page">
                                        📑 Page {source["page"]}
                                    </div>

                                </div>
                                """,
                                unsafe_allow_html=True
                            )


    # =====================================================
    # CHAT INPUT
    # =====================================================

    question = st.chat_input(
        "Ask something about your documents..."
    )


    # =====================================================
    # PROCESS QUESTION
    # =====================================================

    if question:

        # ---------------------------------------------
        # USER MESSAGE
        # ---------------------------------------------

        with st.chat_message(
            "user",
            avatar="👤"
        ):

            st.write(
                question
            )


        # ---------------------------------------------
        # ASSISTANT RESPONSE
        # ---------------------------------------------

        with st.chat_message(
            "assistant",
            avatar="🤖"
        ):

            with st.spinner(
                "🔎 Searching your documents..."
            ):

                try:

                    answer, sources = (
                        st.session_state
                        .rag_pipeline
                        .ask_question(
                            question,
                            top_k=3
                        )
                    )


                    # Display answer
                    st.write(
                        answer
                    )


                    # -------------------------------------
                    # DISPLAY SOURCES
                    # -------------------------------------

                    if sources:

                        with st.expander(
                            "📚 Sources & References"
                        ):

                            displayed_sources = set()

                            for source in sources:

                                source_key = (
                                    source["source"],
                                    source["page"]
                                )

                                if source_key not in displayed_sources:

                                    displayed_sources.add(
                                        source_key
                                    )

                                    st.markdown(
                                        f"""
                                        <div class="source-box">

                                            <div class="source-title">
                                                📄 {source["source"]}
                                            </div>

                                            <div class="source-page">
                                                📑 Page {source["page"]}
                                            </div>

                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )


                    # -------------------------------------
                    # SAVE CHAT
                    # -------------------------------------

                    st.session_state.chat_history.append(
                        {
                            "question": question,
                            "answer": answer,
                            "sources": sources
                        }
                    )


                except Exception as e:

                    st.error(
                        f"❌ Error while generating answer: {e}"
                    )


# =========================================================
# EMPTY STATE
# =========================================================

else:

    st.divider()

    st.info(
        "👋 Welcome to DocuMind! "
        "Upload your PDF documents above, "
        "process them, and start asking questions."
    )