import streamlit as st
from openai import OpenAI
# 注意：即使不直接写 httpx.Client，
# 也要确保 requirements.txt 里有 openai，它会自动处理连接。

# --- 1. DeepSeek API 配置 ---
# 从 Secrets 保险箱读取 Key
DEEPSEEK_API_KEY = st.secrets["DEEPSEEK_KEY"]

# 这里我们恢复最标准、最简洁的写法
client = OpenAI(
    api_key=DEEPSEEK_API_KEY, 
    base_url="https://api.deepseek.com"
)

# --- 后面的代码保持不变 ---

# --- 2. 网页页面设置 ---
st.set_page_config(page_title="DeepSeek 健康助手", layout="centered")
st.title("🤖 AI 智能健康管理专家")
st.caption("由 DeepSeek 大模型驱动 | 丝滑访问免代理")

# --- 3. 界面布局 ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 输入数据")
    height = st.number_input("身高 (cm)", min_value=1.0, max_value=250.0, value=170.0)
    weight = st.number_input("体重 (kg)", min_value=1.0, max_value=300.0, value=65.0)
    
    # 按钮：提交
    submit = st.button("生成 AI 建议", use_container_width=True)

with col2:
    st.subheader("📊 分析结果")
    
    if submit:
        # 计算 BMI
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        
        # 显示大数字指标
        st.metric(label="你的 BMI 指数", value=f"{bmi:.1f}")
        
        # 进度条可视化 (BMI 10-40 范围映射)
        progress_val = min(max((bmi - 10) / 30, 0.0), 1.0)
        st.progress(progress_val)
        st.caption("范围：10 (偏瘦) <---> 40 (肥胖)")

        # --- 4. 调用 DeepSeek 接口 ---
        with st.spinner('DeepSeek 正在全力思考中...'):
            try:
                # 构造指令
                response = client.chat.completions.create(
                    model="deepseek-chat", # 使用 DeepSeek 的聊天模型
                    messages=[
                        {"role": "system", "content": "你是一位经验丰富的私人健身教练和营养师，说话幽默且专业。"},
                        {"role": "user", "content": f"我的身高是 {height}cm，体重是 {weight}kg，BMI 是 {bmi:.1f}。请给我简短的评价，并提供一条具体的饮食建议和一条运动建议，总字数在 150 字以内。"}
                    ],
                    stream=False # 关闭流式传输，一次性获取完整回复
                )
                
                # 获取 AI 的回复文本
                ai_advice = response.choices[0].message.content
                
                st.markdown("---")
                st.success("✨ AI 教练的私房话：")
                st.write(ai_advice)
                
            except Exception as e:
                st.error("糟糕，连接 AI 服务器时出了点小状况：")
                st.info(f"错误详情：{e}")
    else:
        st.write("👈 请在左侧填写数据，开启你的健康之旅。")

# --- 底部版权声明 ---
st.divider()

st.caption("©️ 2026 我的第一个 AI 网站 | 保持运动，热爱生活")


