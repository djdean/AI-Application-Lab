from openai import OpenAI
def main():
    #Go over the SDK and how to connect to AOAI programatically using the API. 
    #Simple prompting
    print("Connecting to Azure OpenAI...")
    endpoint="https://sweden-central-aoai-dade.openai.azure.com/openai/v1"
    openai_key = "17a0c23410f04fc09d3037b1972e3e5e"
    model = "gpt-5.2-chat"
    client = OpenAI(
            base_url = endpoint, 
            api_key=openai_key,  
        )
    print("Done!\n\n")
    question = ""
    while True:
        question = input("\nEnter a question to ask "+model+ " or 'exit' to quit:\n")
        if question == "exit":
             exit(0)
        answer = answer_question(question,client,model)
        print("Answer:\n\n"+answer["content"]+"\n\n")
def assess_result(question,answer,client, model):
    response = client.chat.completions.create(
        model=model, # model = "deployment_name".
        messages=[
            {"role": "system", "content": "You are an AI assistant extremely proficient in assessing the confidence of answers coming from different users."},
            {"role": "user", "content": "\n\nBased on the following question: "+question+\
             "\n\nIs the following answer complete?\n\nAnswer:\n\n"+answer+"\n\n Respond yes or no."},
             
        ]
    )
    result = response.choices[0].message.content
    return result
def answer_question(question,client, model):
    response = client.chat.completions.create(
        model=model, # model = "deployment_name".
        messages=[
            {"role": "system", "content": "You are an AI assistant extremely proficient in answering questions coming from different users. You are extremely sarcastic, please incorporate that into your responses."},
            {"role": "user", "content": "\n\nAnswer the following question:\n\n"+question},
        ]
    )
    result = {
        "content": response.choices[0].message.content
    }
    return result
           
if __name__ == "__main__":
    main()

