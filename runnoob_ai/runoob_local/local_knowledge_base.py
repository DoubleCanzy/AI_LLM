# 文件路径：/Users/runoob/local_knowledge_base.py
# 完全离线的本地知识库 RAG 系统

# 先安装依赖：
# pip install langchain langchain-ollama chromadb pypdf

from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
import os


class LocalKnowledgeBase:
    """本地知识库类，实现完全离线的 RAG 功能"""

    def __init__(self, model_name: str = "llama3", persist_dir: str = "./chroma_db"):
        """
        初始化知识库

        Args:
            model_name: 使用的 Ollama 模型名称
            persist_dir: 向量数据库持久化目录
        """
        self.model_name = model_name
        self.persist_dir = persist_dir

        # 1. 初始化 LLM（本地模型）
        self.llm = OllamaLLM(model=model_name)

        # 2. 初始化嵌入模型（本地嵌入）
        # 使用 nomic-embed-text，这个模型对中英文都不错
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")

        # 3. 向量数据库占位
        self.vector_store = None
        self.qa_chain = None

    def load_documents(self, document_paths: list):
        """
        加载文档并构建向量数据库

        Args:
            document_paths: 文档路径列表
        """
        documents = []

        for path in document_paths:
            if not os.path.exists(path):
                print(f"警告：文件 {path} 不存在，跳过")
                continue

            # 根据文件扩展名选择加载器
            if path.lower().endswith(".pdf"):
                loader = PyPDFLoader(path)
            elif path.lower().endswith(".txt"):
                loader = TextLoader(path, encoding="utf-8")
            else:
                print(f"警告：不支持的文件类型 {path}，跳过")
                continue

            documents.extend(loader.load())
            print(f"已加载：{path}")

        if not documents:
            print("没有成功加载任何文档")
            return

        print(f"总共加载了 {len(documents)} 个文档片段")

        # 4. 切分文档
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,      # 每个块 500 个字符
            chunk_overlap=100    # 块之间重叠 100 个字符
        )
        split_docs = text_splitter.split_documents(documents)
        print(f"切分成 {len(split_docs)} 个片段")

        # 5. 构建向量数据库
        print("正在构建向量数据库...")
        self.vector_store = Chroma.from_documents(
            documents=split_docs,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )
        print("向量数据库构建完成！")

        # 6. 构建问答链
        self._build_qa_chain()

    def _build_qa_chain(self):
        """构建 RAG 问答链"""
        if not self.vector_store:
            print("请先加载文档！")
            return

        # 构建检索器
        retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}  # 返回最相关的 3 个片段
        )

        # 构建 RAG 链
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )

    def load_existing_db(self):
        """加载已有的向量数据库"""
        if os.path.exists(self.persist_dir):
            self.vector_store = Chroma(
                persist_directory=self.persist_dir,
                embedding_function=self.embeddings
            )
            self._build_qa_chain()
            print("已加载现有的向量数据库")
            return True
        else:
            print("没有找到现有的向量数据库")
            return False

    def ask(self, question: str) -> dict:
        """
        向知识库提问

        Args:
            question: 问题

        Returns:
            包含答案和参考来源的字典
        """
        if not self.qa_chain:
            return {"error": "请先加载文档或现有数据库！"}

        # 构造提示词模板，鼓励中文回答
        result = self.qa_chain.invoke({
            "query": f"""请用中文回答以下问题。如果答案在上下文中，请明确指出。
如果上下文中没有答案，请诚实说"根据提供的资料无法回答"。

问题：{question}
"""
        })

        return {
            "question": question,
            "answer": result["result"],
            "sources": [doc.page_content for doc in result["source_documents"]]
        }


# ============================================
# 使用示例
# ============================================

if __name__ == "__main__":
    # 1. 创建知识库实例
    kb = LocalKnowledgeBase(model_name="qwen")  # 用 Qwen，中文更好

    # 2. 尝试加载已有数据库，否则加载文档
    if not kb.load_existing_db():
        # 准备一些文档，比如把一些 RUNOOB 教程存为 txt
        sample_docs = [
            "/Users/runoob/documents/runoob_python_tutorial.txt",
            "/Users/runoob/documents/company_handbook.pdf",
        ]
        kb.load_documents(sample_docs)

    # 3. 交互式问答
    print("=" * 50)
    print("Runoob 本地知识库已启动！")
    print("输入你的问题，或输入 'quit' 退出")
    print("=" * 50)

    while True:
        user_input = input("\n你的问题：")

        if user_input.lower() in ["quit", "exit", "退出"]:
            print("再见！")
            break

        if not user_input.strip():
            continue

        # 提问
        result = kb.ask(user_input)

        if "error" in result:
            print(f"错误：{result['error']}")
            continue

        print(f"\n回答：{result['answer']}")
        print("\n参考来源：")
        for i, source in enumerate(result["sources"], 1):
            print(f"\n[{i}] {source[:200]}...")