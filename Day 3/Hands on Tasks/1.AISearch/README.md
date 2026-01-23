# Azure AI Search - Integrated Vectorization

This folder contains scripts for setting up Azure AI Search with integrated vectorization for the Student Loan Guide documents.

## 📋 Overview

This solution implements a complete Azure AI Search pipeline with:
- **Blob Storage Integration**: Upload documents to Azure Blob Storage
- **Automated Indexing**: Use Azure AI Search indexers for automated processing
- **Text Chunking**: Split documents into manageable chunks
- **Vector Embeddings**: Generate embeddings using Azure OpenAI
- **Multiple Search Types**: Support for vector, hybrid, and semantic searches

## 🏗️ Architecture

```
StudentLoanGuide.pdf
    ↓
Azure Blob Storage
    ↓
Azure AI Search Indexer
    ↓
Skillset (Text Split + Embeddings)
    ↓
Search Index (Vector + Keyword)
    ↓
Search Queries (Vector/Hybrid/Semantic)
```

## 📁 Files

### 1. `upload_to_blob.py`
Uploads the `StudentLoanGuide.pdf` to Azure Blob Storage.

**Features:**
- Reads connection string from `.env` file
- Creates container if it doesn't exist
- Uploads PDF with overwrite option
- Lists all blobs in container

**Usage:**
```bash
python upload_to_blob.py
```

### 2. `setup_search_index.py`
Creates the complete Azure AI Search infrastructure:
- Blob data source connector
- Search index with vector and semantic configurations
- Skillset with text splitting and embedding skills
- Indexer to automate the process

**Features:**
- Creates HNSW-based vector search index
- Configures semantic search capabilities
- Sets up automated chunking (2000 chars with 500 char overlap)
- Uses Azure OpenAI for embeddings (text-embedding-ada-002)

**Usage:**
```bash
python setup_search_index.py
```

### 3. `search_queries.py`
Performs different types of searches on indexed documents.

**Search Types:**
1. **Vector Similarity Search**: Pure semantic search using embeddings
2. **Hybrid Search**: Combines vector + BM25 keyword search
3. **Hybrid + Semantic Reranking**: Hybrid search with L2 reranking

**Features:**
- Interactive mode for custom queries
- Example queries included
- Formatted results with scores
- Semantic captions and reranker scores

**Usage:**
```bash
python search_queries.py
```

### 4. `check_indexer_status.py`
Monitor indexer execution status and troubleshoot issues.

**Features:**
- Check current indexer status
- View execution history
- Run indexer manually
- Reset indexer
- Continuous monitoring mode

**Usage:**
```bash
python check_indexer_status.py
```

### 5. `requirements.txt`
Python package dependencies.

**Important:** Uses Azure SDK beta version `11.6.0b12` for integrated vectorization support.

**Install:**
```bash
pip install -r requirements.txt
```

## 🚀 Getting Started

### Prerequisites

1. **Azure Resources:**
   - Azure Storage Account (Blob Storage)
   - Azure AI Search service
   - Azure OpenAI service with text-embedding-ada-002 deployment

2. **Environment Variables:**
   Ensure your `.env` file in the workspace root contains:

```env
# Azure AI Search
AZURE_AI_SERVICES_KEY=your_search_key
AZURE_AI_SERVICES_ENDPOINT=https://your-search.search.windows.net

# Azure Blob Storage
BLOB_CONNECTION_STRING=your_connection_string
BLOB_CONTAINER_NAME=agent-loan-processing

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com/
AZURE_OPENAI_KEY=your_openai_key
AZURE_OPENAI_ADA002_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
```

### Step-by-Step Setup

#### Step 1: Install Dependencies
```bash
cd Pre_Processing_Index
pip install -r requirements.txt
```

#### Step 2: Place the PDF File
Place `StudentLoanGuide.pdf` in one of these locations:
- `Pre_Processing_Index/StudentLoanGuide.pdf`
- `data/StudentLoanGuide.pdf`
- `input/StudentLoanGuide.pdf`

#### Step 3: Upload to Blob Storage
```bash
python upload_to_blob.py
```

Expected output:
```
✓ Container 'agent-loan-processing' already exists
📤 Uploading 'StudentLoanGuide.pdf' to blob storage...
✅ Successfully uploaded to: https://...blob.core.windows.net/...
```

#### Step 4: Set Up Search Infrastructure
```bash
python setup_search_index.py
```

This will:
1. ✓ Create blob data source connector
2. ✓ Create search index with vector and semantic search
3. ✓ Create skillset with:
   - SplitSkill for text chunking
   - AzureOpenAIEmbeddingSkill for vectorization
   - Index projections for chunk mapping
4. ✓ Create and run indexer

**Note:** The indexer may take 1-2 minutes to process the document and create searchable chunks.

#### Step 5: Run Searches
```bash
python search_queries.py
```

Choose from:
1. Run example queries (automated)
2. Interactive search mode (custom queries)

## 🔍 Search Types Explained

### 1. Vector Similarity Search
- **Method**: Pure semantic search using embeddings
- **Best for**: Finding conceptually similar content
- **How it works**: Converts query to embeddings, finds nearest neighbors using cosine similarity

### 2. Hybrid Search
- **Method**: Combines vector search + BM25 keyword search
- **Best for**: Balancing semantic and exact matches
- **How it works**: Merges results from both vector and keyword searches using RRF (Reciprocal Rank Fusion)

### 3. Hybrid Search + Semantic Reranking
- **Method**: Hybrid search with L2 reranking using Microsoft Bing models
- **Best for**: Highest quality results with deep understanding
- **How it works**: Initial hybrid search followed by transformer-based reranking
- **Features**: 
  - Extractive captions (highlighted relevant parts)
  - Extractive answers (direct answers from content)
  - Reranker scores (quality metrics)

## 📊 Index Configuration

### Fields
- `chunk_id`: Unique identifier (key)
- `parent_id`: Parent document identifier
- `chunk`: Text content (searchable)
- `title`: Document title (searchable, filterable)
- `vector`: Embedding vector (1536 dimensions)

### Vector Search
- **Algorithm**: HNSW (Hierarchical Navigable Small World)
- **Configuration**: Default HNSW settings with cosine similarity
- **Dimensions**: 1536 (Azure OpenAI text-embedding-ada-002)
- **Profile**: vector-profile with hnsw-config

### Chunking
- **Size**: 2000 characters per chunk
- **Overlap**: 500 characters between chunks
- **Method**: Page-based splitting via SplitSkill

### Index Projections
- **Purpose**: Maps skill output (chunks + vectors) to index fields
- **Mode**: SKIP_INDEXING_PARENT_DOCUMENTS (only index chunks, not full document)
- **Location**: Defined in skillset (not indexer)
- **Result**: Each chunk becomes a searchable document

## 🛠️ Troubleshooting

### Issue: "File not found"
**Solution**: Ensure `StudentLoanGuide.pdf` is in one of the search paths listed in Step 2.

### Issue: "Environment variable not set"
**Solution**: Check your `.env` file in the workspace root contains all required variables.

### Issue: "ImportError for Azure SDK classes"
**Solution**: 
1. Ensure you're using `azure-search-documents==11.6.0b12` (beta version)
2. Run: `pip install azure-search-documents==11.6.0b12 --upgrade`
3. The stable version (11.4.0) doesn't support integrated vectorization

### Issue: "Indexer succeeds but no search results"
**Solution**:
1. Index projections must be in the skillset, not the indexer
2. Run `python check_indexer_status.py` to verify items processed > 0
3. Check Azure Portal → Index → Documents count should show multiple chunks

### Issue: "No search results"
**Solution**:
1. Wait for indexer to complete (check status: `python check_indexer_status.py`)
2. Verify the document was chunked (should see multiple documents in index)
3. Try different queries or check index in Azure Portal

## 📈 Monitoring

### Check Indexer Status
You can check the indexer status in:
1. Azure Portal → Azure AI Search → Indexers
2. Or add to `setup_search_index.py`:
```python
status = indexer_client.get_indexer_status(INDEXER_NAME)
print(f"Status: {status.status}")
```

### View Index Statistics
Azure Portal → Azure AI Search → Indexes → student-loan-guide-index

## 🔗 Resources

- [Azure AI Search Documentation](https://learn.microsoft.com/azure/search/)
- [Integrated Vectorization](https://learn.microsoft.com/azure/search/vector-search-integrated-vectorization)
- [Sample Repository](https://github.com/Azure/azure-search-vector-samples)
- [Vector Search Overview](https://learn.microsoft.com/azure/search/vector-search-overview)
- [Semantic Search](https://learn.microsoft.com/azure/search/semantic-search-overview)

## 💡 Tips

1. **Large Documents**: For documents >100 pages, consider increasing chunk size
2. **Query Optimization**: Start with hybrid+semantic for best quality results
3. **Cost Management**: Monitor Azure OpenAI token usage for embeddings
4. **Index Updates**: Indexer can run on a schedule for automatic updates
5. **Testing**: Use the interactive mode in `search_queries.py` to experiment with different queries

## 📝 Example Queries

Try these queries with the search script:

```python
"What are the eligibility requirements for student loans?"
"How do I apply for a student loan?"
"What are the repayment options available?"
"Can I defer my student loan payments?"
"What is the interest rate on student loans?"
"Tell me about loan forgiveness programs"
"How does income-driven repayment work?"
```

## 🎯 Next Steps

1. **Integration**: Integrate search into your loan processing workflow
2. **Customization**: Adjust chunking strategy based on document structure
3. **Scale**: Add more documents to the blob container
4. **Monitoring**: Set up Application Insights for query analytics
5. **Optimization**: Fine-tune vector search parameters based on results

## 📧 Support

For issues or questions:
1. Check Azure Portal for service health
2. Review Azure AI Search logs
3. Consult the Azure documentation links above

---

**Last Updated**: October 22, 2025
**Version**: 1.0.0
