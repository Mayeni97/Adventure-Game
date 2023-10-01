from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from langchain.memory import ConversationBufferMemory, CassandraChatMessageHistory
from langchain.llms import OpenAI
from langchain import LLMChain, PromptTemplate
import json


cloud_config= {
  'secure_connect_bundle': 'secure-connect-adventure-game.zip'
}

with open("Adventure_Game-token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]
ASTRA_DB_KEYSPACE = "database"
OPENAPI_API_KEY = "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"


auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

message_history = CassandraChatMessageHistory(
    session_id = "anything",
    session = session,
    keyspace = ASTRA_DB_KEYSPACE,
    ttl_seconds =3600
)

message_history.clear()

cass_buff_memory = ConversationBufferMemory(
    memory_key = "chat_history",
    chat_memory = message_history
)

template = """you play as Alex Nova, a brilliant quantum physicist who has discovered the existence of a mysterious and powerful device known as the Chrono Nexus. The Chrono Nexus has the ability to manipulate time and reality, and it has fallen into the wrong hands. Your goal is to embark on a thrilling sci-fi adventure to retrieve the Chrono Nexus, prevent it from causing catastrophic temporal anomalies, and ultimately save the future of humanity.
 
Rules to follow:
1. Explore Everything: Check every place for hidden items and clues.
2. Talk to Everyone: Talk to the characters you meet; they might have useful info.
3. Think Before Acting: Before making decisions or solving puzzles, take a moment to consider your options.
4. Watch for Consequences: Understand that your choices affect the game's outcome.
5. Manage Resources: Keep an eye on your supplies and use them wisely.
6. Plan Space Battles: Use tactics in space battles and retreat if necessary.

Here is the chat history, use this to understand what to say next: {chat_history}
human: {human_input}
AI:"""




prompt = PromptTemplate(
    input_variables = ["chat_history","human_input"]
)

llm = OpenAI(OPENAPI_API_KEY= OPENAPI_API_KEY)
LLMChain = LLMChain(
    llm = llm,
    prompt = "prompt",
    memory = cass_buff_memory
)

response = llm_chain.predict(human_input= "start the game")
print(response)

