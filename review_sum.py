import base64

from langchain_core.messages import HumanMessage
from langchain_google_vertexai import ChatVertexAI, VertexAI

with open("image_example.png", "rb") as image_file:
    image_bytes = image_file.read()
# model = VertexAI(model_name="gemini-pro")
llm = ChatVertexAI(model_name="gemini-ultra-vision",project="gdsc-solution-project-412006",)

image_message = {
    "type": "image_url",
    "image_url": {
        "url": f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode('utf-8')}"
    },
}
text_message = {
    "type": "text",
    "text": "What is shown in this image?",
}
message = HumanMessage(content=[text_message, image_message])

output = llm.invoke([message])
print(output.content)

