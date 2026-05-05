# [Document types for Gemini Enterprise Agent Platform RAG Engine](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/supported-documents.md.txt)

The [VPC-SC security controls](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/security-controls) and
CMEK are supported by Agent Platform RAG Engine. Data residency and AXT security controls aren't
supported.

The default parser supports the following file types and their file size limits:

| File type | File size limit |
|---|---|
| Google documents | 10 MB when exported from Google Workspace |
| Google drawings | 10 MB when exported from Google Workspace |
| Google slides | 10 MB when exported from Google Workspace |
| HTML file | 10 MB |
| JSON file | 10 MB |
| JSONL or NDJSON file | 10 MB |
| Markdown file | 10 MB |
| Microsoft PowerPoint slides (PPTX file) | 10 MB |
| Microsoft Word documents (DOCX file) | 50 MB |
| PDF file | 50 MB |
| Text file | 10 MB |

Additional file types are supported by an [Llm Parser](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/llm-parser).

Using Gemini Enterprise Agent Platform RAG Engine with other document types is possible but
can generate lower-quality responses.

## What's next

- [Fine-tune RAG transformations](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/fine-tune-rag-transformations)