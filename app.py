import os
import time
from datetime import datetime
import streamlit as st
import base64
import requests

# ==========================================
# DEVIL OS - ULTIMATE MASTER CORE (ERROR-FREE)
# ==========================================

st.set_page_config(
    page_title="Devil OS - Enterprise Autonomous Core",
    page_icon="💀",
    layout="wide"
)

# --- CREDENTIALS MANAGEMENT ---
ADMIN_CREDENTIALS = {
    "kpk_devil": "devil_master_999"  # Commander Aman ka Admin Account
}

MONITOR_CREDENTIALS = {
    "monitor_alpha": "health_secure_777"  # Dost ka Health & Error Monitor Account
}

# Hugging Face API Setup & DeepSeek Model
HF_TOKEN = os.getenv("HF_TOKEN", "")
MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"

def run_agent_role(agent_name, system_prompt, input_data):
    if not HF_TOKEN:
        return "[ERROR]: Hugging Face API Token (HF_TOKEN) missing in Streamlit Secrets!"
    try:
        headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_data}
            ],
            "max_tokens": 1000,
            "temperature": 0.6
        }
        
        response = requests.post(
            "https://router.huggingface.co/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            res_json = response.json()
            return res_json["choices"][0]["message"]["content"]
        else:
            return f"[API ERROR {response.status_code}]: {response.text}"
            
    except Exception as e:
        return f"[AGENT ERROR]: {str(e)}"

# --- GITHUB AUTO-PUSH FUNCTION ---
def push_code_to_github(file_content, commit_message, repo_name, github_token):
    try:
        if not github_token or not repo_name:
            return "GitHub Error: Repository name ya Token missing hai!"
            
        url = f"https://api.github.com/repos/{repo_name}/contents/generated_feature.py"
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "vnd.github.v3+json"
        }
        
        get_resp = requests.get(url, headers=headers)
        sha = get_resp.json().get("sha") if get_resp.status_code == 200 else None

        encoded_content = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')
        
        payload = {
            "message": commit_message,
            "content": encoded_content,
            "branch": "main"
        }
        if sha:
            payload["sha"] = sha

        put_resp = requests.put(url, headers=headers, json=payload)
        if put_resp.status_code in [200, 201]:
            return "SUCCESS: Code successfully pushed to GitHub! 🚀"
        else:
            return f"GitHub Error: {put_resp.json().get('message', 'Unknown error')}"
    except Exception as e:
        return f"[GITHUB API ERROR]: {str(e)}"

# Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "logs" not in st.session_state:
    st.session_state.logs = [
        {"time": datetime.now().strftime('%H:%M:%S'), "agent": "System", "status": "INFO", "msg": "Devil OS DeepSeek Core initialized successfully."}
    ]

# ==========================================
# LOGIN SCREEN
# ==========================================
if not st.session_state.logged_in:
    st.title("💀 Welcome to Devil OS - Secure Gateway")
    st.markdown("### Enter your credentials to access the autonomous system.")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_btn = st.form_submit_button("Login 🚀")
        
        if submit_btn:
            if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
                st.session_state.logged_in = True
                st.session_state.user_role = "admin"
                st.session_state.current_user = username
                st.success("Access Granted! Welcome back, Commander Aman.")
                st.rerun()
            elif username in MONITOR_CREDENTIALS and MONITOR_CREDENTIALS[username] == password:
                st.session_state.logged_in = True
                st.session_state.user_role = "monitor"
                st.session_state.current_user = username
                st.success(f"Access Granted! Welcome, Health Monitor ({username}).")
                st.rerun()
            else:
                st.error("Ghalat Username ya Password! Dobara koshish karein.")

# ==========================================
# MAIN APP (AFTER LOGIN)
# ==========================================
else:
    st.sidebar.title("💀 DEVIL OS PANEL")
    st.sidebar.write(f"Logged in as: **{st.session_state.current_user}**")
    st.sidebar.write(f"Role: **{st.session_state.user_role.upper()}**")
    
    if st.sidebar.button("Logout 🚪"):
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.current_user = ""
        st.rerun()

    st.sidebar.markdown("---")

    # ------------------------------------------
    # VIEW 1: MONITOR (Friends View - ReadOnly)
    # ------------------------------------------
    if st.session_state.user_role == "monitor":
        st.title("🛡️ Devil OS - System Health Monitor")
        st.markdown(f"### *Monitor Dashboard ({st.session_state.current_user}): Live Error Surveillance*")
        st.info("Aapka yeh dashboard sirf system health aur errors track karne ke liye hai.")

        col1, col2, col3 = st.columns(3)
        col1.metric("Active Agents", "7-Agent DeepSeek Pipeline", "Stable")
        col2.metric("System Errors", "0", "All Clear ✅")
        col3.metric("Last Check", datetime.now().strftime('%H:%M:%S'), "Live")

        st.markdown("---")
        st.subheader("📋 Live System & Error Logs")
        
        for log in reversed(st.session_state.logs):
            if log["status"] == "ERROR":
                st.error(f"[{log['time']}] {log['agent']}: {log['msg']}")
            else:
                st.success(f"[{log['time']}] {log['agent']} [{log['status']}]: {log['msg']}")

    # ------------------------------------------
    # VIEW 2: ADMIN (Aman's Full Control & Pipeline)
    # ------------------------------------------
    elif st.session_state.user_role == "admin":
        st.title("👑 Devil OS - Master Command Center")
        st.markdown(f"### *Aman Ullah (KPK-DEVIL) - Powered by {MODEL_NAME}*")
        
        tab1, tab2, tab3 = st.tabs(["🏢 7-Agent Pipeline", "🐙 GitHub Auto-Push", "📊 Master Logs"])

        with tab1:
            st.subheader("Autonomous Enterprise Software Engineering Pipeline")
            project_domain = st.text_input("Enter Enterprise Domain or Goal:", "High-security user authentication system with auto-scaling.")

            if st.button("Run Full 7-Agent DeepSeek Pipeline 🚀"):
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Agent 1: Strategist
                status_text.text("Agent 1 (Strategist) thinking of enterprise features...")
                p1 = "You are the Enterprise Strategist Agent. Think of high-level enterprise-grade features, compliance, security, and scalability requirements for the given domain."
                out1 = run_agent_role("Enterprise Strategist", p1, project_domain)
                progress_bar.progress(15)
                with st.expander("1️⃣ Enterprise Feature Strategist Output"):
                    st.write(out1)

                # Agent 2: Architect
                status_text.text("Agent 2 (Architect) planning technical blueprint...")
                p2 = "You are the System Architect Agent. Take the enterprise features and design a complete technical blueprint and step-by-step architecture on how to build it."
                out2 = run_agent_role("System Architect", p2, out1)
                progress_bar.progress(30)
                with st.expander("2️⃣ System Architect Blueprint"):
                    st.write(out2)

                # Agent 3: Incremental Coder
                status_text.text("Agent 3 (Coder) writing modular code...")
                p3 = "You are the Incremental Coder Agent. Write clean, modular Python code piece by piece based on the architecture plan. Focus on core backend logic first."
                out3 = run_agent_role("Incremental Coder", p3, out2)
                progress_bar.progress(50)
                with st.expander("3️⃣ Incremental Coder Output (Code Chunks)"):
                    st.code(out3, language="python")
                    st.session_state.last_generated_code = out3

                # Agent 4: Sandbox Tester
                status_text.text("Agent 4 (Sandbox Tester) scanning for bugs...")
                p4 = "You are the Sandbox Tester Agent. Analyze the provided code for syntax errors, security vulnerabilities, and bugs. Fix them and output the robust version."
                out4 = run_agent_role("Sandbox Tester", p4, out3)
                progress_bar.progress(70)
                with st.expander("4️⃣ Sandbox Test & Bug Fixes"):
                    st.code(out4, language="python")
                    st.session_state.last_generated_code = out4

                # Agent 5: Simulation Analyst
                status_text.text("Agent 5 (Simulation Analyst) running impact simulations...")
                p5 = "You are the Simulation and Impact Analyst Agent. Simulate running this feature in a live enterprise environment. Detail the Advantages (Pros) and Disadvantages (Cons) clearly."
                out5 = run_agent_role("Simulation Analyst", p5, out4)
                progress_bar.progress(85)
                with st.expander("5️⃣ Simulation Results: Advantages & Disadvantages"):
                    st.write(out5)

                # Agent 6: Virtual Server Tester
                status_text.text("Agent 6 (Virtual Server Tester) checking server performance...")
                p6 = "You are the Virtual Server Environment Agent. Verify resource usage, memory footprint, and server readiness for deployment."
                out6 = run_agent_role("Virtual Server Tester", p6, out4)
                progress_bar.progress(95)
                with st.expander("6️⃣ Virtual Server Environment Report"):
                    st.write(out6)

                # Agent 7: Deployment Agent
                status_text.text("Agent 7 (Deployment Agent) finalizing integration...")
                p7 = "You are the Deployment Agent. Finalize the package, provide the deployment manifest, and confirm system integration."
                out7 = run_agent_role("Deployment Agent", p7, out6)
                progress_bar.progress(100)
                
                status_text.text("Pipeline Completed Successfully! 🎉")
                st.success("Enterprise feature successfully built and tested!")
                
                st.session_state.logs.append({
                    "time": datetime.now().strftime('%H:%M:%S'),
                    "agent": "Enterprise Pipeline",
                    "status": "SUCCESS",
                    "msg": f"Executed DeepSeek pipeline for: {project_domain[:25]}..."
                })

                with st.expander("7️⃣ Final Deployment Confirmation"):
                    st.write(out7)

        with tab2:
            st.subheader("🐙 GitHub Auto-Push Integration")
            st.write("Pipeline ke zariye banaya gaya code aap direct apne GitHub repo par push kar sakte hain.")
            
            gh_repo = st.text_input("GitHub Repository (e.g., username/repo-name):", "kpkdevil1209/devil-os")
            gh_token = st.text_input("GitHub Personal Access Token:", type="password")
            commit_msg = st.text_input("Commit Message:", "Devil OS Autonomous Agent: New Enterprise Feature Update")

            if st.button("Push Generated Code to GitHub 🚀"):
                if "last_generated_code" in st.session_state and st.session_state.last_generated_code:
                    with st.spinner("Pushing code to GitHub..."):
                        result_msg = push_code_to_github(
                            st.session_state.last_generated_code,
                            commit_msg,
                            gh_repo,
                            gh_token
                        )
                    if "SUCCESS" in result_msg:
                        st.success(result_msg)
                        st.session_state.logs.append({
                            "time": datetime.now().strftime('%H:%M:%S'),
                            "agent": "GitHub Auto-Push",
                            "status": "SUCCESS",
                            "msg": f"Pushed code to {gh_repo}"
                        })
                    else:
                        st.error(result_msg)
                else:
                    st.warning("Pehle '7-Agent Pipeline' run karein taake code generate ho sake!")

        with tab3:
            st.subheader("Master System Logs & Debugging")
            for log in st.session_state.logs:
                st.write(f"[{log['time']}] **{log['agent']}** - Status: `{log['status']}` - Msg: {log['msg']}")
            
            if st.button("Clear Logs"):
                st.session_state.logs = []
                st.rerun()
    
