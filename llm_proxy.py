#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大模型API代理层
负责封装大模型API调用，实现密钥注入、请求转发、异常捕获等功能
"""

import os
import logging
from openai import OpenAI
from typing import Optional, Dict, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LLMProxy:
    """大模型API代理类"""
    
    def __init__(self):
        """初始化代理"""
        self.api_key = os.getenv('LLM_API_KEY')
        self.base_url = os.getenv('LLM_API_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
        self.model = os.getenv('LLM_MODEL', 'qwen-plus')
        
        # 验证配置
        if not self.api_key:
            logger.error("大模型API密钥未配置，请设置LLM_API_KEY环境变量")
            raise ValueError("大模型API密钥未配置")
        
        # 初始化OpenAI客户端
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )
    
    def analyze_resume(self, resume_text: str, jd_text: str, target_position: str) -> str:
        """
        分析简历与岗位匹配度
        
        Args:
            resume_text: 简历文本内容
            jd_text: 职位JD文本内容
            target_position: 目标岗位
            
        Returns:
            分析结果文本
        """
        if not resume_text:
            return "请输入简历内容"
        if not jd_text:
            return "请输入JD内容"
        if not target_position:
            return "请输入目标岗位"
        
        try:
            prompt = f"请基于以下候选人简历文本、目标岗位和JD文本，生成一份结构清晰、核心信息用表格呈现的岗位匹配度分析报告，严格遵循以下模块和格式要求：\n\n### 输入材料\n1. 候选人简历文本：{resume_text}\n2. 目标岗位：{target_position}\n3. 目标岗位 JD 文本：{jd_text}\n\n### 输出格式要求\n---\n## 一、评分与分析理由板块\n1. **整体评分**：给出0-10分的综合得分\n2. **综合评价**：150字左右的总述，突出匹配亮点与核心短板\n3. **维度拆解分析**：必须用表格呈现，表格列固定为「维度|评分 (/10)|分析理由」，维度包含：\n   - 岗位匹配度\n   - 工作经验相关性\n   - 技能掌握程度\n   - 教育背景契合度\n   - 软技能与岗位适配性\n4. **主要差距总结**：用项目符号列出3-5条最核心的不匹配点\n\n---\n## 二、对照岗位 JD 逐条修改简历板块\n必须用表格呈现，表格列固定为「简历现有内容|岗位 JD 要求|差异分析|修改建议」，需将简历中所有与 JD 相关的条目逐一对应分析，并给出可直接替换的改写话术。\n\n---\n## 三、面试可能问的问题板块\n列出8-10个高针对性问题，每个问题后用「⚠️」标注考察点，例如：\n1. 你在实习中提到「构建多维度测评体系」，能否详细说明你是如何定义「准确性」和「逻辑性」的？⚠️ 考察数据质量把控能力和标准化思维\n\n---\n## 四、职业发展路径板块\n分「短期 (1-3年)」「中期 (3-5年)」「长期 (5年以上)」三个阶段，每个阶段包含：\n- 目标职位\n- 核心任务 / 能力升级重点\n- 行动建议（用「✅」标注具体动作）\n\n---\n## 五、结语建议板块\n给候选人的投递/面试策略总结，3-4条可落地的行动建议。\n\n---\n### 格式约束\n- 所有对比类、评分类内容必须用表格呈现，禁止纯文本堆砌\n- 每个板块用「---」分隔，标题用「#」「##」分级，保持视觉清晰\n- 语言需专业、简洁，避免冗余表述\n\n要求分析全面、具体，避免模板化回复，完全基于提供的JD和简历内容"

            # 记录调用开始
            logger.info(f"开始分析简历，目标岗位：{target_position}")
            
            # 调用大模型API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是专业简历分析助手，具有5年以上招聘经验，对AI产品经理等岗位有深入理解"},
                    {"role": "user", "content": prompt}
                ]
            )
            
            # 记录调用成功
            logger.info(f"简历分析完成，目标岗位：{target_position}")
            
            return response.choices[0].message.content
            
        except Exception as e:
            # 避免泄露密钥相关错误信息
            logger.error(f"大模型API调用失败：{str(e)}")
            return "服务暂时不可用，请稍后重试"

# 创建全局代理实例
llm_proxy = None
try:
    llm_proxy = LLMProxy()
    logger.info("大模型API代理初始化成功")
except Exception as e:
    logger.error(f"大模型API代理初始化失败：{str(e)}")
