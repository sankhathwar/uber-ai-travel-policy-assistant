# Uber AI Travel Policy Assistant

An AI-powered travel policy assistant that helps employees quickly
understand company travel policies using **Retrieval-Augmented
Generation (RAG)**, an **agentic workflow**, **MCP tools**, and
**short-term conversation memory**.

------------------------------------------------------------------------

## 1. Business Problem

Employees often need to search through multiple travel-policy documents
to answer questions about:

-   Travel and ride limits
-   Expense reimbursement
-   Employee travel eligibility
-   Travel approval requirements
-   Airport transportation
-   Trip cancellation policies

Manually searching policy documents can be slow and may lead to
inconsistent interpretation of the rules.

The goal of this project is to provide a conversational AI assistant
that can retrieve the relevant policy information, use specialized tools
when required, maintain context across a conversation, and return a
concise answer with the source policy document.

------------------------------------------------------------------------

## 2. Solution

The **Uber AI Travel Policy Assistant** provides a Flask-based chat
interface where an employee can ask questions in natural language.

The application:

1.  Loads company travel-policy documents.
2.  Cleans and chunks the documents.
3.  Generates semantic embeddings.
4.  Stores the embeddings in a FAISS vector store.
5.  Retrieves the most relevant policy sections for a user question.
6.  Uses a LangGraph agent to decide when a policy tool should be
    called.
7.  Uses MCP to expose and communicate with specialized policy tools.
8.  Uses short-term conversation memory through LangGraph checkpoints.
9.  Sends the retrieved information to the Gemini LLM.
10. Returns a final response together with the source document used.

The system is designed to answer from the available policy context
rather than inventing unsupported policy information.

------------------------------------------------------------------------

## 3. Architecture

``` text
                    ┌──────────────┐
                    │     User     │
                    └──────┬───────┘
                           │
                           ▼
                ┌────────────────────┐
                │   Flask Web UI     │
                │  HTML/CSS/JS       │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │     Flask API      │
                │      /chat         │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │  LangGraph Agent   │
                │  ReAct workflow    │
                └─────────┬──────────┘
                          │
             ┌────────────┼────────────┐
             │            │            │
             ▼            ▼            ▼
        ┌─────────┐  ┌──────────┐  ┌──────────┐
        │   RAG   │  │  Tools   │  │  Memory  │
        └────┬────┘  └────┬─────┘  └────┬─────┘
             │             │             │
             ▼             ▼             │
        ┌─────────┐  ┌──────────┐        │
        │  FAISS  │  │   MCP    │        │
        │  Vector │  │  Server/ │        │
        │  Store  │  │  Client  │        │
        └────┬────┘  └────┬─────┘        │
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                   ┌──────────────┐
                   │  Gemini LLM  │
                   └──────┬───────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Final Response +   │
                │ Source Document    │
                └────────────────────┘
```

### Main Components

  Component          Responsibility
  ------------------ -----------------------------------------------
  User               Asks travel-policy questions
  Flask Web UI       Provides the chat interface
  Flask API          Receives questions and returns answers
  LangGraph Agent    Orchestrates reasoning and tool calls
  RAG                Retrieves relevant policy context
  FAISS              Stores and searches document embeddings
  MCP                Exposes specialized policy tools
  LangGraph Memory   Maintains short-term conversation context
  Gemini LLM         Generates the final natural-language response

------------------------------------------------------------------------

## 4. Technology Stack

-   **Python** --- Core programming language
-   **Flask** --- Web application and REST-style API
-   **HTML/CSS/JavaScript** --- Frontend chat interface
-   **LangChain** --- Tools and LLM integration
-   **LangGraph** --- Agent orchestration and conversation state
-   **Sentence Transformers** --- Semantic embeddings
-   **FAISS** --- Vector similarity search
-   **Gemini LLM API** --- Response generation
-   **MCP (Model Context Protocol)** --- Policy tool server/client
    communication
-   **python-dotenv** --- Environment configuration
-   **Git/GitHub** --- Version control and project repository

------------------------------------------------------------------------

## 5. RAG Workflow

The application uses Retrieval-Augmented Generation to ground responses
in the company travel-policy documents.

``` text
Documents
    ↓
Text Preprocessing
    ↓
Chunking
    ↓
Embeddings
    ↓
FAISS Vector Store
    ↓
Semantic Retrieval
    ↓
Relevant Policy Context
    ↓
Gemini LLM
    ↓
Answer + Source
```

### Step-by-step

#### 1. Documents

Policy documents are stored under the project's data directory.

Examples of policy areas include:

-   Expense policy
-   Employee eligibility
-   Travel approval
-   Airport policy
-   Cancellation policy

#### 2. Preprocessing

The ingestion pipeline cleans the document text before it is used for
retrieval.

#### 3. Chunking

Large documents are divided into smaller chunks so that relevant policy
sections can be retrieved independently.

#### 4. Embeddings

Each chunk is converted into a semantic vector using **Sentence
Transformers**.

#### 5. Vector Store

The vectors are stored in **FAISS**.

#### 6. Semantic Retrieval

When the user asks a question, the question is embedded and compared
with the stored document vectors. The most relevant chunks are
retrieved.

#### 7. LLM

The retrieved policy context is provided to the Gemini LLM, which
generates the final answer.

#### 8. Source

The response is designed to identify the source policy document used to
answer the question.

Example:

``` text
The company covers eligible airport transportation expenses.

Source: airport_policy.txt
```

------------------------------------------------------------------------

## 6. Agent Workflow

The application uses a **LangGraph ReAct agent** with specialized policy
tools.

The agent can decide when it needs to retrieve policy information or
invoke a specific tool.

### 6.1 Retrieve Policy Information

For normal policy questions, the agent can use the RAG retrieval
pipeline to find relevant policy chunks.

The retrieved context contains metadata such as:

-   Source document
-   Policy type
-   Country
-   Similarity score
-   Policy text

### 6.2 Employee Tool

The employee eligibility tool can be used when the question requires
employee-specific eligibility information.

Example:

``` text
"Is employee E123 eligible for company travel?"
```

The agent can call the employee eligibility tool rather than treating
the question as a generic policy lookup.

### 6.3 Validate a Trip

For questions involving travel approval, the agent can use the
travel-approval tool.

Example:

``` text
"Does employee E123 need approval for a $500 ride in the US?"
```

The tool receives:

-   Employee ID
-   Country
-   Amount

and retrieves the relevant approval policy.

### 6.4 Calculate / Check Reimbursement

For expense-related questions, the expense-policy tool retrieves the
relevant reimbursement policy based on:

-   Country
-   Amount

The assistant can then explain whether the expense falls within the
applicable policy.

### 6.5 Conversation Memory

Short-term conversation memory is implemented using:

``` python
InMemorySaver()
```

A Flask session stores a conversation ID, which is passed to LangGraph
as the `thread_id`.

This allows follow-up questions to use the previous conversation
context.

Example:

``` text
User: What is the travel limit in India?

Assistant: ...

User: What happens if I exceed it?

Assistant: ...
```

The second question can be interpreted using the context from the first
question.

**Important:** this is short-term in-memory memory. It is not a
persistent long-term employee memory system and is reset when the
application process restarts.

### 6.6 Final Response

After retrieval/tool execution, the Gemini LLM generates the final
response.

The response should:

-   Answer the user's question directly.
-   Use retrieved policy information.
-   Avoid unsupported claims.
-   Mention the relevant source document.
-   Preserve conversation context when applicable.

------------------------------------------------------------------------

## 7. Flask Application

### 7.1 Flask Routes

The application currently exposes two main routes.

#### `GET /`

Loads the main chat interface.

``` python
@app.route("/")
def home():
    return render_template("index.html")
```

#### `POST /chat`

Receives the user's question and sends it to the LangGraph agent.

``` python
@app.route("/chat", methods=["POST"])
def chat():
    ...
```

The frontend sends:

``` json
{
    "question": "What is the travel policy in India?"
}
```

The API returns:

``` json
{
    "success": true,
    "answer": "..."
}
```

### 7.2 Frontend / Backend Communication

The JavaScript frontend communicates with Flask using the `fetch()` API.

``` text
User enters question
        ↓
JavaScript
        ↓
POST /chat
        ↓
Flask
        ↓
LangGraph Agent
        ↓
Tools / RAG / Memory
        ↓
Gemini
        ↓
JSON Response
        ↓
JavaScript
        ↓
Chat UI
```

### 7.3 Conversation Memory

Flask sessions store a unique `conversation_id`.

The ID is passed to LangGraph as:

``` python
config={
    "configurable": {
        "thread_id": conversation_id
    }
}
```

This connects multiple requests to the same short-term conversation
checkpoint.

### 7.4 Error Handling

The application handles several failure scenarios.

#### Empty Questions

If the user submits an empty question:

``` text
Please enter a question.
```

is returned instead of calling the agent.

#### Invalid Inputs

Tool-level validation is intended for invalid values such as:

-   Invalid employee IDs
-   Invalid trip amounts
-   Unsupported tool arguments

#### Retrieval Failures

RAG retrieval failures should be caught and handled without silently
generating an unsupported answer.

#### MCP Tool Failures

Failures while communicating with the MCP server/client should be
handled and surfaced as a controlled application error.

#### API / LLM Failures

External LLM/API failures should be handled as application errors rather
than exposing internal implementation details to the user.

#### Missing Policy Documents

If the required policy information cannot be retrieved, the assistant
should indicate that the information is unavailable rather than
hallucinating a policy.

#### Unsupported Questions

Questions outside the available policy knowledge should receive a
controlled response explaining that the assistant cannot answer from the
available policy documents.

------------------------------------------------------------------------

### 7.5 UI Components

The Flask UI contains:

-   Application title
-   Chat message area
-   User messages
-   Assistant messages
-   Question input box
-   Send button
-   Enter-key submission
-   Temporary "Thinking..." status
-   Markdown-style formatting for assistant responses

The frontend is implemented using:

``` text
templates/
└── index.html

static/
├── style.css
└── script.js
```

------------------------------------------------------------------------

## 8. Testing

The application should be tested across the major policy categories,
agent tools, retrieval, conversation memory, and error handling.

### Test Cases

  ---------------------------------------------------------------------------
                     \# Test Case           Expected Result  Result
  --------------------- ------------------- ---------------- ----------------
                      1 Ask for the         Relevant India   Pass / verify
                        standard            policy is        
                        company-sponsored   retrieved and    
                        travel/ride limit   answered with    
                        in India            source           

                      2 Ask what happens    Assistant        Pass / verify
                        when the India      explains the     
                        travel limit is     applicable       
                        exceeded            policy           

                      3 Ask for the         Relevant US      Pass / verify
                        standard            policy is        
                        travel/ride limit   retrieved        
                        in the US                            

                      4 Ask what happens    Assistant        Pass / verify
                        when the US travel  explains the     
                        limit is exceeded   applicable       
                                            policy           

                      5 Ask which expenses  Expense policy   Pass / verify
                        are eligible for    is retrieved     
                        reimbursement                        

                      6 Ask for the         Expense limit is Pass / verify
                        reimbursement limit retrieved        
                        for a travel                         
                        expense                              

                      7 Ask who is eligible Eligibility      Pass / verify
                        to use company      policy is        
                        travel benefits     retrieved        

                      8 Ask for employee    Eligibility      Pass / verify
                        travel-policy       information is   
                        eligibility         returned         
                        requirements                         

                      9 Ask when manager    Approval policy  Pass / verify
                        approval is         is retrieved     
                        required                             

                     10 Ask who must        Approval         Pass / verify
                        approve an expense  information is   
                        exceeding the limit returned         

                     11 Ask which airport   Airport policy   Pass / verify
                        expenses are        is retrieved     
                        covered                              

                     12 Ask about airport   Airport policy   Pass / verify
                        transportation      is retrieved     
                        policy                               

                     13 Ask about           Cancellation     Pass / verify
                        cancellation before policy is        
                        departure           retrieved        

                     14 Ask what happens    Cancellation     Pass / verify
                        after a booking is  policy is        
                        cancelled           retrieved        

                     15 Ask a multi-part    Agent should use Pass / verify
                        question involving  relevant policy  
                        expense, approval,  context/tools    
                        and cancellation    and provide a    
                                            grounded answer  

                     16 Submit an empty     API returns a    Pass
                        question            controlled       
                                            validation       
                                            message          

                     17 Ask a follow-up     LangGraph        Pass
                        question that       short-term       
                        depends on the      memory preserves 
                        previous message    the conversation 
                                            context          

                     18 Ask an unsupported  Assistant should Pass / verify
                        policy question     not invent a     
                                            policy answer    
  ---------------------------------------------------------------------------

### Memory Test

Short-term memory was separately verified using LangGraph checkpointing.

Example:

``` text
First message:
"My name is Sankalp."

Follow-up:
"What is my name?"
```

The checkpointed conversation retained the earlier message,
demonstrating that the configured LangGraph memory mechanism works.

### Testing Note

The table above separates **verified implementation behavior** from test
cases that should be executed against the current policy dataset. The
README intentionally does not fabricate policy-specific pass/fail
results when an observed test output has not been recorded.

For a final project submission, the `Pass / verify` entries should be
replaced with the actual result observed during the final test run.

------------------------------------------------------------------------

## 9. Prompt Improvements

Prompt engineering was used to make the assistant more reliable and
grounded.

### Initial Prompt

A basic prompt can be represented as:

``` text
You are a travel policy assistant.

Answer the user's question using the provided policy information.
```

This provides the model with a role but does not strongly enforce source
grounding or explain how unsupported questions should be handled.

### Improved Prompt

The improved role-based prompt should follow these principles:

``` text
You are an AI Travel Policy Assistant.

Your job is to answer employee questions using the provided company
travel-policy context.

Rules:

1. Answer only from the provided policy context.
2. Do not invent or assume policy rules that are not present.
3. If the policy context does not contain enough information, clearly
   say that the information is unavailable.
4. Use the relevant tool when the question requires employee eligibility,
   travel approval, expense, airport, or cancellation information.
5. Consider previous conversation context when answering follow-up questions.
6. Give a concise and easy-to-understand explanation.
7. Always mention the source policy document used for the answer.
8. If multiple policy documents were used, list all relevant sources.
9. Distinguish policy facts from any explanation or interpretation.

At the end of the response, include:

Source: <policy document filename>
```

### Why the Prompt Was Improved

The improved prompt addresses several common RAG/agent problems:

-   Reduces hallucination.
-   Encourages use of the correct tool.
-   Makes source attribution explicit.
-   Handles missing information more safely.
-   Supports conversational follow-up questions.
-   Produces more consistent responses.

------------------------------------------------------------------------

## 10. Limitations

The current system has several limitations.

### 10.1 Policy Knowledge Is Limited to Available Documents

The assistant can only provide reliable policy answers based on the
documents available in its knowledge base.

If a policy is missing from the documents, the assistant cannot reliably
answer it.

### 10.2 Short-Term Memory Only

The current memory implementation uses `InMemorySaver`.

Conversation state is not intended to be a permanent employee history.

Restarting the application process clears the in-memory conversation
state.

### 10.3 LLM Dependency

The application depends on the configured Gemini LLM API.

API failures, rate limits, authentication problems, or service outages
can prevent response generation.

### 10.4 Retrieval Quality

RAG quality depends on:

-   Document quality
-   Chunk size
-   Chunk overlap
-   Embedding quality
-   Similarity search
-   Policy-document structure

Poorly structured or ambiguous documents can result in less relevant
retrieval.

### 10.5 Tool Coverage

The agent currently has a defined set of specialized policy tools:

-   Expense policy
-   Employee eligibility
-   Travel approval
-   Airport policy
-   Cancellation policy

Questions requiring information outside these tools and the available
policy documents may not be answerable.

### 10.6 No Real Transaction Execution

The assistant provides policy guidance.

It does not actually:

-   Book a ride
-   Book a flight
-   Submit an expense claim
-   Approve a trip
-   Cancel a real trip
-   Modify an employee's account

### 10.7 Policy Interpretation

The system provides information from policy documents but does not
replace an official HR, travel, finance, or manager decision.

### 10.8 No Long-Term Employee Profile

The current implementation does not maintain a persistent employee
profile or long-term personalized travel history.

### 10.9 Input Validation

The application includes validation and error-handling paths, but
production deployment would require stronger validation, logging,
authentication, authorization, monitoring, and security controls.

------------------------------------------------------------------------

## Project Structure

``` text
uber-ai-travel-policy-assistant/
│
├── data/
│   └── company_policy/
│
├── src/
│   ├── agent.py
│   ├── chunking.py
│   ├── config.py
│   ├── ingestion.py
│   ├── llm.py
│   ├── mcp_server.py
│   ├── mcp_tool_client.py
│   ├── metadata.py
│   ├── preprocessing.py
│   ├── prompts.py
│   ├── rag_pipeline.py
│   ├── retriever.py
│   └── tools.py
│
├── mcp/
├── models/
├── notebooks/
├── tests/
├── vector_store/
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

------------------------------------------------------------------------

## Running the Application

### 1. Activate the virtual environment

``` bash
cd ~/Documents/AICapProject/uber-ai-travel-policy-assistant
source venv/bin/activate
```

### 2. Configure environment variables

Create a `.env` file and provide the required Gemini API key and
application configuration.

Example:

``` text
GOOGLE_API_KEY=your_api_key
FLASK_SECRET_KEY=your_secret_key
```

Do not commit `.env` to GitHub.

### 3. Start the MCP server

From the project root:

``` bash
python -m src.mcp_server
```

The MCP server is configured to use the application's MCP endpoint.

### 4. Start Flask

In another terminal:

``` bash
cd ~/Documents/AICapProject/uber-ai-travel-policy-assistant
source venv/bin/activate
python app.py
```

The Flask application runs on:

``` text
http://127.0.0.1:5000
```

Open the address in a browser and use the chat interface.

------------------------------------------------------------------------

## Conclusion

The Uber AI Travel Policy Assistant combines **RAG, semantic search,
agentic tool calling, MCP, LangGraph memory, and a Flask web
application** into a single conversational travel-policy solution.

The architecture separates document retrieval, policy tools, agent
orchestration, conversation memory, and LLM response generation, making
the project suitable as a foundation for a more production-ready
enterprise travel-policy assistant.
