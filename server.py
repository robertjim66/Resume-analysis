#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
import os
import sys
from openai import OpenAI

PORT = 8000

class ResumeHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # 发送HTTP响应头
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        # 创建HTML响应
        html = """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AIPM 简历分析智能助手</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                .form-group {
                    margin-bottom: 15px;
                }
                label {
                    display: block;
                    margin-bottom: 5px;
                    font-weight: bold;
                }
                input[type="text"],
                input[type="password"],
                select,
                textarea {
                    width: 100%;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    font-size: 16px;
                }
                textarea {
                    height: 150px;
                }
                button {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 16px;
                }
                button:hover {
                    background-color: #45a049;
                }
                .result {
                    margin-top: 20px;
                    padding: 15px;
                    background-color: #f0f8ff;
                    border: 1px solid #add8e6;
                    border-radius: 4px;
                    white-space: pre-wrap;
                }
                .error {
                    margin-top: 20px;
                    padding: 15px;
                    background-color: #ffebee;
                    border: 1px solid #ffcdd2;
                    border-radius: 4px;
                    color: #c62828;
                }
            </style>
        </head>
        <body>
            <h1>AIPM 简历分析智能助手</h1>
            <p>这是一个基于AI的简历分析工具，帮助AI产品经理分析自己的简历并给出建议。</p>
            
            <form method="POST" action="/">
                <div class="form-group">
                    <label for="api_key">API Key:</label>
                    <input type="password" id="api_key" name="api_key" placeholder="请输入你的API Key">
                </div>
                
                <div class="form-group">
                    <label for="target_position">目标岗位:</label>
                    <select id="target_position" name="target_position">
                        <option value="AI产品经理">AI产品经理</option>
                        <option value="AI产品运营">AI产品运营</option>
                        <option value="AI解决方案">AI解决方案</option>
                        <option value="大模型应用产品经理">大模型应用产品经理</option>
                        <option value="AI训练师">AI训练师</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="jd_text">JD内容:</label>
                    <textarea id="jd_text" name="jd_text" placeholder="请输入JD内容"></textarea>
                </div>
                
                <div class="form-group">
                    <label for="resume_text">简历内容:</label>
                    <textarea id="resume_text" name="resume_text" placeholder="请输入简历内容"></textarea>
                </div>
                
                <button type="submit">开始分析</button>
            </form>
        </body>
        </html>
        """
        
        # 发送响应内容
        self.wfile.write(html.encode('utf-8'))
    
    def do_POST(self):
        # 获取表单数据
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        # 解析表单数据
        form_data = {}
        import urllib.parse
        for pair in post_data.split('&'):
            key, value = pair.split('=', 1)
            key = urllib.parse.unquote_plus(key)
            value = urllib.parse.unquote_plus(value)
            form_data[key] = value
        
        # 提取表单字段
        api_key = form_data.get('api_key', '')
        target_position = form_data.get('target_position', '')
        jd_text = form_data.get('jd_text', '')
        resume_text = form_data.get('resume_text', '')
        
        # 发送HTTP响应头
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        # 创建HTML响应
        html = """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AIPM 简历分析智能助手</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                .form-group {
                    margin-bottom: 15px;
                }
                label {
                    display: block;
                    margin-bottom: 5px;
                    font-weight: bold;
                }
                input[type="text"],
                input[type="password"],
                select,
                textarea {
                    width: 100%;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    font-size: 16px;
                }
                textarea {
                    height: 150px;
                }
                button {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 16px;
                }
                button:hover {
                    background-color: #45a049;
                }
                .result {
                    margin-top: 20px;
                    padding: 15px;
                    background-color: #f0f8ff;
                    border: 1px solid #add8e6;
                    border-radius: 4px;
                    white-space: pre-wrap;
                }
                .error {
                    margin-top: 20px;
                    padding: 15px;
                    background-color: #ffebee;
                    border: 1px solid #ffcdd2;
                    border-radius: 4px;
                    color: #c62828;
                }
            </style>
        </head>
        <body>
            <h1>AIPM 简历分析智能助手</h1>
            <p>这是一个基于AI的简历分析工具，帮助AI产品经理分析自己的简历并给出建议。</p>
            
            <form method="POST" action="/">
                <div class="form-group">
                    <label for="api_key">API Key:</label>
                    <input type="password" id="api_key" name="api_key" placeholder="请输入你的API Key">
                </div>
                
                <div class="form-group">
                    <label for="target_position">目标岗位:</label>
                    <select id="target_position" name="target_position">
                        <option value="AI产品经理">AI产品经理</option>
                        <option value="AI产品运营">AI产品运营</option>
                        <option value="AI解决方案">AI解决方案</option>
                        <option value="大模型应用产品经理">大模型应用产品经理</option>
                        <option value="AI训练师">AI训练师</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="jd_text">JD内容:</label>
                    <textarea id="jd_text" name="jd_text" placeholder="请输入JD内容"></textarea>
                </div>
                
                <div class="form-group">
                    <label for="resume_text">简历内容:</label>
                    <textarea id="resume_text" name="resume_text" placeholder="请输入简历内容"></textarea>
                </div>
                
                <button type="submit">开始分析</button>
            </form>
        """
        
        # 处理分析逻辑
        try:
            if not all([api_key, jd_text, resume_text]):
                html += '<div class="error">请填写完整信息</div>'
            else:
                # 使用AI分析简历
                result = analyze_resume_with_AI(resume_text, jd_text, target_position, api_key)
                html += f'<div class="result"><strong>分析结果:</strong>\n{result}</div>'
        except Exception as e:
            html += f'<div class="error">发生错误: {str(e)}</div>'
        
        html += """
        </body>
        </html>
        """
        
        # 发送响应内容
        self.wfile.write(html.encode('utf-8'))

def analyze_resume_with_AI(resume_text: str, jd_text: str, target_position: str, api_key: str) -> str:
    """
    使用AI分析简历内容
    :param resume_text: 简历文本内容
    :param jd_text: 职位JD文本内容
    :param target_position: 目标岗位
    :param api_key: OpenAI API Key
    :return: AI分析结果
    """
    if not resume_text:
        return "请输入简历内容"
    if not jd_text:
        return "请输入JD内容"
    if not target_position:
        return "请输入目标岗位"
    if not api_key:
        return "请输入你的OpenAI API Key"

    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        prompt = f"请基于以下候选人简历文本、目标岗位和JD文本，生成一份结构清晰、核心信息用表格呈现的岗位匹配度分析报告，严格遵循以下模块和格式要求：\n\n### 输入材料\n1. 候选人简历文本：{resume_text}\n2. 目标岗位：{target_position}\n3. 目标岗位 JD 文本：{jd_text}\n\n### 输出格式要求\n---\n## 一、评分与分析理由板块\n1. **整体评分**：给出0-10分的综合得分\n2. **综合评价**：150字左右的总述，突出匹配亮点与核心短板\n3. **维度拆解分析**：必须用表格呈现，表格列固定为「维度|评分 (/10)|分析理由」，维度包含：\n   - 岗位匹配度\n   - 工作经验相关性\n   - 技能掌握程度\n   - 教育背景契合度\n   - 软技能与岗位适配性\n4. **主要差距总结**：用项目符号列出3-5条最核心的不匹配点\n\n---\n## 二、对照岗位 JD 逐条修改简历板块\n必须用表格呈现，表格列固定为「简历现有内容|岗位 JD 要求|差异分析|修改建议」，需将简历中所有与 JD 相关的条目逐一对应分析，并给出可直接替换的改写话术。\n\n---\n## 三、面试可能问的问题板块\n列出8-10个高针对性问题，每个问题后用「⚠️」标注考察点，例如：\n1. 你在实习中提到「构建多维度测评体系」，能否详细说明你是如何定义「准确性」和「逻辑性」的？⚠️ 考察数据质量把控能力和标准化思维\n\n---\n## 四、职业发展路径板块\n分「短期 (1-3年)」「中期 (3-5年)」「长期 (5年以上)」三个阶段，每个阶段包含：\n- 目标职位\n- 核心任务 / 能力升级重点\n- 行动建议（用「✅」标注具体动作）\n\n---\n## 五、结语建议板块\n给候选人的投递/面试策略总结，3-4条可落地的行动建议。\n\n---\n### 格式约束\n- 所有对比类、评分类内容必须用表格呈现，禁止纯文本堆砌\n- 每个板块用「---」分隔，标题用「#」「##」分级，保持视觉清晰\n- 语言需专业、简洁，避免冗余表述\n\n要求分析全面、具体，避免模板化回复，完全基于提供的JD和简历内容"

        response = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "你是专业简历分析助手，具有5年以上招聘经验，对AI产品经理等岗位有深入理解"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI分析时出错: {str(e)}"

def main():
    # 启动HTTP服务器
    with socketserver.TCPServer(("", PORT), ResumeHandler) as httpd:
        print(f"服务器运行在 http://localhost:{PORT}")
        print(f"请在浏览器中访问 http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    main()
