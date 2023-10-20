from langchain.embeddings import OpenAIEmbeddings
import os
openai_api_key = os.environ.get('OPENAI_API_KEY')
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
markdown_content = """

# Case 1
## First case
### Isidoro A. Lucena, Applicant  vs. Diablo Auto Body; Liberty; Mutual Insurance;
#### Background:
WORKERS' COMPENSATION APPEALS BOARD STATE OF CALIFORNIA Isidoro A. Lucena, Applicant  vs. Diablo Auto Body; Liberty; Mutual Insurance; ﻿Sun Valley Ford; Great States Insurance, Defendant(s).  Case No. WCK 037874 OPINION AND DECISION AFTER RECONSIDERATION (OPINION AND ORDER VACATING ORDER GRANTING RECONSIDERATION AND ORDER DISMISSING PETITION FOR RECONSIDERATION) ﻿ I . 1 II .DISCUSSION  shall be verified upon oath in the manner required for verified pleadings in courts of record ... .” Thus, there is a clear and specific statutory requirement that petitions be verified. 2 Petitioner, as noted above, has not done so and, despite notice from the WCJ in his Report that the petition was not verified as required by section 5902, petitioner has not filed a verification late or otherwise. Petitioner has not offered a compelling reason, or indeed any reason, for the lack of verification after specific notice of the absence thereof. Therefore, we will dismiss the petition for failure to comply with section 5902. (See Conner v. Workers’ Comp. Appeals Bd. Wings West Airlines v. Workers’ Comp. Appeals Bd. (Nebelon)  (1986) 187 Cal.App.3d 1047, 1055 ; Mullane v. Industrial Acc. Com.  (1931) 118 Cal. App. 283, 286 .) Further, on this record, we see no basis 2 3 4     IT IS HEREBY ORDERED VACATED. 3 4 Wings West Airlines v. Workers’ Comp. Appeals Bd. (Nebelon), supra,  187 Cal.App.3d at p. 1055 ; Mullane v. Industrial Acc. Com., supra,  118 Cal. App. at p. 286 ) and, of course, we have the discretion not to dismiss unverified petitions. (E.g. Detherage v. Workers' Comp. Appeals Bd.  (1998) 63 Cal.Comp.Cases 803 (writ den.); Lorenz v. Workers' Comp. Appeals Bd.  (1995) 60 Cal.Comp.Cases 511 (writ den.); Pacific Telephone & Telegraph Co. v. Workers' Comp. Appeals Bd. (Nichols)  (1983) 48 Cal.Comp.Cases 530 (writ den.); Arko v. Workers' Comp. Appeals Bd.  (1982) 47 Cal.Comp.Cases 1281 (writ den.); General Telephone & Electric v. Workers' Comp. Appeals Bd. (Tortorice) IT IS FURTHER ORDERED DISMISSED. WORKERS' COMPENSATION APPEALS BOARD ﻿/s/ Merle C. Rabine   ﻿I CONCUR, ﻿ ﻿ /s/ Robert N. Ruggles ﻿/s/ Dennis J. Hannigan ﻿DATED AND FILED AT SAN FRANCISCO, CALIFORNIA  December 7, 2000 SERVICE BY MAIL ON SAID DATE TO ALL PARTIES AS SHOWN ON THE OFFICIAL ADDRESS RECORD EXCEPT LIEN CLAIMANTS.
# Case 2
## Second case
### LES HALL, Applicant, vs. VALLEY MEDIA and LEGION INSURANCE COMPANY,
#### Background:
WORKERS' COMPENSATION APPEALS BOARD STATE OF CALIFORNIA LES HALL, Applicant, vs. VALLEY MEDIA and LEGION INSURANCE COMPANY, Defendants Case No. SAC 309589 OPINION AND DECISION AFTER RECONSIDERATION AND ORDER DISMISSING PETITION FOR REMOVAL 1  BACKGROUND ll court actions, arbitrations and mediations currently or hereafter pending against an insured of Legion in the Commonwealth of Pennsylvania or elsewhere are stayed for ninety (90) days from the effective date of this Order or such additional time as the Rehabilitator may request.” 2 DISCUSSION : “ workmen’s compensation release  upon a higher plane than a private contractual release; it is a judgment, with ‘the same force and effect as an award made after a full hearing.’ (Raischell & Cottrell, Inc. v. Workmen's Comp. Appeals Bd. (1967) 249 Cal.App.2d 991, 997 .)”3 3 4 4  IT IS ORDERED AFFIRMED DELETED IT IS FURTHER ORDERED DISMISSED WORKERS’ COMPENSATION APPEALS BOARD ﻿ ____________________________________________________ I CONCUR, DATED AND FILED AT SAN FRANCISCO, CALIFORNIA SERVICE BY MAIL ON ALL PARTIES EXCEPT LIEN CLAIMANTS AS SHOWN ON THE OFFICIAL ADDRESS RECORD EFFECTED ON ABOVE DATE Reserved with page 2 Sept. 12, 2002 csl
"""
from langchain.text_splitter import MarkdownHeaderTextSplitter

headers_to_split_on = [
    ("#", "Case Number"),
    ("##", "Case No."),
    ("###", "Name of case"),
    ("####","Subheadings")
]

markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
md_header_splits1 = markdown_splitter.split_text(markdown_content)
md_header_splits1
# Define our text splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

chunk_size = 2500
chunk_overlap = 0
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size, chunk_overlap=chunk_overlap
)
all_splits = text_splitter.split_documents(md_header_splits1)

from langchain.vectorstores import FAISS
db = FAISS.from_documents(all_splits, embeddings)

retriever = db.as_retriever()
retriever.get_relevant_documents("Workers compensation")
from langchain.tools import BaseTool, StructuredTool, Tool, tool
@tool("search", return_direct=True)
def search_document(query: str) -> str:
    """Searches and returns documents regarding the legal cases"""
    docs = retriever.get_relevant_documents(query)
    return str(docs)
tools = [search_document]
memory_key="demo-v6"
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(memory_key=memory_key, return_messages=True)
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.schema import SystemMessage
from langchain.prompts import MessagesPlaceholder
system_message = SystemMessage(
        content=(
            "Do your best to answer the questions. "
            "Feel free to use any tools available to look up "
            "relevant information, only if neccessary"
        )
)
prompt = OpenAIFunctionsAgent.create_prompt(
        system_message=system_message,
        extra_prompt_messages=[MessagesPlaceholder(variable_name=memory_key)]
    )

from langchain.chat_models import ChatOpenAI
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
llm = ChatOpenAI(temperature = 0, openai_api_key=openai_api_key)

agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)

from langchain.agents import AgentExecutor
agent_executor2 = AgentExecutor(agent=agent,memory=memory, tools=tools,verbose=True)

from fastapi import FastAPI
from fastapi import HTTPException

app = FastAPI()

@app.post("/chat/")
async def process_text(input_text: str):
    # Perform some processing on the input text (you can replace this with your own logic)
    result = agent_executor2({"input": input_text})
    
    # Return the processed text
    return {"processed_text": result["output"]}


