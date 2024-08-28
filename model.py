from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os

load_dotenv()


llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
prompt_template = """Найди все ФИО в тексте и выпиши их через запятую. Напиши их с теми же падежами, в каких они стоят в тексте. Если одна и та же ФИО встречается несколько раз, запиши её несколько раз, даже если она на другом языке. Не меняй падежи. Если записано неполная ФИО, либо отдельно Фамилия, либо имя, либо отчество, то записывай отдельно и ничего от себя не добавляй.
    КРОМЕ ФИО БОЛЬШЕ НЕ ЕДИНОГО СЛОВА НЕ ПИШИ.
    Пример:
    Гагарин полетел на орбиту на ракете Сергея Королёва
    Ответ: Гагарин, Сергея Королёва
    Текст: {text}"""
prompt = ChatPromptTemplate.from_template(prompt_template)
chain = ({'text': RunnablePassthrough()}
         | prompt
         | llm
         | StrOutputParser()
         )


async def generate_answer(text, chain):
    final_answer = []
    answer_str = await chain.ainvoke(text)
    answer_split = list(map(lambda x: str.strip(x), answer_str.split(',')))
    for per in answer_split:
        start_index = text.index(per)
        end_index = text.index(per) + len(per)
        final_answer.append([per, [start_index, end_index]])
        text = text.replace(per, ' ' * len(per), 1)

    return final_answer
