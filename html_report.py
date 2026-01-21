import markdown
from datetime import datetime

# 定义语义化、简洁高级的HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="专业的简历分析报告，包含岗位匹配度评分、改进建议等">
    <title>简历分析报告</title>
    <style>
        /* 全局样式重置 */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        /* 基础样式 */
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.7;
            color: #2d3748;
            background-color: #f7fafc;
            padding: 20px;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        /* 主容器 */
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        /* 头部区域 */
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 48px 40px;
            text-align: center;
        }
        
        header h1 {
            font-size: 2.8rem;
            margin-bottom: 12px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        
        header .subtitle {
            font-size: 1.125rem;
            opacity: 0.95;
            margin-bottom: 24px;
            font-weight: 400;
        }
        
        header .date {
            font-size: 0.9375rem;
            opacity: 0.9;
            font-weight: 300;
        }
        
        /* 内容区域 */
        main {
            padding: 40px;
        }
        
        /* 标题样式 */
        h2 {
            color: #1a202c;
            font-size: 1.875rem;
            margin-bottom: 32px;
            padding-bottom: 12px;
            border-bottom: 3px solid #e2e8f0;
            font-weight: 700;
            letter-spacing: -0.3px;
        }
        
        h3 {
            color: #2d3748;
            font-size: 1.5rem;
            margin: 40px 0 24px;
            font-weight: 600;
        }
        
        /* 段落样式 */
        p {
            margin-bottom: 24px;
            font-size: 1.0625rem;
            color: #4a5568;
            line-height: 1.75;
        }
        
        /* 表格样式 */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 32px 0;
            font-size: 1rem;
            background-color: #ffffff;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
            border-radius: 12px;
            overflow: hidden;
            transition: box-shadow 0.3s ease;
        }
        
        table:hover {
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        }
        
        table th,
        table td {
            padding: 18px 20px;
            text-align: left;
            border-bottom: 1px solid #f1f5f9;
        }
        
        table th {
            background-color: #f8fafc;
            font-weight: 600;
            color: #2d3748;
            text-transform: uppercase;
            font-size: 0.875rem;
            letter-spacing: 0.5px;
        }
        
        table tr {
            transition: background-color 0.2s ease;
        }
        
        table tr:hover {
            background-color: #f8fafc;
        }
        
        table tr:last-child td {
            border-bottom: none;
        }
        
        /* 列表样式 */
        ul, ol {
            margin: 28px 0;
            padding-left: 32px;
        }
        
        li {
            margin-bottom: 16px;
            font-size: 1.0625rem;
            color: #4a5568;
            line-height: 1.7;
            position: relative;
        }
        
        ul li::before {
            content: "•";
            color: #667eea;
            font-weight: bold;
            position: absolute;
            left: -24px;
            font-size: 1.5rem;
            line-height: 1.4;
        }
        
        li strong {
            color: #2d3748;
            font-weight: 600;
        }
        
        /* 特殊标记样式 */
        .warning {
            color: #e53e3e;
            font-weight: 700;
            margin-right: 4px;
        }
        
        .checkmark {
            color: #38a169;
            font-weight: 700;
            margin-right: 4px;
        }
        
        /* 主要板块样式 */
        section {
            margin-bottom: 56px;
            padding: 36px;
            background-color: #fafbfc;
            border-radius: 12px;
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }
        
        section:hover {
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
            transform: translateY(-2px);
        }
        
        /* 评分板块特殊样式 */
        .score-section {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            margin: 32px 0;
            padding: 40px;
            background: linear-gradient(135deg, #f0f4ff 0%, #e9ecef 100%);
            border-radius: 16px;
        }
        
        .score {
            font-size: 4rem;
            font-weight: 800;
            color: #667eea;
            margin: 20px 0;
            line-height: 1;
        }
        
        .score-label {
            font-size: 1.25rem;
            color: #4a5568;
            margin-bottom: 8px;
            font-weight: 500;
        }
        
        /* 突出显示 */
        .highlight {
            background-color: #ebf8ff;
            padding: 24px;
            border-radius: 12px;
            border-left: 4px solid #3182ce;
            margin: 28px 0;
            transition: all 0.3s ease;
        }
        
        .highlight:hover {
            box-shadow: 0 4px 16px rgba(49, 130, 206, 0.1);
        }
        
        /* 警告提示 */
        .alert-warning {
            background-color: #fffaf0;
            border-left: 4px solid #ecc94b;
            padding: 20px;
            border-radius: 8px;
            margin: 24px 0;
            color: #744210;
        }
        
        /* 成功提示 */
        .alert-success {
            background-color: #f0fff4;
            border-left: 4px solid #38a169;
            padding: 20px;
            border-radius: 8px;
            margin: 24px 0;
            color: #22543d;
        }
        
        /* 响应式设计 */
        @media (max-width: 768px) {
            body {
                padding: 0;
            }
            
            .container {
                margin: 0;
                border-radius: 0;
            }
            
            header {
                padding: 36px 24px;
            }
            
            header h1 {
                font-size: 2.25rem;
            }
            
            main {
                padding: 24px;
            }
            
            section {
                padding: 24px;
                margin-bottom: 40px;
            }
            
            h2 {
                font-size: 1.625rem;
                margin-bottom: 24px;
            }
            
            h3 {
                font-size: 1.375rem;
                margin: 32px 0 20px;
            }
            
            table {
                font-size: 0.9375rem;
                margin: 24px 0;
            }
            
            table th,
            table td {
                padding: 12px 16px;
            }
            
            .score {
                font-size: 3rem;
            }
        }
        
        @media (max-width: 480px) {
            header {
                padding: 32px 20px;
            }
            
            header h1 {
                font-size: 2rem;
            }
            
            main {
                padding: 20px;
            }
            
            section {
                padding: 20px;
            }
            
            table {
                font-size: 0.875rem;
            }
            
            table th,
            table td {
                padding: 10px 12px;
            }
        }
        
        /* 打印样式 */
        @media print {
            body {
                background: white;
            }
            
            .container {
                box-shadow: none;
                max-width: 100%;
            }
            
            section {
                break-inside: avoid;
            }
            
            table {
                break-inside: avoid;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>简历分析报告</h1>
            <div class="subtitle">{target_position}岗位匹配度评估</div> 
            <div class="date">生成时间: {{ date }}</div>
        </header>
        <main>
            {{ content }}
        </main>
    </div>
</body>
</html>
"""

def markdown_to_html(markdown_content, target_position):
    """
    将Markdown格式的简历分析报告转换为HTML格式
    
    Args:
        markdown_content: 生成的Markdown格式分析报告
        target_position: 目标岗位，用于在报告标题中显示 
        
    Returns:
        html_content: 转换后的HTML格式分析报告
    """
    # 配置Markdown扩展，使用更全面的扩展集
    extensions = [
        'tables',
        'fenced_code',
        'nl2br',
        'attr_list',
        'codehilite',
        'sane_lists',
        'md_in_html'
    ]
    
    # 转换Markdown到HTML
    html_content = markdown.markdown(markdown_content, extensions=extensions)
    
    # 自定义处理特定的格式标记
    html_content = html_content.replace('⚠️', '<span class="warning">⚠️</span>')
    html_content = html_content.replace('✅', '<span class="checkmark">✅</span>')
    
    # 为主要板块添加语义化section标签
    sections = [
        "一、评分与分析理由板块",
        "二、对照岗位 JD 逐条修改简历板块",
        "三、面试可能问的问题板块",
        "四、职业发展路径板块",
        "五、结语建议板块"
    ]
    
    for section in sections:
        html_content = html_content.replace(
            f'<h2>{section}</h2>', 
            f'<section><h2>{section}</h2>'
        )
    
    # 关闭所有section标签
    html_content = html_content + '</section>' * len(sections)
    
    # 为评分部分添加特殊样式
    html_content = html_content.replace(
        '<h3>1. 整体评分</h3>',
        '<div class="score-section"><h3 class="score-label">1. 整体评分</h3>'
    )
    html_content = html_content.replace(
        '</div>',
        '</div>',
        1  # 只替换第一个匹配项
    )
    
    # 为综合评价添加高亮样式
    if '<h3>2. 综合评价</h3>' in html_content:
        # 找到综合评价的起始和结束位置
        start_idx = html_content.find('<h3>2. 综合评价</h3>') + len('<h3>2. 综合评价</h3>')
        next_h3_idx = html_content.find('<h3>', start_idx)
        if next_h3_idx != -1:
            # 提取综合评价内容
            eval_content = html_content[start_idx:next_h3_idx]
            # 包裹高亮样式
            highlighted_eval = f'<div class="highlight">{eval_content}</div>'
            # 替换原内容
            html_content = html_content[:start_idx] + highlighted_eval + html_content[next_h3_idx:]
    
    # 处理差距总结部分，添加警告样式
    html_content = html_content.replace(
        '<h3>4. 主要差距总结</h3>',
        '<div class="alert-warning"><h3 style="margin-top: 0;">4. 主要差距总结</h3>'
    )
    html_content = html_content.replace(
        '</div>',
        '</div>',
        1  # 只替换第一个匹配项
    )
    
    # 为职业发展路径的时间阶段添加特殊样式
    career_phases = [
        '短期 (1-3年)',
        '中期 (3-5年)',
        '长期 (5年以上)'
    ]
    
    for phase in career_phases:
        html_content = html_content.replace(
            f'<h3>{phase}</h3>',
            f'<h3 style="color: #667eea; border-left: 4px solid #667eea; padding-left: 16px;">{phase}</h3>'
        )
    
    # 填充HTML模板
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    final_html = HTML_TEMPLATE.replace('{target_position}', target_position)
    final_html = final_html.replace('{{ content }}', html_content)
    final_html = final_html.replace('{{ date }}', today)
    
    return final_html

def save_html_report(html_content, filename="resume_analysis_report.html"):
    """
    将HTML内容保存为文件
    
    Args:
        html_content: HTML格式的分析报告
        filename: 保存的文件名，默认为resume_analysis_report.html
        
    Returns:
        filename: 保存的文件名
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return filename
